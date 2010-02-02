# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 

import racy
import racy.rlog     as rlog
import racy.rplugins as yplug

from racy.renv             import constants
from racy.renv.options     import get_option
from racy.rproject.project import ConstructibleRacyProject, \
                                  InstallableRacyProject
from racy.rutils           import memoize, remove_vcs_dirs

all = ['RacyProjectsDB']

@memoize
def find_files(root, dir, filename):
    """Find recursively 'filename' in 'root' and returns a list
    with paths of found files if these files are in a directory 'dir'.
    Ignore VCS dirs.
    The 'dir' is filtered to minimize the number of directories walked.
    """

    path_list = []
    walker = os.walk(root, followlinks=True)
    for root, dirs, files in walker:
        remove_vcs_dirs(dirs)

        #if dir containt 'dir', don't walk others
        if dir in dirs: dirs[:] = [dir]

        if root.endswith(os.path.sep + dir):
            if filename in files:
                path_list.append(os.path.join(root, filename))
                dirs[:] = []

    return path_list


@memoize
def find_files_in_dirs(directory_list, filename):
    """Specialized version of find_files, lookup in multiple directories and
    filter dirs with constants.PRJ_OPT_DIR"""
    path_list = []

    for directory in directory_list :
        path_list += find_files(
                directory, 
                constants.PRJ_OPT_DIR, 
                filename
                )

    return path_list




class RacyProjectsDB(object):
    """Build a map of all build options in a directory list"""

    def __init__(self, directory_list=[], env={}, 
            prj_file=constants.OPTS_FILE ):

        from collections import defaultdict
        self.prj_args     = {}
        self.deps_db      = defaultdict(dict)
        self.src_lib_deps = {}
        self.bin_lib_deps = {}
        self.installed_libext = []
        self._prj_map     = {}
        self._prj_aliases = {}

        cc_version = env['TOOLINFO']['VERSION'].replace('.','-')
        cxx        = env['TOOLINFO']['NAME'] + cc_version

        self.prj_args['platform']    = get_option('PLATFORM')
        self.prj_args['debug']       = get_option('DEBUG')
        self.prj_args['env']         = env
        self.prj_args['cxx']         = cxx
        self.prj_args['projects_db'] = self

        if not directory_list:
            directory_list = racy.renv.dirs.code
        self.prj_path_list = find_files_in_dirs(directory_list, prj_file)

        for f in self.prj_path_list:
            self._register_prj_from_file(f)


    def __iter__(self):
        return self._prj_map.__iter__()

    def __getitem__(self, item):
        res = None

        name = getattr(item, 'register_name', item)
        name = self._prj_aliases.get(name, name)
        res = self._prj_map[name]

        return res

    def has_key(self, key):
        return self._prj_map.has_key(key)

    def __len__(self):
        return self._prj_map.__len__()


    def get_additive_projects(self, prj):
        res = []
        for dep in (prj,) + prj.source_rec_deps:
            res += yplug.register.get_additive_projects(dep)

        return res

    def _register_prj(self, prj):
        if prj.register_name in self._prj_map:
            prev_prj = self._prj_map[prj.register_name]
            msg = """An existing project is already called <{0.register_name}>.
                  defined here   : {1.project_dir}
                  redefined here : {0.project_dir}
                  """.format(prj, prev_prj)
            racy.print_warning( 'Project {0.full_name}'.format(prj), msg)

        self._prj_map[prj.register_name] = prj

        if prj.name != prj.register_name:
            self._prj_aliases[prj.name] = prj.register_name



    @memoize
    def _make_prj_from_file(self, file, args = {},
            factory = ConstructibleRacyProject):
        kwargs = {}
        kwargs.update(self.prj_args)
        kwargs.update(args)

        prj = factory(file, **kwargs)

        return prj

    def _register_prj_from_file(self, file):
        name = file.split(os.sep)[-3]

        target = racy.renv.TARGETS.get(name)
        
        args = {}
        for el in target.args:
            if el.startswith("@") :
                args['config'] = config = el[1:]

        if args.get('config'):
            target.name = '_'.join([target.name, config])

        prj = self._make_prj_from_file(file, args)

        self._register_prj(prj)

    def target_lookup(self, name, **kw):

        try:
            target = racy.renv.TARGETS.get(name)

            db = self
            if target.name and db.has_key(target.name):
                print 'Target : ' + name # XXX
                rlog.info.log("Target", name)
                prj      = db[target.name]
                
                to_build = [prj]
                to_build += db.get_additive_projects(prj)
                res = []
                for p in to_build:
                    builddeps = racy.rutils.is_true(p.get('BUILDDEPS'))
                    buildpkg  = racy.rutils.is_true(p.get('BUILDPKG'))
                    opts = ['rc']
                    opts += ['deps'] if builddeps else []
                    opts += ['pkg'] if buildpkg else []
                    res += p.install(opts = opts) 

                for libext in racy.rlibext.register.configured.values():
                    if hasattr(libext, '__src__'):
                        buildoptions = os.path.join(libext.__src__,
                            'bin','build.options')
                        if os.path.exists(buildoptions):
                            libextprj = self._make_prj_from_file(buildoptions,
                                    factory=InstallableRacyProject)
                            if libextprj.name not in self.installed_libext:
                                res += libextprj.install(['bin','rc'])
                                self.installed_libext.append(libextprj.name)

                            
                pack = []
                #pack = prj.env.Package(
                        ##source=res,
                        #target="/tmp/"+prj.full_name+".zip",
                        #PACKAGETYPE='zip',
                        #NAME=prj.name,
                        #VERSION=prj.version,
                        #LICENCE='bsd',
                        #DESCRIPTION='fwCore lib',
                        #SUMMARY='f4s basics',
                        #VENDOR='IRCAD',
                        #X_MSI_LANGUAGE = 'En',
                        #)

                res = prj.env.Alias(prj.full_name, res+pack)

                return res[0]
            elif target.name:
                msg = 'Unknown target : {trg.name}'.format(trg = target)
                racy.print_warning('Unknown target', msg)

        except racy.RacyException, e:
            racy.manage_exception(e)
            exit(1)


# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import os

from os.path import join as pathjoin, abspath, normpath


import racy
import racy.renv          as renv
import racy.rlibext       as rlibext
import racy.rutils        as rutils

from racy import ConfigVariantError,\
                 LibBadVersion,\
                 LibMissingVersion,\
                 NotUsed,\
                 RacyProjectError\

from racy.renv.configs import get_config, allowedvalues
from racy.renv         import constants
from racy.rutils       import cached_property, memoize, run_once


def abspath_key(r): 
    return r.get_abspath()

all = ['LibName', 'RacyProject', 'ConstructibleRacyProject']


LIBEXT    = ('libext', )
STATIC    = ('static', )
SHARED    = ('shared', )
BUNDLE    = ('bundle', )
EXEC      = ('exec'  , )
LIB       = SHARED + STATIC

BINLIBEXT = ('bin_libext', )
BINSTATIC = ('bin_static', )
BINSHARED = ('bin_shared', )
BINBUNDLE = ('bin_bundle', )
BINEXEC   = ('bin_exec'  , )
BINLIB    = BINSHARED + BINSTATIC

TYPE_ALL       = LIBEXT + STATIC + LIB + EXEC
TYPE_ALLBIN    = BINLIBEXT + BINSTATIC + BINLIB + BINEXEC
TYPE_ALLBUNDLE = BUNDLE + BINBUNDLE
TYPE_ALLSTATIC = STATIC + BINSTATIC
TYPE_ALLSHARED = SHARED + BINSHARED
TYPE_ALLEXEC   = EXEC   + BINEXEC
TYPE_ALLLIB    = LIB    + BINLIB
TYPE_ALLLIBEXT = LIBEXT + BINLIBEXT
#------------------------------------------------------------------------------

@racy.no_undef_attr_read
@racy.no_undef_attr_write
class LibName(str):
    """ Analyse the string representing the lib's name to extract wanted
    informations (name, version, ...)
    lib's name string format = name_version_config_etc
    """
    SEP = constants.LIBNAME_SEP

    @cached_property
    def _splited(self):
        return self.split(LibName.SEP)


    @cached_property
    def name(self):
        """Returns the lib's name'"""
        return self._splited[0]


    @cached_property
    def version(self):
        """Returns the lib's version, 0-0 if none specified."""
        s = self._splited
        if len(s) == 1:
            return ''
        return rutils.Version(s[1])

    @cached_property
    def config(self):
        """Returns the lib's name'"""
        s = self._splited
        if len(s) <= 2:
            return ''
        return s[2]

    @cached_property
    def register_name(self):
        """Returns the lib name used to register it in project database
        Ex: fwData_config, fwDataIO.
        """
        items = [el for el in [self.name] if el]
        return LibName.SEP.join(items)

    def check(self):
        """Returns True if lib name defines at least name and version"""
        s = self._splited
        return len(s) > 1

#------------------------------------------------------------------------------

@racy.no_undef_attr_read
@racy.no_undef_attr_write
class RacyProject(object):
    """Represents a racy project, read the options and provide some usefull
    methods to get project informations."""

    _compiler      = None
    _config        = None
    _debug         = None
    _opts_source   = None
    _platform      = None
    _project_dir   = None

    prj_def_vars   = None
    prj_locals     = None
    projects_db    = None
    special_source = None
    special_target = None

    base_name      = None

    def __init__(self, build_options, prj_path=None,
            platform='', cxx='', debug='',
            config = None,
            projects_db = {}, **kw):

        build_options_is_dict = isinstance(build_options, dict)

        if not build_options_is_dict and os.path.isfile(build_options):
            build_options = abspath(normpath(build_options))
            build_options_dir = os.path.dirname(build_options)
            if prj_path is None:
                prj_path = pathjoin(build_options, '..', '..')
                prj_path = abspath(normpath(prj_path))
        else :
            error = []
            if not build_options_is_dict:
                error.append('build_options:"{0}" is neither a file nor a '
                        'dictionnary.'.format(build_options))
            if prj_path is None:
                error.append('"prj_path" must be specified if "build_options" '
                             'is not a file.')
            if error:
                raise RacyProjectError( self, ' '.join(error) )

            build_options_dir = pathjoin(prj_path,'bin')


        config_dir  = pathjoin(build_options_dir,'configs')
        self._opts_source = build_options
        self._project_dir = prj_path

        self.prj_def_vars = {}
        self.prj_locals = kw.get('_locals' ,{})
        _globals        = kw.get('_globals',{})
        if self.prj_locals is None:
            self.prj_locals = {}


        if build_options_is_dict:
            self.prj_locals.update(build_options)
            self.prj_def_vars.update(build_options)
        else:
            get_config(os.path.basename(build_options),
                    path     = build_options_dir,
                    _locals  = self.prj_locals,
                    _globals = _globals,
                    defs     = self.prj_def_vars,
                    )

        # Check if one project config matches the global specified CONFIG
        # if a specific config has not been specified
        if not config:
            global_config = renv.options.get_option( "CONFIG" )
            has_global_config = os.path.exists(
                    pathjoin(config_dir, global_config))
            if has_global_config:
                config = global_config

        if config:
            config_locals = get_config(config,
                        path          = config_dir,
                        _locals       = self.prj_locals,
                        _globals      = _globals,
                        write_postfix = True,
                        read_default  = False,
                        defs          = self.prj_def_vars,
                        )

        self._platform  = platform
        self._compiler  = rutils.Version(cxx)
        self._debug     = debug
        self._config    = config

        self.base_name = self.prj_locals.get('NAME')
        if not self.base_name:
            self.base_name = os.path.basename(prj_path)


        self.projects_db    = projects_db
        self.special_source = []
        self.special_target = []


    def __repr__(self):
        return '{0.__class__.__name__} for {0.full_name}'.format(self)

    def __str__(self):
        return LibName(self.full_name)
    

    def get(self, opt):
        """Get the value V of opt in the prj's options dictionnary, check if V
        matches allowed value (if defined) and get the final value with
        get_option : if V was None, V is at least replaced by a default value,
        else V may be replaced by a highest priority value (like command-line
        defined value). see renv/options"""
        kwargs = {}

        name = self.base_name
        kwargs['opt']          = opt
        kwargs['prj']          = self
        kwargs['option_value'] = self.prj_def_vars.get(opt, None)
        config = (self.config if self.config else "default")
        config = ''.join([name, ':', config])
        
        if opt in self.prj_def_vars:
            allowedvalues.check_value_with_msg(
                    opt,
                    kwargs['option_value'],
                    config + " " + str(kwargs['prj'].opts_source)
                    )
        res = renv.options.get_option( **kwargs )
        return res


    def get_lower(self, opt):
        """Get option value in lower_case (must be a string option)."""
        return self.get(opt).lower()
    

    def get_path(self, path = ""):
        """Return base path of project."""
        path = pathjoin(self._project_dir, path)
        return abspath(normpath(path))


    @property
    def platform (self):
        return self._platform


    @property
    def compiler (self):
        return self._compiler


    @property
    def debug (self):
        return self._debug

    @property
    def is_debug (self):
        return self.debug != 'release'

    @property
    def config (self):
        return self._config

    @property
    def vc_dir (self):
        """Return directory of vc resrc file"""
        return pathjoin(self.bin_path, 'vc')

    @property
    def root_path (self):
        """Return path of project"""
        return self._project_dir

    @property
    def opts_source (self):
        """Return path of options file"""
        return self._opts_source


    @cached_property
    def src_dirs (self):
        return [constants.SOURCE_PATH] + self.get('PRJ_SOURCES')

    @cached_property
    def src_path (self):
        return map(self.get_path, self.src_dirs)

    @cached_property
    def include_dirs (self):
        return [constants.INCLUDE_PATH] + self.get('PRJ_INCLUDES')

    @cached_property
    def include_path (self):
        return map(self.get_path, self.include_dirs)


    @cached_property
    def bin_path (self):
        return self.get_path(constants.BIN_PATH)

    @cached_property
    def lib_path (self):
        return self.get_path(constants.LIB_PATH)

    @cached_property
    def rc_path (self):
        return self.get_path(constants.RC_PATH)


    @cached_property
    def cpp_path (self):
        return [self.get_path(p) for p in [constants.INCLUDE_PATH,'interface'] 
                if os.path.isdir(self.get_path(p))]


    @cached_property
    def prefix (self):
        prefix = LibName.SEP.join(self.get('PREFIX'))
        return prefix
    

    @cached_property
    def postfix (self):
        postfix = LibName.SEP.join(self.get('POSTFIX'))
        return postfix


    @cached_property
    def full_postfix(self):
        """Returns full postfix in the form : 
        version_platform_arch_compiler_prjpostfix_console_debug
        """
        compiler    = self.compiler
        platform    = self.platform
        arch        = renv.options.get_option('ARCH')
        prj_postfix = self.postfix
        console     = ''
        debug       = ''

        if self.is_console : console = 'C'
        if self.debug != 'release': debug = 'D'

        postfix_list = [platform, arch, compiler, prj_postfix, console, debug]
        while '' in postfix_list: postfix_list.remove('')

        return LibName.SEP.join(postfix_list)


    @cached_property
    def noprefix_full_name(self):
        """Returns final name without prefix in the form : 
        name_version_platform_arch_compiler_prjpostfix_console_debug
        """
        versioned_name = self.versioned_name
        full_postfix   = self.full_postfix

        full_list = [versioned_name, full_postfix]
        while '' in full_list: full_list.remove('')

        full_name = LibName.SEP.join(full_list)
        return full_name

    @cached_property
    def full_name(self):
        """Returns final name in the form : 
        prjprefix_name_version_platform_arch_compiler_prjpostfix_console_debug
        """
        prj_prefix     = self.prefix

        full_list = [prj_prefix, self.noprefix_full_name]
        while '' in full_list: full_list.remove('')

        full_name = LibName.SEP.join(full_list)
        return full_name

    

    @cached_property
    def version (self):
        return rutils.Version(self.get('VERSION'))


    @cached_property
    def name (self):
        return self.base_name

    @cached_property
    def desc(self):
        """Returns a description string of the project"""
        return "<{prj.name}> [{prj._opts_source}]".format(prj = self)
    

    @cached_property
    def versioned_name (self):
        """Returns the versioned project name 
        Ex: fwData_0-1
        """
        return LibName.SEP.join([self.name, self.version.normalized])


    @cached_property
    def name_version_config (self):
        """Returns the versioned project name with the configuration 
        Ex: fwData_0-1_config.
        """
        items = [el for el in 
                [self.name, self.version.normalized, self.config] if el]
        return LibName.SEP.join(items)


    @cached_property
    def register_name (self):
        return LibName(self.name_version_config).register_name


    @cached_property
    def type (self):
        type = self.get_lower('TYPE')
        if type not in allowedvalues.TYPE:
            raise RacyProjectError( self, 'TYPE must be defined.')
        return type


    @property
    def is_exec (self):
        return self.type == 'exec'

    @property
    def is_shared (self):
        return self.type == 'shared'

    @property
    def is_static (self):
        return self.type == 'static'

    @property
    def is_lib (self):
        return self.is_shared or self.is_static

    @property
    def is_bundle (self):
        return self.type == 'bundle'


    @property
    def is_bin_shared (self):
        return self.type == 'bin_shared'


    @property
    def is_bin_bundle (self):
        return self.type == 'bin_bundle'


    @property
    def is_bin_exec (self):
        return self.type == 'bin_exec'


    @property
    def is_bin_libext (self):
        return self.type == 'bin_libext'

    @property
    def is_bin_lib (self):
        return self.is_bin_shared

    @property
    def is_bin (self):
        return any( [ 
            self.is_bin_shared,
            self.is_bin_lib,
            self.is_bin_libext,
            self.is_bin_exec,
            self.is_bin_bundle,
            ])

    @cached_property
    def is_console (self):
        return rutils.is_true(self.get_lower('CONSOLE'))


    def _get_libnames(self, value):
        libnames = tuple(LibName(val.strip()) for val in self.get(value))

        db = self.projects_db
        miss = [el for el in libnames if not db.has_key(el.register_name)]

        miss = [el for el in miss if not rlibext.register.is_available(el)]

        if miss :
            raise RacyProjectError(self,
                    ('Missing <' + ', '.join(miss) + '>. '
                     'Required by {prj.desc}')
                    )

        # uncomment to check missing version in bundles and libs
#        missing_versions = tuple(lib for lib in libnames if not lib.check())
#        if missing_versions:
#            raise LibMissingVersion(missing_versions, self)

        return libnames


    @cached_property
    def libs(self):
        """Returns libs names that project depends on. Libs version presence
        is checked, version *must* be determined.
        """
        libnames = self._get_libnames('LIB')

        # ------- lib missing version checked only for lib actually : ---XXX
        missing_versions = tuple(lib for lib in libnames if not lib.check())
        if missing_versions:
            raise LibMissingVersion(missing_versions, self)
        # ---------------------------------------------------------------XXX
        return libnames

    @cached_property
    def bundles(self):
        """Returns bundles that project depends on"""
        return self._get_libnames('BUNDLES')


    @cached_property
    def uses(self):
        """Returns external libs that project depends on"""
        return tuple(LibName(use.strip()) for use in self.get('USE'))


    def _get_deps(self, item, src_projects, check_versions=True):
        db = self.projects_db
        items = getattr(self,item)
        try:
            if check_versions and src_projects:
                def check_vers(dep):
                    try:
                        name = dep.register_name
                        registered = name in db
                        return registered and not db[name].version==dep.version
                    except KeyError:
                        raise RacyProjectError(self,
                            ''.join(['Missing <' , dep.register_name , '>. '
                                        'Required by {prj.desc}'])
                                        )

                bad_versions = tuple(dep for dep in items if check_vers(dep))
                if bad_versions:
                    raise LibBadVersion(bad_versions, self)


            if src_projects:
                def is_src_project(dep):
                    name = dep.register_name
                    return name in db and not db[dep.register_name].is_bin

                validator = is_src_project
            else:
                def is_bin_prj(dep):
                    name = dep.register_name
                    if name not in db:
                        #this will register name to db
                        libext = rlibext.register.get_lib_for_prj(name, self)
                    return db[name].is_bin

                validator = is_bin_prj


            deps = tuple( db[dep.register_name]
                            for dep in items if validator(dep) )

            return deps

        except ConfigVariantError, e: # could be raised by db[lib]
            raise RacyProjectError( self, 
                    str(e) + " Required by {prj.desc}"
                    )

    @cached_property
    def source_libs_deps(self):
        """Returns libs provided as sources that project depends on.
        """
        return self._get_deps('libs', src_projects = True)



    @cached_property
    def source_bundles_deps(self):
        """Returns bundles provided as sources that project depends on.
        """
        return self._get_deps('bundles', src_projects = True,
                                check_versions=False)

    @cached_property
    def source_deps(self):
        """Returns deps provided as sources that project depends on.
        """
        return self.source_libs_deps + self.source_bundles_deps




    @cached_property
    def bin_libs_deps(self):
        """Returns libs provided as binary packages that project depends on.
        """
        return self._get_deps('libs', src_projects = False)

    @cached_property
    def bin_bundles_deps(self):
        """Returns bundles provided as binary packages that project depends on.
        """
        return self._get_deps('bundles', src_projects = False,
                                check_versions=False)

    @cached_property
    def bin_uses_deps(self):
        """Returns bundles provided as binary packages that project depends on.
        """
        return self._get_deps('uses', src_projects = False,
                                check_versions=False)

    @cached_property
    def bin_deps(self):
        """Returns deps provided as binary packages that project depends on.
        """
        return self.bin_libs_deps + self.bin_bundles_deps + self.bin_uses_deps


    def _get_rec_deps(self, callers, attribs = ['source_deps']):
        """Returns recursive dependencies (libs + bundles). Usefull to get all
        include path for example.
        """
        if self in callers:
            cycle = [prj.name for prj in callers[callers.index(self):]]
            msg = " -> ".join(cycle + [self.name])
            raise RacyProjectError(self,
                    ('Cyclic dependency on {prj.name}: ' + msg )
                    )
        db = self.projects_db

        dbdeps = db.deps_db[tuple(sorted(attribs))]

        deps = dbdeps.get(self)
        callers.append(self)
        if not deps:
            deps = sum([list(getattr(self,attr)) for attr in attribs],[])
            for lib in self.source_deps:
                deps += lib._get_rec_deps(callers, attribs)
            deps = tuple(sorted(set(deps), key=str))
            dbdeps[self] = deps
        callers.remove(self)
        return deps


    @cached_property
    def source_rec_deps(self):
        """Returns recursive source dependencies (libs + bundles). Usefull to
        get all include path for example.
        """
        return self._get_rec_deps([])

    @cached_property
    def lib_rec_deps(self):
        """Returns recursive source dependencies (libs + bundles). Usefull to
        get all include path for example.
        """
        return self._get_rec_deps([], attribs = ['source_libs_deps'])


    @cached_property
    def bin_rec_deps(self):
        """Returns recursive binary dependencies (libs + bundles). Usefull to
        get all include path for example.
        """
        return self._get_rec_deps([], attribs = ['bin_deps'])


    @cached_property
    def rec_deps(self):
        return self.source_rec_deps + self.bin_rec_deps



    @cached_property
    def deps_include_path (self):
        """Returns include paths for all dependencies using source_rec_deps."""
        inc = [lib.include_path for lib in self.source_rec_deps]
        if len(inc)>1:
            inc = reduce( lambda a,b : a+b, inc)
        elif len(inc) == 1:
            inc = inc[0]
        return inc


    @cached_property
    def loglevel (self):
        return self.get('LOGLEVEL')


    @cached_property
    def n_loglevel (self):
        """Returns the numeric value of loglevel."""
        return constants.LOGLEVEL[self.loglevel]

    @cached_property
    def extra_sources_build_dirs(self):
        dirs = set(map(os.path.dirname, self.get('PRJ_SOURCES_FILES')))
        builddirs = map( self.get_build_dir_for , dirs )
        dirs      = map( self.get_path , dirs )
        return zip(builddirs, dirs)

    @cached_property
    def extra_sources(self):
        return map(self.get_build_dir_for, self.get('PRJ_SOURCES_FILES'))

    @cached_property
    def sources_build_dirs(self):
        dirs = set(self.src_dirs)
        builddirs = map( self.get_build_dir_for , dirs )
        dirs      = map( self.get_path , dirs )
        return zip(builddirs, dirs)


    @cached_property
    def sources(self):
        """Returns CXX source files of the project"""
        build_dirs = map(self.get_build_dir_for, self.src_path)

        sources = rutils.DeepGlob(
                constants.CXX_SOURCE_EXT,
                self.src_path,
                build_dirs
                ) + self.extra_sources + self.special_source
        return sources


    @cached_property
    def build_dir(self):
        return pathjoin(renv.dirs.build, self.full_name)


    def get_build_dir_for(self, file):
        prj_path = self.get_path()
        if file.startswith(prj_path):
            file = file[len(prj_path)+1:]
        return pathjoin( self.build_dir , file )

    @cached_property
    def target(self):
        return pathjoin(self.build_dir, self.full_name)


    @cached_property
    def install_rc_path(self):
        if self.type in TYPE_ALLEXEC + TYPE_ALLLIB + BINLIBEXT:
            install_dir = renv.dirs.install_share
        elif self.type in TYPE_ALLBUNDLE:
            install_dir = renv.dirs.install_bundle
        else:
            raise RacyProjectError ( self,
               'project TYPE installation not managed right now ({prj.type})')

        install_dir = pathjoin(install_dir, self.versioned_name)

        return install_dir


    @cached_property
    def install_path(self):
        if self.type in TYPE_ALLEXEC:
            install_dir = renv.dirs.install_bin
        elif self.type in TYPE_ALLLIB + BINLIBEXT:
            if racy.renv.system() == "windows":
                install_dir = renv.dirs.install_bin
            else:
                install_dir = renv.dirs.install_lib
        elif self.type in TYPE_ALLBUNDLE:
            install_dir = pathjoin(renv.dirs.install_bundle,
                    self.versioned_name)
        else:
            raise RacyProjectError ( self,
                'Unable to install, unknown project TYPE ({prj.type})')

        return install_dir


    @cached_property
    def install_pkg_path(self):
        if self.type in TYPE_ALLEXEC + TYPE_ALLLIB + BINLIBEXT:
            install_dir = renv.dirs.install_binpkg
        else:
            raise RacyProjectError ( self,
                    'Binary packaging not managed for this type: ({prj.type})')

        install_dir = pathjoin(install_dir, self.full_name)

        return install_dir
    

class InstallableRacyProject(RacyProject):

    env = None

    def __init__(self, build_options, env, **kwargs):
        self.env = env.Clone()
        super(InstallableRacyProject,self).__init__(
                build_options = build_options, 
                **kwargs
                )

    @memoize
    def install_files (self, src_path, dst_path, ext):
        """Create the installation targets for specified files."""
        prj = self
        env = self.env

        result = []
        if os.path.isdir(src_path):
            sources_files, install_files = rutils.DeepGlob(
                                            extensions  = ext,
                                            src_dir     = src_path,
                                            replace_dir = dst_path,
                                            return_orig = True
                                            )
            def rmbo(L):
                return [abspath(el) 
                        for el in L if 'build.options' not in el]
            sources_files = rmbo(sources_files)
            install_files = rmbo(install_files)
            result = env.CopyFile( install_files, source = sources_files )
            for node in result:
                env.Clean(node, node)

        return result

    @memoize
    def install_bin_shared (self):
        return self.install_files(self.lib_path, self.install_path, ['.*'])

    @memoize
    def install_bin_libext (self):
        env = self.env
        import fnmatch
        libext = self.get('LIBEXTINSTANCE')

        patterns = []
        if racy.renv.system() == "windows":
            patterns.append( env.subst('${SHLIBPREFIX}{0}${SHLIBSUFFIX}'))
            patterns.append( '{0}.pdb*' )
            patterns.append( env.subst('{0}${WINDOWSSHLIBMANIFESTSUFFIX}*') )
        elif racy.renv.system() == "darwin":
            patterns.append( env.subst('${SHLIBPREFIX}{0}${SHLIBSUFFIX}'))
            patterns.append( env.subst('${SHLIBPREFIX}{0}.*${SHLIBSUFFIX}'))
        else:
            patterns.append( env.subst('${SHLIBPREFIX}{0}${SHLIBSUFFIX}*'))


        matches = []
        for pattern in patterns:
            for lib in libext.LIBS:
                matches.append( fnmatch.translate(pattern.format(lib)) )

        for pattern in libext.libs_install:
            matches.append( fnmatch.translate(pattern) )

        regex = '|'.join(matches)

        res = []
        if regex:
            for path in libext.ABS_LIBPATH:
                res += self.install_files(path, self.install_path, regex)

        res = self.env.Alias('install_bin_libext-' + self.full_name, res)
        return res

    @memoize
    def install_bin_bundle (self):
        return self.install_files(self.lib_path, self.install_path, ['.*'])


    @memoize
    def install_bin_exec(self):
        return self.install_files(self.bin_path, self.install_path, [])


    @memoize
    def install_pkg(self):
        """Create the installation targets for project's binary package and 
        return them.
        """
        pkg_path = self.install_pkg_path

        def get_include_path_target(path):
            return pathjoin( pkg_path , os.path.split(path)[1] )

        rc  = pathjoin(pkg_path, constants.RC_PATH)
        inc = map(get_include_path_target, self.include_path)

        install_args = [ (self.rc_path     , rc , ['.*']) ]
        for incpth, replace in zip(self.include_path, inc):
            install_args.append((incpth, replace, constants.CXX_HEADER_EXT))

        res = []
        for args in install_args:
            res += self.install_files(*args)

        return res


    @memoize
    def install_rc(self):
        """Create the installation targets for project's ressources and return
        them.
        """
        return self.install_files(self.rc_path, self.install_rc_path, ['.*'])


    @memoize
    def install(self, opts = ['rc']):
        env = self.env
        result = []
        if 'rc' in opts:
            result += self.install_rc()

        if ('bin' in opts and self.type in TYPE_ALLBIN):
            func = ''.join(['install_', self.type])
            result += getattr(self,func)()

        if 'pkg' in opts and self.type not in TYPE_ALLBIN:
            result += self.install_pkg()

        bin_deps = 'bin' in opts and 'deps' in opts
        if bin_deps:
            bin_results = []
            for dep in self.bin_rec_deps:
                bin_results.append( dep.install(opts) )
            bin_results.sort()

        result.sort(key=abspath_key)
        result = env.Alias ('install-' + self.full_name, result)

        if bin_deps:
            env.Depends(result, bin_results)

        return result


class ConstructibleRacyProject(InstallableRacyProject):
    
    @memoize
    def exports(self, export=False):
        env = self.env
        api_export       = '{0}_API'.format(self.name.upper())
        class_api_export = '{0}_CLASS_API'.format(self.name.upper())
        templ_api_export = '{0}_TEMPLATE_API'.format(self.name.upper())


        if self.get('USEVISIBILITY') == "racy":
            exp = 'EXPORT' if export else 'IMPORT'
            exports_defs = [
                    (api_export,       "_API_"+exp      ),
                    (class_api_export, "_CLASS_API_"+exp),
                    (templ_api_export, "_TEMPL_API_"+exp),
                    ]
        else:
            exports_defs = [
                    (api_export       , "\/\*\*\/"),
                    (class_api_export , "\/\*\*\/"),
                    (templ_api_export , "\/\*\*\/"),
                    ]

        return exports_defs


    @cached_property
    def options (self):
        """Returns a dictionnary with project build options."""
        prj = self

#        import pipes
        prj_version = r'\"{0.version}\"'.format(prj)
        #prj_version = '"{0.version}"'.format(prj)
        #if self.env.get('CC') != "cl":
        #    prj_version = pipes.quote(prj_version)
        
        CPPDEFINES = [
                ['SPYLOG_LEVEL', prj.n_loglevel],
                [prj.name.upper()+'_VER', prj_version ],
                ['PRJ_NAME', r'\"{0}\"'.format(self.name) ],
                ] 
        CPPDEFINES += prj.get('DEF')

        
        CPPPATH  = []
        CPPPATH += prj.include_path
        CPPPATH += prj.deps_include_path
        CPPPATH += prj.get('INC')
        
        LIBPATH  = []
        LIBPATH += prj.get('STDLIBPATH')

        need_rec_deps = self.is_exec or racy.renv.system() in ['windows','darwin']
        lib_dep = prj.lib_rec_deps if need_rec_deps else prj.source_libs_deps

        LIBPATH += [ self.env.Dir(lib.build_dir) for lib in lib_dep]
        LIBS = [ lib.full_name for lib in lib_dep ]

        if renv.system() != 'linux':
            LIBPATH += [ lib.build_dir for lib in prj.source_bundles_deps ]
            LIBS    += [ lib.full_name for lib in prj.source_bundles_deps ]

        LIBS += prj.get('STDLIB')
        
        CFLAGS   = []
        CFLAGS  += prj.get('CFLAGS')
                   
        CXXFLAGS   = []
        CXXFLAGS  += prj.get('CXXFLAGS')
                   
        LINKFLAGS  = []
        LINKFLAGS += prj.get('LINKFLAGS')

        if not prj.is_exec:
            if self.get('USEVISIBILITY') in ["no", "racy"]:
                deps = prj.source_libs_deps + prj.source_bundles_deps

                # XXX Racy visibility transition ###########################
                CPPDEFINES += ['_{0}_CONFIG_HPP_'.format(dep.name.upper()) #
                                for dep in (self,) + deps]                 #
                ############################################################

                exports = self.exports(True)
                for dep in deps:
                    exports += dep.exports(False)
                CPPDEFINES += exports
            else:
                CPPDEFINES += [ prj.name.upper() + '_EXPORTS' ]
        

        names = [
                'CPPDEFINES', 'CPPPATH' ,
                'LIBPATH'   , 'LIBS'    ,
                'CFLAGS'    , 'CXXFLAGS',
                'LINKFLAGS' ,
                ]

        attrs = [locals()[n] for n in names]
        options = dict(zip(names,attrs))
        
        return options


    def manage_options(self, opts):
        """Delegate management of options specified in opts to rtool."""
        opts = rutils.iterize(opts)

        prj = self
        options = {}

        for opt in opts:
            val = prj.get(opt)
            options[opt] = val

        # ManageOption has been added by the current rtool
        self.env.ManageOption(prj = self, options = options)


    def variant_dir(self, build_dir, src_dir):
        self.env.VariantDir(build_dir, src_dir, duplicate=0)


    @run_once
    def configure_env(self):
        """Configure the SCons environment."""
        prj = self
        env = self.env

        for path, dir in zip(prj.src_path, prj.src_dirs):
            builddir = pathjoin( prj.build_dir , dir )
            self.variant_dir(builddir, path)

        builddirs  = []
        builddirs += prj.sources_build_dirs
        builddirs += prj.extra_sources_build_dirs
        for builddir, path in builddirs:
            self.variant_dir(builddir, path)

        direct_bin_deps = prj.bin_deps
        indirect_bin_deps = set(self.bin_rec_deps) - set(direct_bin_deps)
        indirect_bin_deps = sorted(indirect_bin_deps, key=str)

        link_opts = []
        if self.is_exec:
            link_opts += ['forcelink']

        rlibext.register.configure(prj, indirect_bin_deps, opts=['nolink'])
        rlibext.register.configure(prj, direct_bin_deps  , opts=link_opts)

        env.Prepend(**self.options)

        tool_level_options = [
                'WARNINGSASERRORS',
                'OPTIMIZATIONLEVEL',
                'NOLIB',
                'CONSOLE',
                'USEVISIBILITY',
                ]
        self.manage_options(tool_level_options)


    # This one *must* be memoized to avoid several build in env, otherwise
    # SCons will make a big noise and probably interrupt
    @memoize
    def result(self, deps_results=True):
        """Returns the SCons targets for this project.

        if deps_results is False, don't care about depencies existance
        """
        prj = self
        env = self.env


        if not deps_results:
            result = []
            self.configure_env()

            if prj.sources:
                if prj.is_exec:
                    result = env.Program(
                            target = prj.target,
                            source = prj.sources,
                            )
                elif prj.is_shared or prj.is_bundle:
                    result = env.SharedLibrary(
                            target = prj.target,
                            source = prj.sources,
                            )
                elif prj.is_static:
                    result = env.StaticLibrary(
                            target = prj.target,
                            source = prj.sources,
                            )
                else:
                    raise RacyProjectError( prj,
                        'Unknown project TYPE ({prj.type})')

            elif not prj.is_bundle:
                msg = ('Only bundles are allowed to be codeless. '
                        '<{prj.name}> type is "{prj.type}"')
                raise RacyProjectError( prj, msg)

        else:
            dep_results = []
            for dep in prj.source_libs_deps + prj.source_bundles_deps:
                dep_results.append( dep.build() )
            result = self.result(deps_results=False)

            if result:
                env.Depends(result, dep_results)
            else:
                # this may happends if we are in a codeless bundle
                for bun in prj.source_bundles_deps:
                    result += bun.build()

        return result + self.special_target


    def build (self, build_deps=True):
        """Returns the SCons targets for this project.

        if build_deps is False, don't care about depencies existance
        """

        result = self.result(deps_results = build_deps)
        #result.sort(key=abspath_key)
        #result = self.env.Alias ('build-' + self.full_name, result)
        return result




    @memoize
    def install (self, opts = ['deps','rc']):
        """Create the installation targets for project's results files and 
        return them.

        if rc in opts, install ressources
        if deps in opts, install dependencies
        """
        if not rutils.is_true(self.get('BUILD')):
            return []

        prj = self
        env = self.env

        build_results = prj.build(build_deps='deps' in opts)
        result = build_results

        if result and prj.sources:
            filter = env.InstallFileFilter
            to_install = [r for r in result if filter(r)]
            result = env.Install(dir = prj.install_path, source = to_install)
        else:
            result = []

        #ensure alias-like targets are build
        result += [r for r in build_results if not hasattr(r,"get_path")]

        result += super(ConstructibleRacyProject,self).install(opts)

        if 'deps' in opts:
            deps = prj.source_libs_deps + prj.source_bundles_deps
            deps_results = []
            deps_results += [dep.install(opts) for dep in deps]
            bin_results = []
            for dep in self.bin_deps:
                bin_results.append( dep.install(['bin','deps','rc']) )
            env.Depends(result, deps_results)
            env.Depends(result, bin_results)

        result.sort(key=abspath_key)
        alias = 'install-{prj.type}-{prj.full_name}'
        result = env.Alias (alias.format(prj=self), result)

        return result
        
    def generate_pkg_files(self):
        from string import Template
        env  = self.env
        prj  = self
        opts = prj.prj_locals

        arch = renv.options.get_option('ARCH')
        depends = list(self.uses + self.libs + self.bundles)
        depends = map(lambda obj:getattr(obj, 'name', obj), depends)
        CPPPATH = map(lambda x:[x], self.include_dirs)
        LIBPATH = [ ['lib'] ] + opts.get('STDLIBPATH')


        infos = {
                'REGISTER_NAMES' : [prj.name]            ,
                'VERSION'        : prj.version.normalized,
                'ISDEBUG'        : prj.is_debug          ,
                'ARCH'           : arch                  ,
                'PLATFORM'       : prj.platform          ,
                'COMPILER'       : prj.compiler          ,
                'DEPENDSON'      : depends               ,
                'CPPPATH'        : CPPPATH               ,
                'LIBPATH'        : LIBPATH               ,
                'LIBS'           : [prj.full_name]       ,
                'EXTRALIBS'      : opts.get('STDLIB')    ,
                'CPPDEFINES'     : opts.get('DEF')       ,
                'FRAMEWORKPATH'  : []                    ,
                'FRAMEWORK'      : []                    ,
                'CXXFLAGS'       : []                    ,
                'LINKFLAGS'      : []                    ,
                #'CXXFLAGS'       : opts.get('CXXFLAGS')  ,
                #'LINKFLAGS'      : opts.get('LINKFLAGS') ,
                }

        tpl_file = racy.ressources('binpkg.__init__.py.tpl')
        tpl = Template(rutils.get_file_content(tpl_file))
        infocontent = tpl.substitute(infos)

        pkg_path = self.install_pkg_path
        infofile = pathjoin(pkg_path, '__init__.py')

        res = []
        res += env.WriteFile(infofile, infocontent)

        return res


    @memoize
    def install_pkg(self):
        env = self.env
        res = super(ConstructibleRacyProject,self).install_pkg()
        alllibs = self.result(deps_results=False)

        libs = alllibs
        bins = alllibs

        if racy.renv.system() == "windows":
            libs = [ lib for lib in alllibs if lib.get_path().endswith('.lib')]
        bins = [lib for lib in alllibs if lib not in libs]

        pkg_path = self.install_pkg_path
        lib      = pathjoin(pkg_path, constants.LIB_PATH)
        bin      = pathjoin(pkg_path, constants.BIN_PATH)
        res     += env.Install(dir = lib, source = libs)
        res     += env.Install(dir = bin, source = bins)
        res     += self.generate_pkg_files()
        return res


    @cached_property
    def recursive_install_path(self):
        return [el.install_path for el in self.source_rec_deps]





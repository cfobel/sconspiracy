# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 

from os.path import join as opjoin

import racy

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once


class DoxygenError(racy.RacyProjectError):
    pass

DOXYGEN_PLUGIN_PATH = os.path.dirname(__file__)

class DoxygenProject(ConstructibleRacyProject):
    doxygen_dir    = 'Dox'

    var_name = 'DOX'

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = ('DoxygenProject take a '
                   'ConstructibleRacyProject as first argument')
            raise DoxygenError( self, msg )

        opt_file = prj.opts_path

        super(DoxygenProject, self).__init__(
                                        options_file = opt_file, 
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )


    @property
    def name (self):
        name = super(DoxygenProject, self).name
        return LibName.SEP.join( [self.doxygen_dir, name])

    @cached_property
    def dox_sources(self):
        sources = super(DoxygenProject, self).sources

#        headers = racy.rutils.DeepGlob(
#                constants.CXX_HEADER_EXT, 
#                self.include_path, 
#                self.build_dir
#                )
        headers = []

        return sources + headers

    @cached_property
    def doxyfile_path(self):
        return opjoin(DOXYGEN_PLUGIN_PATH, 'rc')

    @cached_property
    def doxyfile(self):
        return opjoin(self.doxyfile_path, 'Doxyfile')


    @run_once
    def configure_env(self):
        super(DoxygenProject, self).configure_env()

        env = self.env
        import SCons.Builder

        doxygen = env.WhereIs('doxygen', os.environ['PATH'])
        if not doxygen:
            msg = '"doxygen" command not found.'
            raise DoxygenError(self, msg)

        command = '"{dox}" "{doxyfile}"'
        command = command.format(dox=doxygen, doxyfile=self.doxyfile)

        def DoxygenEmitter(source, target, env):
            target.append(env.Dir(env['ENV']['DOX_OUTPUTDIR']))

            return (target, source)

        doxyfile_builder = SCons.Builder.Builder(
            action = command,
            target_factory = env.fs.Entry,
        )
        
        env.Append(BUILDERS = {
        'Doxygen': doxyfile_builder,
        })






    @memoize
    def result(self, deps_results=True):
        prj = self
        env = self.env

        result = []
        self.configure_env()

        dirs = []
        if prj.dox_sources:
            dirs = [self.src_path, self.include_path]
        if deps_results:
            for dep in prj.source_rec_deps:
                dirs += [dep.src_path, dep.include_path]

        env['ENV']['DOX_INCLUDES_PATH'] = " ".join(env['CPPPATH'])
        env['ENV']['DOX_PRJNAME']       = self.base_name
        env['ENV']['DOX_INPUTDIR']      = " ".join(dirs)
        env['ENV']['DOX_OUTPUTDIR']     = self.build_dir
#        print "#"*50
#        print 'DOX_INCLUDES_PATH', env['ENV']['DOX_INCLUDES_PATH']
#        print 'DOX_PRJNAME'      , env['ENV']['DOX_PRJNAME']      
#        print 'DOX_INPUTDIR'     , env['ENV']['DOX_INPUTDIR']     
#        print 'DOX_OUTPUTDIR'    , env['ENV']['DOX_OUTPUTDIR']    
#        print "#"*50

        sources = []
#        for dep in (prj,) + prj.source_rec_deps:
#            sources += racy.rutils.DeepGlob(
#                constants.CXX_SOURCE_EXT + constants.CXX_HEADER_EXT, 
#                os.path.abspath(dep.root_path),
#                os.path.abspath(dep.root_path)
#                )

        result = env.Doxygen( 
                    target = env['ENV']['DOX_OUTPUTDIR'],
                    source = sources,
                    )
#        env.Depends(result, sources)
        result = env.AlwaysBuild(result)

        for node in result:
            env.Clean(node, node)

        return result


    @cached_property
    def install_path(self):
        install_dir = racy.renv.dirs.install_doc
        return install_dir


    @memoize
    def install (self, opts = ['rc','deps']):
        prj = self
        env = self.env

        result = prj.build(build_deps='deps' in opts)

        if result:
            import shutil
            shutil.rmtree(env['ENV']['DOX_OUTPUTDIR'], ignore_errors=True)
            shutil.rmtree(opjoin(prj.install_path,prj.full_name), ignore_errors=True)
            result = env.Install(dir = prj.install_path, source = result)
            for node in result:
                env.Clean(node, node)
        else:
            result = []

        return result

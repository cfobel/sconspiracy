# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os
import SCons.Defaults
import SCons.Node

from os.path import join as opjoin
from hashlib import md5

import racy

from racy.renv       import constants
from racy.rproject   import ConstructibleRacyProject, LibName
from racy.rutils     import cached_property, memoize, run_once

import sconsbuilders
import sconsbuilders.url

from libexterror    import LibextError
from nodeholder     import NodeHolder
from builderwrapper import BuilderWrapper

class CommandWrapper(BuilderWrapper):

    def __init__(self, *args, **kwargs):
        kwargs['builder'] = self.builder
        super(CommandWrapper, self).__init__(*args, **kwargs)

    def builder_args(self, options, pwd, **kwargs):
        args = kwargs.setdefault('ARGS', [])
        args.extend(options)
        marker = '{dir}/{cmd}_{prj}_{hash}'
        marker = marker.format(
                dir  = '${BUILD_DIR}/',
                cmd  = self.builder_name,
                prj  = self.prj.full_name,
                hash = md5(' '.join(options)).hexdigest(),
                )
        kwargs.setdefault('target', [marker])
        kwargs.setdefault('source', [pwd])
        return kwargs

    def builder(self, options, pwd, **kwargs):
        kwargs = self.builder_args(options, pwd, **kwargs)
        scons_builder = getattr(self.prj.env, self.builder_name)
        return scons_builder(**kwargs)


class ConfigureWrapper(CommandWrapper):

    def __call__(self, *args, **kwargs):
        prj = self.prj
        ENV = prj.env['ENV']
        ENV['CXXFLAGS']  = ENV.get('CXXFLAGS','')
        ENV['CFLAGS']    = ENV.get('CFLAGS','')
        ENV['LINKFLAGS'] = ENV.get('LINKFLAGS','')
        ENV['CXXFLAGS']  += ' -I'.join([''] + prj.deps_include_path)
        ENV['CFLAGS']    += ' -I'.join([''] + prj.deps_include_path)
        ENV['LINKFLAGS'] += ' -L'.join([''] + prj.deps_lib_path)

        ARGS = kwargs.setdefault('ARGS', [])
        ARGS.append('--prefix=${BUILD_DIR}/local')

        super(ConfigureWrapper, self).__call__(*args, **kwargs)


class CMakeWrapper(CommandWrapper):
    def __call__(self, *args, **kwargs):
        ARGS = kwargs.setdefault('ARGS', [])
        ARGS.insert(0,'-DCMAKE_INCLUDE_PATH:PATH=$LIBEXT_INCLUDE_PATH')
        ARGS.insert(0,'-DCMAKE_LIBRARY_PATH:PATH=$LIBEXT_LIBRARY_PATH')
        ARGS.append('-DCMAKE_INSTALL_PREFIX:PATH=${BUILD_DIR}/local')

        if racy.renv.is_windows():
            ARGS.insert(0,'NMake Makefiles')
        else:
            ARGS.insert(0,'Unix Makefiles')
        ARGS.insert(0,'-G')

        super(CMakeWrapper, self).__call__(*args, **kwargs)

    def builder(self, options, source, builddir, **kwargs):
        kwargs = self.builder_args(options, pwd=source, **kwargs)
        kwargs['CMAKE_BUILD_PATH'] = builddir
        return self.prj.env.CMake(**kwargs)



class WaitDependenciesWrapper(BuilderWrapper):

    def __init__(self, *args, **kwargs):
        builder = self.wait_dependencies_builder
        kwargs['name'] = 'WaitDependencies'
        kwargs['builder'] = builder
        super(WaitDependenciesWrapper, self).__init__(*args, **kwargs)

    def wait_dependencies_builder(self, *args, **kwargs):
        """Return return a node dependent on libext's dependencies"""
        env = self.prj.env
        alias = env.Alias(str(self.prj)+ '_WaitDependencies')
        env.Depends(alias, self.prj.deps_nodes)
        return alias



class LibextProject(ConstructibleRacyProject):
    LIBEXT    = ('libext', )

    def __init__(self, *args, **kwargs):
        libext_builders = {}
        builder_wrappers = [
                BuilderWrapper(self,'Download'),
                BuilderWrapper(self,'UnTar'),
                BuilderWrapper(self,'Delete',self.DeleteBuilder),
                CMakeWrapper  (self,'CMake'),
                CommandWrapper(self,'Make'),
                CommandWrapper(self,'Patch'),
                CommandWrapper(self,'SysCommand', reg_name='Command'),
                ConfigureWrapper(self, 'Configure'),
                WaitDependenciesWrapper(self),
                ]

        for bld in builder_wrappers:
            bld.subscribe_to(libext_builders)

        kwargs['_globals']=kwargs.get('_globals',{})
        kwargs['_globals'].update(libext_builders)
        kwargs['_globals']['Url'] = sconsbuilders.url.Url

        super(LibextProject, self).__init__( *args, **kwargs )



    def DeleteBuilder(self, file, *args, **kwargs):
        env = self.env
        return env.Command(
                env.Value("Delete " + file),
                [],
                [SCons.Defaults.Delete(file, must_exist=1)],
                target_factory=env.Value,
                *args,
                **kwargs
                )

    @cached_property
    def download_target (self):
        path = [racy.renv.dirs.build, 'LibextDownload']
        fmt = "{0.name}_{0.version}"
        path.append(fmt.format(self))
        return os.path.join(*path)

    @cached_property
    def extract_dir (self):
        path = [self.build_dir, 'sources']
        return os.path.join(*path)

    @cached_property
    def local_dir (self):
        path = [self.build_dir, 'local']
        return os.path.join(*path)


    @cached_property
    def include_path (self):
        path = [self.local_dir, 'include']
        return os.path.join(*path)


    @cached_property
    def lib_path (self):
        path = [self.local_dir, 'lib']
        return os.path.join(*path)

    @cached_property
    def deps_include_path (self):
        inc = [lib.include_path for lib in self.source_rec_deps]
        return inc

    @cached_property
    def deps_lib_path (self):
        inc = [lib.lib_path for lib in self.source_rec_deps]
        return inc

    @cached_property
    def deps_nodes (self):
        inc = [lib.build() for lib in self.source_rec_deps]
        return inc

    @run_once
    def configure_env(self):
        super(LibextProject, self).configure_env()


    @memoize
    def result(self, deps_results=True):
        prj = self
        env = self.env

        result = []
        prj.configure_env()

        prj.prj_locals['generate']()

        download_target = env.Dir(prj.download_target)
        extract_dir = env.Dir(prj.extract_dir)

        previous = []
        res = BuilderWrapper.apply_calls(
                    prj,
                    DOWNLOAD_DIR        = download_target,
                    EXTRACT_DIR         = extract_dir    ,
                    BUILD_DIR           = prj.build_dir  ,
                    LOCAL_DIR           = prj.local_dir  ,
                    RC_DIR              = prj.rc_path    ,
                    NAME                = prj.name       ,
                    VERSION             = prj.version    ,
                    LIBEXT_INCLUDE_PATH = os.pathsep.join(prj.deps_include_path),
                    LIBEXT_LIBRARY_PATH = os.pathsep.join(prj.deps_lib_path),
                    SUBPROCESSPREFIXSTR = '[{0}]:'.format(self.name)
                    )

        for nodes in res:
            for node in nodes:
                #HACK: scons need a name attribute to manage dependencies
                if not hasattr(node, "name"):
                    node.name = ''
                env.Depends( node, previous )
                previous = node

        result += nodes

        for node in [extract_dir]:
            env.Clean(node, node)


        alias = 'result-{prj.type}-{prj.full_name}'
        result = env.Alias (alias.format(prj=self), result)
        env.Clean(result, env.Dir(self.build_dir + '/local'))
        return result


    def build(self,  build_deps = True):
        """build_deps = False is not available"""
        res = self.result()
        return res

    @memoize
    def install (self, opts = ['rc','deps']):
        prj = self
        env = self.env

        result = prj.build(build_deps='deps' in opts)

        #if result:
            #import shutil
            #shutil.rmtree(env['ENV']['DOX_OUTPUTDIR'], ignore_errors=True)
            #shutil.rmtree(opjoin(prj.install_path,prj.full_name), ignore_errors=True)
            #result = env.Install(dir = prj.install_path, source = result)
            #for node in result:
                #env.Clean(node, node)
        #else:
            #result = []

        return result

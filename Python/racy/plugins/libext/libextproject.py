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

def marker(command, prj, options):
    res = '{dir}/{cmd}_{prj}_{hash}'
    res = res.format(
            dir  = '${BUILD_DIR}/',
            cmd  = command,
            prj  = prj,
            hash = md5(' '.join(options)).hexdigest(),
            )
    return res

class CommandWrapper(BuilderWrapper):

    def __init__(self, *args, **kwargs):
        kwargs['builder'] = self.builder
        super(CommandWrapper, self).__init__(*args, **kwargs)

    def builder_args(self, options, pwd, **kwargs):
        args = kwargs.setdefault('ARGS', [])
        args.extend(options)
        target = marker(self.builder_name, self.prj.full_name, options)
        kwargs.setdefault('target', [target])
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
        ARGS.append('--prefix=${LOCAL_DIR}')

        if prj.get('DEBUG') != 'release':
            ARGS.append('--enable-debug')
        else:
            ARGS.append('--disable-debug')

        super(ConfigureWrapper, self).__call__(*args, **kwargs)


class CMakeWrapper(CommandWrapper):
    def __call__(self, *args, **kwargs):
        prj = self.prj

        ARGS = kwargs.setdefault('ARGS', [])
        ARGS.insert(0,'-DCMAKE_INCLUDE_PATH:PATH=${DEPS_INCLUDE}')
        ARGS.insert(0,'-DCMAKE_LIBRARY_PATH:PATH=${DEPS_LIB}')
        ARGS.append('-DCMAKE_INSTALL_PREFIX:PATH=${LOCAL_DIR}')

        def build_type():
            if prj.get('DEBUG') != 'release':
                return 'Debug'
            else:
                return 'Release'

        ARGS.append('-DCMAKE_BUILD_TYPE:STRING={0}'.format(build_type()))

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


class EditWrapper(CommandWrapper):

    def builder(self, expr, files, **kwargs):
        kwargs = self.builder_args(files + expr, pwd=[], **kwargs)
        return self.prj.env.Edit(FILES=files, EXPR=expr, **kwargs)




class WaitDependenciesWrapper(BuilderWrapper):

    def __init__(self, *args, **kwargs):
        builder = self.wait_dependencies_builder
        kwargs['name'] = 'WaitDependencies'
        kwargs['builder'] = builder
        super(WaitDependenciesWrapper, self).__init__(*args, **kwargs)

    def wait_dependencies_builder(self, *args, **kwargs):
        return self.prj



class LibextProject(ConstructibleRacyProject):
    LIBEXT    = ('libext', )

    def __init__(self, *args, **kwargs):
        libext_builders = {}
        builder_wrappers = [
                BuilderWrapper  (self,'Download'),
                BuilderWrapper  (self,'UnTar'),
                BuilderWrapper  (self,'UnZip'),
                BuilderWrapper  (self,'Delete',self.DeleteBuilder),
                BuilderWrapper  (self,'Copy'  ,self.CopyBuilder),
                BuilderWrapper  (self,'Mkdir' ,self.MkdirBuilder),
                CMakeWrapper    (self,'CMake'),
                EditWrapper     (self,'Edit'),
                CommandWrapper  (self,'Make'),
                CommandWrapper  (self,'Patch'),
                CommandWrapper  (self,'SysCommand', reg_name='Command'),
                ConfigureWrapper(self, 'Configure'),
                WaitDependenciesWrapper(self),
                ]

        for bld in builder_wrappers:
            bld.subscribe_to(libext_builders)

        kwargs['_globals']=kwargs.get('_globals',{})
        kwargs['_globals'].update(libext_builders)
        kwargs['_globals']['prj'] = self

        super(LibextProject, self).__init__( *args, **kwargs )



    def DeleteBuilder(self, file, **kwargs):
        env = self.env
        sub = env.subst
        return env.Command(
                env.Value("Delete " + sub(file)),
                [],
                [SCons.Defaults.Delete(file, must_exist=1)],
                target_factory=env.Value,
                **kwargs
                )


    def CopyBuilder(self, source, to, **kwargs):
        env = self.env
        sub = env.subst
        res = env.Command(
                env.Value(sub("Copy {0} to {1}".format(source, to))),
                [],
                [SCons.Defaults.Copy(to, source)],
                target_factory=env.Value,
                **kwargs
                )
        env.Clean(res, to)
        return res


    def MkdirBuilder(self, dir, **kwargs):
        env = self.env
        args = [dir]
        res = env.Mkdir([marker('Mkdir',self.full_name, args)], [], ARGS=args)
        env.Clean(res, dir)
        return res


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
        return [os.path.join(*path)]


    @cached_property
    def lib_path (self):
        path = [self.local_dir, 'lib']
        return os.path.join(*path)

    @cached_property
    def deps_include_path (self):
        inc = []
        for lib in self.source_rec_deps:
            inc += lib.include_path
        return inc

    @cached_property
    def deps_lib_path (self):
        inc = [lib.lib_path for lib in self.source_rec_deps]
        return inc

    @cached_property
    def deps_nodes (self):
        inc = [lib.build() for lib in self.source_rec_deps]
        return inc

    @cached_property
    def environment(self):
        prj = self
        env = self.env
        deps = dict(
                ('DEP_{0}'.format(p.name).upper(), p.local_dir)
                for p in self.source_rec_deps
                )
        items = deps.items()
        deps_include = dict(( k+'_INCLUDE' , v+'/include') for k,v in items)
        deps_lib     = dict(( k+'_LIB'     , v+'/lib'    ) for k,v in items)
        deps_bin     = dict(( k+'_BIN'     , v+'/bin'    ) for k,v in items)
        kwdeps = {}
        kwdeps.update(deps)
        kwdeps.update(deps_include)
        kwdeps.update(deps_lib)
        kwdeps.update(deps_bin)
        kwdeps['DEPS'] = os.pathsep.join(deps.values())
        kwdeps['DEPS_INCLUDE'] = os.pathsep.join(deps_include.values())
        kwdeps['DEPS_LIB'] = os.pathsep.join(deps_lib.values())
        kwdeps['DEPS_BIN'] = os.pathsep.join(deps_bin.values())


        download_target = env.Dir(prj.download_target)
        extract_dir = env.Dir(prj.extract_dir)
        kwargs = {
                    'DOWNLOAD_DIR'        : download_target,
                    'EXTRACT_DIR'         : extract_dir    ,
                    'BUILD_DIR'           : prj.build_dir  ,
                    'LOCAL_DIR'           : prj.local_dir  ,
                    'RC_DIR'              : prj.rc_path    ,
                    'NAME'                : prj.name       ,
                    'VERSION'             : prj.version    ,
                    #'LIBEXT_INCLUDE_PATH' : os.pathsep.join(prj.deps_include_path),
                    #'LIBEXT_LIBRARY_PATH' : os.pathsep.join(prj.deps_lib_path),
                    'SUBPROCESSPREFIXSTR' : '[{0}]:'.format(self.name),
                    'DEBUG_FLAG'          : '',
                    'RELEASE_FLAG'        : '',
                    }

        kwargs.update(kwdeps)

        kwargs
        if self.get('DEBUG') != 'release':
            BuildType = 'Debug'
            kwargs['DEBUG_FLAG'] = 'd'
            kwargs['DEBUGONOFF'] = 'on'
            kwargs['DEBUGYESNO'] = 'yes'
        else:
            BuildType = 'Release'
            kwargs['RELEASE_FLAG'] = 'r'
            kwargs['DEBUGONOFF'] = 'off'
            kwargs['DEBUGYESNO'] = 'no'

        kwargs['BuildType'] = BuildType
        kwargs['BUILDTYPE'] = BuildType.upper()
        kwargs['buildtype'] = BuildType.lower()
        kwargs['lower'] = str.upper
        kwargs['upper'] = str.lower
        kwargs['_VERSION_'] = prj.version.replace('.','_')

        return kwargs

    @run_once
    def configure_env(self):
        prj = self
        env = self.env
        env.Append(**self.environment)
        #super(LibextProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        prj = self
        env = self.env

        result = []
        prj.configure_env()

        prj.prj_locals['generate']()

        kwargs = self.environment

        res = [
                self.MkdirBuilder('${LOCAL_DIR}', **kwargs),
                self.MkdirBuilder('${LOCAL_DIR}/bin', **kwargs),
                self.MkdirBuilder('${LOCAL_DIR}/lib', **kwargs),
                self.MkdirBuilder('${LOCAL_DIR}/include', **kwargs),
                ]
        res += BuilderWrapper.apply_calls( prj, **kwargs)

        previous_node = []
        for nodes in res:
            if not isinstance(nodes, LibextProject):
                for node in nodes:
                    #HACK: scons need a name attribute to manage dependencies
                    if not hasattr(node, "name"):
                        node.name = ''
                    env.Depends( node, previous_node )
                    previous_node = node
            else:
                previous_node = [previous_node, nodes.deps_nodes]

        if not isinstance(nodes, LibextProject):
            result += nodes
        else:
            result += previous_node

        for node in [prj.extract_dir]:
            env.Clean(node, node)


        alias = 'result-{prj.type}-{prj.full_name}'
        result = env.Alias (alias.format(prj=self), result)
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

        return result

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os
import time

import SCons.Defaults
import SCons.Node

from os.path import join as opjoin

import racy

from racy            import rutils
from racy.renv       import constants
from racy.rproject   import ConstructibleRacyProject, LibName
from racy.rutils     import cached_property, memoize, run_once

from sconsbuilders.utils import marker

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
        target = marker(self.builder_name, self.prj.full_name, options)
        kwargs.setdefault('target', [target])
        kwargs.setdefault('source', [pwd])
        return kwargs

    def builder(self, options, pwd, **kwargs):
        kwargs = self.builder_args(options, pwd, **kwargs)
        scons_builder = getattr(self.prj.env, self.builder_name)
        if not pwd:
            msg = "{0}: missing or invalid pwd."
            racy.RacyPluginError, msg.format(self.__class__.__name__)
        return scons_builder(**kwargs)


class ConfigureWrapper(CommandWrapper):

    def __call__(self, *args, **kwargs):
        prj = self.prj
        ENV = prj.env['ENV']
        ENV['CXXFLAGS']  = ENV.get('CXXFLAGS','')
        ENV['CFLAGS']    = ENV.get('CFLAGS','')
        ENV['LINKFLAGS'] = ENV.get('LINKFLAGS','')
        ENV['CXXFLAGS']  += ' ' + kwargs.get('CXXFLAGS','')
        ENV['CFLAGS']    += ' ' + kwargs.get('CFLAGS','')
        ENV['LINKFLAGS'] += ' ' + kwargs.get('LINKFLAGS','')
        ENV['CXXFLAGS']  += '${DEPS_INCLUDE_FLAGS}'
        ENV['CFLAGS']    += '${DEPS_INCLUDE_FLAGS}'
        ENV['LINKFLAGS'] += '${DEPS_LIB_FLAGS}'
        #ENV['CXXFLAGS']  += ' -I'.join([''] + prj.deps_include_path)
        #ENV['CFLAGS']    += ' -I'.join([''] + prj.deps_include_path)
        #ENV['LINKFLAGS'] += ' -L'.join([''] + prj.deps_lib_path)
        ENV['CXXFLAGS']  = prj.env.subst(ENV['CXXFLAGS'])
        ENV['CFLAGS']    = prj.env.subst(ENV['CFLAGS'])
        ENV['LINKFLAGS'] = prj.env.subst(ENV['LINKFLAGS'])
        ENV['LDFLAGS'] = ENV['LINKFLAGS']

        ARGS = kwargs.setdefault('ARGS', [])
        ARGS.append('--prefix=${LOCAL_DIR}')

        if prj.is_debug:
            ARGS.append('--enable-debug')
        else:
            ARGS.append('--disable-debug')

        super(ConfigureWrapper, self).__call__(*args, **kwargs)


class CMakeWrapper(CommandWrapper):
    def __call__(self, *args, **kwargs):
        prj = self.prj

        def build_type():
            if prj.is_debug:
                return 'Debug'
            else:
                return 'Release'

        ARGS = kwargs.setdefault('ARGS', [])
        ARGS.insert(0,'-DCMAKE_BUILD_TYPE:STRING={0}'.format(build_type()))
        ARGS.insert(0,'-DCMAKE_PREFIX_PATH:PATH=${winpathsep(DEPS)}')
        ARGS.append('-DCMAKE_INSTALL_PREFIX:PATH=${LOCAL_DIR}')

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


class WhereIsWrapper(object):
    def __init__(self, prj):
        self.prj = prj
    def __call__(self, *args, **kwargs):
        subst = self.prj.env.subst
        for k,v in kwargs.items():
            kwargs[k] = subst(v)
        return self.prj.env.WhereIs(*subst(args), **kwargs)

class AppendENVPathWrapper(object):
    def __init__(self, prj):
        self.prj = prj
    def __call__(self, *args, **kwargs):
        subst = self.prj.env.subst
        for k,v in kwargs.items():
            kwargs[k] = subst(v)
        return self.prj.env.AppendENVPath(*subst(args), **kwargs)


class PrependENVPathWrapper(object):
    def __init__(self, prj):
        self.prj = prj
    def __call__(self, *args, **kwargs):
        subst = self.prj.env.subst
        for k,v in kwargs.items():
            kwargs[k] = subst(v)
        return self.prj.env.PrependENVPath(*subst(args), **kwargs)


class SetENVWrapper(object):
    def __init__(self, prj):
        self.prj = prj
    def __call__(self, name, newpath):
        subst = self.prj.env.subst
        self.prj.env['ENV'][name] = subst(newpath)
        return None

class SetWrapper(object):
    def __init__(self, prj):
        self.prj = prj
    def __call__(self, var, val):
        subst = self.prj.env.subst
        self.prj.env[var] = subst(val)
        return None


class LibextProject(ConstructibleRacyProject):
    LIBEXT    = ('libext', )

    ENV       = None

    def __init__(self, *args, **kwargs):
        self.generate_functions = generate_functions = {}
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
            bld.subscribe_to(generate_functions)

        self.env_functions = functions = {
                'WhereIs'         : WhereIsWrapper(self),
                'AppendENVPath'   : AppendENVPathWrapper(self),
                'PreprendENVPath' : PrependENVPathWrapper(self),
                'SetENV'          : SetENVWrapper(self),
                'Set'             : SetWrapper(self),
                }
        generate_functions.update(functions)

        kwargs['_globals']=kwargs.get('_globals',{})
        kwargs['_globals'].update(generate_functions)
        kwargs['_globals']['prj'] = self
        self.ENV = kwargs['_globals']['ENV'] = {}

        super(LibextProject, self).__init__( *args, **kwargs )



    def DeleteBuilder(self, file, **kwargs):
        env = self.env
        args = [file]
        res = env.LibextDelete([marker('Delete',self.full_name, args)], [], ARGS=args)
        return res


    def CopyBuilder(self, source, to, **kwargs):
        env = self.env
        args = [source, to]
        res = env.LibextCopyFile([marker('Copy',self.full_name, args)], [], ARGS=args)
        env.Clean(res, to)
        return res



    def MkdirBuilder(self, dir, **kwargs):
        env = self.env
        args = [dir]
        res = env.Mkdir([marker('Mkdir',self.full_name, args)], [], ARGS=args)
        env.Clean(res, dir)
        return res

    def WriteBuilder(self, file, content, **kwargs):
        env = self.env
        args = [file, content]
        res = env.Write(
                [marker('Write',self.full_name, args)],
                [],
                FILES    = [file],
                CONTENTS = [env.subst(content, raw=1)],
                )
        env.Clean(res, file)
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
    def build_bin_path (self):
        path = [self.local_dir, 'bin']
        return os.path.join(*path)



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
    def install_pkg_path(self):
        install_dir = racy.renv.dirs.install_binpkg
        install_dir = opjoin(install_dir, self.full_name)
        return install_dir


    @cached_property
    def deps_build_nodes (self):
        inc = [lib.build() for lib in self.source_rec_deps]
        return inc


    @cached_property
    def deps_install_nodes (self):
        inc = [lib.install() for lib in self.source_rec_deps]
        return inc

    @cached_property
    def environment(self):
        prj = self
        env = self.env
        direct_deps = self.source_deps
        all_deps    = set(self.source_rec_deps)
        indirect_deps = set(all_deps) - set(self.source_deps)
        all_deps.add(self)

        ld_var = racy.renv.LD_VAR
        local_bins = [ opjoin(dep.local_dir, 'bin') for dep in all_deps ]
        local_libs = [ opjoin(dep.local_dir, 'lib') for dep in all_deps ]
        env.PrependENVPath('PATH', local_bins)
        env.PrependENVPath(ld_var, local_libs)

        keys_deps = (
                ('DIRECT_DEP'  , direct_deps),
                ('INDIRECT_DEP', indirect_deps),
                ('DEP'         , all_deps),
                )

        if self.compiler.startswith('cl'):
            inc_opt = ' /I'
            lib_opt = ' /L'
        else:
            inc_opt = ' -I'
            lib_opt = ' -L'

        kwdeps = {}
        for prefix, dependencies in keys_deps:
            deps_prj = dict(
                    ('{0}_{1}'.format(prefix, p.name).upper(), p)
                    for p in dependencies
                    )
            deps = dict( (n , p.local_dir) for n, p in deps_prj.items())

            items = deps.items()
            deps_include = dict((k+'_INCLUDE', v+'/include') for k,v in items)
            deps_lib     = dict((k+'_LIB'    , v+'/lib'    ) for k,v in items)
            deps_bin     = dict((k+'_BIN'    , v+'/bin'    ) for k,v in items)

            deps_ver = dict((k+'_VERSION', p.version) for k,p in deps_prj.items())

            if prefix == 'DEP':
                kwdeps.update(deps)
                kwdeps.update(deps_include)
                kwdeps.update(deps_lib)
                kwdeps.update(deps_bin)
                kwdeps.update(deps_ver)
            join = os.pathsep.join

            vars = {
            '{0}S'        : join(deps.values()),
            '{0}S_INCLUDE': join(deps_include.values()),
            '{0}S_LIB'    : join(deps_lib.values()),
            '{0}S_BIN'    : join(deps_bin.values()),

            '{0}S_INCLUDE_FLAGS' : inc_opt.join([''] + deps_include.values()),
            '{0}S_LIB_FLAGS'     : lib_opt.join([''] + deps_lib.values()),
            }

            for k, v in vars.items():
                kwdeps[k.format(prefix)] = v

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
                    'VERSION_DASHED'      : prj.version.dashed      ,
                    'VERSION_DOTTED'      : prj.version.dotted      ,
                    'VERSION_UNDERSCORED' : prj.version.underscored ,
                    '_VERSION_'           : prj.version.underscored ,
                    #'LIBEXT_INCLUDE_PATH' : os.pathsep.join(prj.deps_include_path),
                    #'LIBEXT_LIBRARY_PATH' : os.pathsep.join(prj.deps_lib_path),
                    'CURRENT_PROJECT'     : self.name      ,
                    }

        kwargs.update(kwdeps)

        if self.is_debug:
            BuildType = 'Debug'
            kwargs['IS_DEBUG']     = True
            kwargs['DEBUG_FLAG']   = 'd'
            kwargs['RELEASE_FLAG'] = ''
            kwargs['DEBUGONOFF']   = 'on'
            kwargs['DEBUGYESNO']   = 'yes'
        else:
            BuildType = 'Release'
            kwargs['IS_DEBUG']     = False
            kwargs['DEBUG_FLAG']   = ''
            kwargs['RELEASE_FLAG'] = 'r'
            kwargs['DEBUGONOFF']   = 'off'
            kwargs['DEBUGYESNO']   = 'no'

        kwargs['BuildType'] = BuildType
        kwargs['BUILDTYPE'] = BuildType.upper()
        kwargs['buildtype'] = BuildType.lower()
        kwargs['lower'] = str.upper
        kwargs['upper'] = str.lower
        kwargs['winpathsep']  = lambda s:s.replace(':',';')
        kwargs['unixpathsep'] = lambda s:s.replace(';',':')
        kwargs['winsep']      = lambda s:s.replace('/','\\')
        kwargs['unixsep']     = lambda s:s.replace('\\','/')
        kwargs['winlinesep']  = lambda s:s.replace('\n','\r\n')
        kwargs['unixlinesep'] = lambda s:s.replace('\r\n','\n')

        kwargs['SYSTEM']    = racy.renv.platform()
        kwargs['COMPILER']  = str(prj.compiler)
        kwargs['NOW']     = time.ctime()

        return kwargs

    def configure_consumer(self, consumer, self_configure = True):
        direct_deps = self.source_deps

        for d in direct_deps:
            d.configure_consumer(consumer)

        if self_configure:
            configure = self.prj_locals.get('configure_consumer')
            if configure is not None:
                configure(consumer)


    @run_once
    def configure_env(self):
        prj = self
        env = self.env
        self.ENV.update(self.environment)
        env.Append(**self.ENV)
        #super(LibextProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        prj = self
        env = self.env

        result = []

        class ConfigureMethods(object):
            prj = self
            for name, f in self.env_functions.items():
                locals()[name] = f

        prj.configure_env()
        prj.configure_consumer(ConfigureMethods, False)
        command = CommandWrapper(prj,'SysCommand')
        prj.prj_locals['generate']()

        if racy.renv.is_darwin():
            install_tool = opjoin(racy.get_bin_path(),'..','Utils',
                                    'osx_install_name_tool.py')
            libs = [self.lib_path]
            deps_lib = self.ENV['DEPS_LIB']
            if deps_lib:
                libs += deps_lib.split(':')

            command(['python', install_tool, '-i', '-a', '-P','*',
                '-s',self.build_bin_path] + libs , pwd = '.')


        #import defined strings and functions from generate method
        for k,v in self.ENV.items():
            if isinstance(v, basestring) or callable(v):
                env[k] = v

        res = [
                self.MkdirBuilder('${LOCAL_DIR}'),
                self.MkdirBuilder('${LOCAL_DIR}/bin'),
                self.MkdirBuilder('${LOCAL_DIR}/lib'),
                self.MkdirBuilder('${LOCAL_DIR}/include'),
                ]
        res += BuilderWrapper.apply_calls( prj, **self.ENV )

        downloads = [x for x in res if self.download_target in str(x)]
        map(res.remove, downloads)
        res = downloads + res

        previous_node = []
        for nodes in res:
            if not isinstance(nodes, LibextProject):
                for node in nodes:
                    #HACK: scons need a name attribute to manage dependencies
                    if not hasattr(node, "name"):
                        node.name = ''
                    env.Depends( node, previous_node )
                    previous_node = node
            elif deps_results:
                previous_node = [previous_node, nodes.deps_build_nodes]

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
        res = self.result(build_deps)
        return res

    @cached_property
    def install_nodes(self):
        prj = self
        env = self.env
        initmodel = opjoin(prj.rc_path,'__init__.py')
        if os.path.isfile(initmodel):
            content  = rutils.get_file_content(initmodel)
            initfile = opjoin(prj.local_dir, '__init__.py')
            write    = prj.WriteBuilder(initfile, content)
            copy  = prj.CopyBuilder('${LOCAL_DIR}', prj.install_pkg_path)
            env.Depends(copy, write)
        return [copy, write]

    @memoize
    def install (self, opts = ['rc','deps']):
        prj = self
        env = self.env

        install_deps = 'deps' in opts
        result = prj.build(build_deps=install_deps)

        nodes = self.install_nodes
        env.Depends(nodes, result)
        result = nodes

        alias = 'install-{prj.type}-{prj.full_name}'
        result = env.Alias (alias.format(prj=prj), result)

        if install_deps:
            env.Depends(result, prj.deps_install_nodes)

        return result


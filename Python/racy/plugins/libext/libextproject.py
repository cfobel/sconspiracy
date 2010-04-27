# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os
import SCons.Defaults

from os.path import join as opjoin

import racy
import racy.rscons.url

from racy.renv       import constants
from racy.rproject   import ConstructibleRacyProject, LibName
from racy.rutils     import cached_property, memoize, run_once



class LibextError(racy.RacyProjectError):
    pass

class NodeHolder(object):

    def __init__(self):
        self._node = None

    @property
    def node(self):
        node = self._node
        if node is None:
            raise LibextError, "Node uninitialized"
        return node

    @node.setter
    def node(self, n):
        self._node = n

    @staticmethod
    def unwrap(iterable):
        def unwrap_filter(a):
            if isinstance(a, NodeHolder):
                return a.node
            return a

        def unwrap_dict_item(item):
            k,v = item
            return k, unwrap_filter(v)

        if isinstance(iterable, dict):
            res = dict(map(unwrap_dict_item, iterable.items()))
        else:
            res = map(unwrap_filter, iterable)

        return res


        

class BuilderWrapper(object):
    _called_builders = {}

    def __init__(self, prj, name, builder = None, reg_name = None):
        self.prj                   = prj
        self.builder_name          = name
        self.builder_reg_name      = reg_name if reg_name else name
        self.builder               = builder
        self._called_builders[prj] = []

    @property
    def called_builders(self):
        return self._called_builders[self.prj]

    def __call__(self, *args, **kwargs):
        nodewrap = NodeHolder()
        call = (self.builder_name, self.builder, args, kwargs, nodewrap)
        self.called_builders.append(call)
        return nodewrap

    def subscribe_to(self, dict):
        dict[self.builder_reg_name] = self

    @staticmethod
    def apply_calls(prj, *args, **kwargs):
        env = prj.env
        called_builders = BuilderWrapper._called_builders[prj]
        results = []
        for (name, builder, call_args, call_kwargs, ndwrap) in called_builders:
            if builder is None:
                builder = getattr(env, name)
            if builder is None:
                raise LibextError, "Builder " + name + "Not found"
            builder_args = []
            builder_args.extend(NodeHolder.unwrap(call_args))
            builder_args.extend(args)
            builder_kwargs = {}
            builder_kwargs.update(NodeHolder.unwrap(call_kwargs))
            builder_kwargs.update(kwargs)
            ndwrap.node = builder(*builder_args, **builder_kwargs)
            results.append(ndwrap.node)
        return results


class LibextProject(ConstructibleRacyProject):
    LIBEXT    = ('libext', )

    def __init__(self, *args, **kwargs):

        libext_builders = {}
        builder_wrappers = [
                BuilderWrapper(self,'Download'),
                BuilderWrapper(self,'UnTar'),
                BuilderWrapper(self,'Delete',self.DeleteBuilder),
                BuilderWrapper(self,'CMake'),
                BuilderWrapper(self,'Make'),
                ]

        for bld in builder_wrappers:
            bld.subscribe_to(libext_builders)

        kwargs['_globals']=kwargs.get('_globals',{})
        kwargs['_globals'].update(libext_builders)
        kwargs['_globals']['Url'] = racy.rscons.url.Url
        super(LibextProject, self).__init__( *args, **kwargs )

        self.prj_locals['generate']()



    def DeleteBuilder(self, file, *args, **kwargs):
        env = self.env
        return env.Command(
                env.Value("no target"),
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


    @run_once
    def configure_env(self):
        super(LibextProject, self).configure_env()

    def build(self, *a, **k):
        env = self.env
        download_target = env.Dir(self.download_target)
        extract_dir = env.Dir(self.extract_dir)

        previous = []
        res = BuilderWrapper.apply_calls(
                    self                            ,
                    #DOWNLOADED_FILE = res           ,
                    DOWNLOAD_DIR    = download_target,
                    EXTRACT_DIR     = extract_dir   ,
                    BUILD_DIR       = self.build_dir,
                    LOCAL_DIR       = self.local_dir,
                    )

        for nodes in res:
            for node in nodes:
                #HACK: scons need a name attribute to manage dependencies
                if not hasattr(node, "name"):
                    node.name = ''
                env.Depends( node, previous )
                previous = node

        for node in [extract_dir]:
            env.Clean(node, node)

        return res

    @memoize
    def result(self, deps_results=True):
        prj = self
        env = self.env

        result = []
        self.configure_env()

        sources = []

        for node in result:
            env.Clean(node, node)

        return result


    #@cached_property
    #def install_path(self):
        #install_dir = racy.renv.dirs.install_doc
        #return install_dir


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

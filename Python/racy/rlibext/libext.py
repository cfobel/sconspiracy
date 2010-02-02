# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

@racy.no_undef_attr_read
@racy.no_undef_attr_write
class LibExt(object):
    register_names = []

    version        = '0'

    arch           = racy.renv.options.get_option('ARCH')

    compiler       = None

    depends_on     = []

    basepath       = racy.Undefined

    binpath        = []

    libpath        = []
    libs           = []
    extra_libs     = []

    cpppath        = []
    cppdefines     = []

    frameworkpath  = []
    frameworks     = []

    cxxflags       = []
    linkflags      = []

    parse_configs  = {}

    debug_suffix   = ''

    scons_tools    = []
    scons_env      = {}

    name  = None
    debug = None

    __src__ = None

    def __init__(self, name, debug, infosource=None):
        func = getattr(self, racy.renv.system(), self.not_managed)

        self.name = name
        self.debug = debug

        if infosource is None:
            infosource = self.__class__
        else:
            self.basepath = getattr(infosource, 'basepath',
                                    infosource.__path__[0])
            self.basepath = os.path.abspath(self.basepath)

        if self.basepath is racy.Undefined:
            raise LibExtException, "Unable to find {0} base path"

        names = [
                'register_names', 'depends_on'    ,
                'binpath'       ,
                'libpath'       , 'libs'          , 'extra_libs',
                'cpppath'       , 'cppdefines'    ,
                'frameworks'    , 'frameworkpath' ,
                'cxxflags'      , 'linkflags'     ,
                'parse_configs' 
                ]
        for name in names:
            classattr = getattr(infosource, name, getattr(self, name))
            #check if classattr is not a property
            if not hasattr(classattr,'getter'):
                attr = getattr(infosource, name, getattr(self, name))
                setattr(self,name, list(attr))

        self.version = racy.rutils.Version(infosource.version)
        self.arch = infosource.arch

        self.init()
        func()

    def init(self):
        pass

    def linux(self):
        pass

    def darwin(self):
        pass

    def windows(self):
        pass

    def not_managed(self):
        msg = '<{0}> system is not managed.'.format(racy.renv.system())
        from racy import LibExtException
        raise LibExtException, msg

    @property
    def DEBUG_SUFFIX(self):
        return self.debug_suffix if self.debug else ''

    @property
    def BINPATH(self):
        return self.binpath

    @property
    def LIBPATH(self):
        return self.libpath

    @property
    def LIBS(self):
        def checkdebug(s):
            debug_tag = '{debug}'
            if debug_tag not in s:
                s += debug_tag
            s = s.format(debug = self.DEBUG_SUFFIX)
            return s
        res = [checkdebug(lib) for lib in self.libs]
        return res + self.extra_libs

    @property
    def CPPPATH(self):
        return self.cpppath

    @property
    def CPPDEFINES(self):
        return self.cppdefines

    @property
    def FRAMEWORKPATH(self):
        return self.frameworkpath

    @property
    def FRAMEWORKS(self):
        return self.frameworks

    @property
    def LINKFLAGS(self):
        return self.linkflags

    @property
    def CXXFLAGS(self):
        return self.cxxflags

    @staticmethod
    def absolutize(path, base):
        """Return an absolute path : path if path is an abspath else base+path
        """
        if not os.path.isabs(path):
            path = os.path.join(base, path)
            path = os.path.normpath(path)
            path = os.path.abspath(path)
        return path

    @staticmethod
    def get_libext_path(path):
        path = racy.rutils.iterize(path)
        path = os.path.join(*path)
        return path

    def preconfigure(self, env, opts):
        pass

    def configure(self, env, opts=[]):
        back_env = env.Clone()
        self.preconfigure(env, opts)

        nolink = 'nolink' in opts
        conf = {}
        names = [
                'LIBPATH'      , 'LIBS'      ,
                'CPPPATH'      , 'CPPDEFINES',
                'FRAMEWORKPATH', 'FRAMEWORKS',
                'CXXFLAGS'     , 'LINKFLAGS' ,
                ]

        for name in names:
            attr = getattr(self, name)
            if attr:
                if 'PATH' in name:
                    attr = [self.get_libext_path(path) for path in attr]
                    attr = [self.absolutize(path, self.basepath) for path in attr]
                conf[name] = attr

        if self.parse_configs:
            try :
                for config in self.parse_configs:
                    env.ParseConfig(config)
            except OSError, e:
                from racy import LibExtException
                raise LibExtException, e

            if nolink:
                for name in ['LIBPATH','LIBS','LINKFLAGS']:
                    env[name] = back_env[name]

        env.AppendUnique(**conf)


        bin_path = [self.get_libext_path(path) for path in self.BINPATH]
        bin_path = [self.absolutize(path, self.basepath) for path in bin_path]
        env.PrependENVPath('PATH',bin_path)


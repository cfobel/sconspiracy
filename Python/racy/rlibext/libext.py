# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from racy import LibExtException

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
    libs_install   = []

    extra_libs     = []

    cpppath        = []
    cppdefines     = []

    frameworkpath  = []
    frameworks     = []

    cxxflags       = []
    linkflags      = []

    parse_configs  = {}

    debug_suffix   = ''

    install        = []

    scons_tools    = []
    scons_env      = {}

    name  = None
    debug = None

    _src            = None
    _project_source = None

    def __init__(self, name, debug, infosource=None):
        platform_init = getattr(self, racy.renv.system(),
                                self.platform_not_managed)

        self.name = name
        self.debug = debug

        if infosource is None:
            infosource = self.__class__
            infosource_instance = self
        else:
            infosource_instance = infosource()
            self.basepath = getattr(infosource, 'basepath',
                                    infosource.__path__[0])
            self.basepath = os.path.abspath(self.basepath)

        if self.basepath is racy.Undefined:
            raise LibExtException, "Unable to find {0} base path".format(name)

        names = [
                'register_names', 'depends_on'    ,
                'binpath'       ,
                'libpath'       , 'libs'          ,
                'debug_suffix'  ,
                'libs_install'  , 'extra_libs'    ,
                'cpppath'       , 'cppdefines'    ,
                'frameworks'    , 'frameworkpath' ,
                'cxxflags'      , 'linkflags'     ,
                'parse_configs' ,
                'scons_tools'   , 'scons_env'     ,
                'install'       ,
                ]
        import copy
        for name in names:
            attr = getattr(infosource_instance, name, getattr(self, name))

            if callable(attr):
                try:
                    attr = attr()
                except TypeError:
                    msg = ("libext callable members must take only one "
                            "argument (self). '{attr}' method is"
                            "invalid  in '{lib}' __init__.py file.")
                    raise LibExtException, msg.format(lib=self.name, attr=name)

            if isinstance(attr,basestring) or hasattr(attr,'__iter__'):
                setattr(self,name, copy.deepcopy(attr))
            else:
                msg = ("libext members must be an allowed type (list, dict, str"
                       "), a callable, or a property. '{attr}' attribute type "
                       "({attrtype}) is invalid  in '{lib}' __init__.py file.")
                raise LibExtException, msg.format(
                        lib=self.name,
                        attr=name,
                        attrtype=type(attr))

        self.version = racy.rutils.Version(infosource_instance.version)
        self.arch = infosource_instance.arch

        self.init()
        platform_init()

    def init(self):
        pass

    def linux(self):
        pass

    def darwin(self):
        pass

    def windows(self):
        pass

    def platform_not_managed(self):
        msg = '<{0}> system is not managed.'.format(racy.renv.system())
        from racy import LibExtException
        raise LibExtException, msg

    @property
    def DEBUG_SUFFIX(self):
        return self.debug_suffix if self.debug else ''

    @property
    def BINPATH(self):
        return map(LibExt.get_path, self.binpath)

    @property
    def LIBPATH(self):
        return map(LibExt.get_path, self.libpath)

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
        return map(LibExt.get_path, self.cpppath)

    @property
    def CPPDEFINES(self):
        return self.cppdefines

    @property
    def FRAMEWORKPATH(self):
        return map(LibExt.get_path, self.frameworkpath)

    @property
    def ABS_BINPATH(self):
        return self.get_abs_path(self.binpath)

    @property
    def ABS_LIBPATH(self):
        return self.get_abs_path(self.libpath)

    @property
    def ABS_CPPPATH(self):
        return self.get_abs_path(self.cpppath)

    @property
    def ABS_FRAMEWORKPATH(self):
        return self.get_abs_path(self.frameworkpath)


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
    def get_path(path):
        path = racy.rutils.iterize(path)
        path = os.path.join(*path)
        return path

    def get_abs_path(self, pathlst):
            pathlst = [LibExt.get_path(path) for path in pathlst]
            pathlst = [LibExt.absolutize(path, self.basepath)
                        for path in pathlst]
            return pathlst

    def preconfigure(self, env, opts):
        pass

    def configure(self, env, opts=[]):
        back_env = env.Clone()
        self.preconfigure(env, opts)

        nolink = 'nolink' in opts
        conf = {}
        names = {
                'LIBPATH'       : 'ABS_LIBPATH'      ,
                'CPP_LIBEXT_PATH'       : 'ABS_CPPPATH'      ,
                #'CPPPATH'       : 'ABS_CPPPATH'      ,
                'FRAMEWORKPATH' : 'ABS_FRAMEWORKPATH',
                'LIBS'          : 'LIBS'             ,
                'CPPDEFINES'    : 'CPPDEFINES'       ,
                'FRAMEWORKS'    : 'FRAMEWORKS'       ,
                'CXXFLAGS'      : 'CXXFLAGS'         ,
                'LINKFLAGS'     : 'LINKFLAGS'        ,
                }

        for name, attr_name in names.items():
            attr = getattr(self, attr_name)
            if attr:
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
                if env.has_key(name):
                    env[name] = back_env[name]

        
        env.PrependUnique(**conf)


        bin_path = [self.get_path(path) for path in self.BINPATH]
        bin_path = [self.absolutize(path, self.basepath) for path in bin_path]
        env.PrependENVPath('PATH',bin_path)


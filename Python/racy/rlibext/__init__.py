# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os
import traceback
import functools

import racy

from racy.rutils import Version

from libext import LibExt

UNSPECIFIED_COMPLIER = 'unspecified_compiler'

class register(object):

    # dictionnary registering libext as libs[name][compiler][version]
    libs       = {}
    configured = {}

    def __call__(self, cls, src=None):
        self.register(cls, src)

    def register(self, cls, src=None):
        if issubclass(cls, LibExt):
            src = traceback.extract_stack()[-2][0] # caller's file


        for name in cls.register_names:
            name    = name.lower()
            version = Version(cls.version)
            comp    = Version(getattr(cls, 'compiler', ''))
            comp    = comp if comp else UNSPECIFIED_COMPLIER
            nv      = version.normalized


            self.libs.setdefault(name,{}).setdefault(comp,{})

            if nv in self.libs[name][comp]:
                overrided = self.libs[name][comp][nv]
                msg = ('<{lib}-{comp}-{version}> libext will be overrided. '
                       'Previously defined in <"{fileorig}">. '
                       'New definition in <"{file}">.')
                msg = msg.format(
                        lib      = name,
                        comp     = comp,
                        version  = nv,
                        fileorig = overrided.__src__,
                        file     = src
                        )
                import racy
                racy.print_warning("Overrided libext", msg)

            libext = cls
            if not issubclass(cls, LibExt):
                libext = functools.partial(LibExt, infosource=cls)

            libext.__src__ = src
            self.libs[name][comp][nv] = libext

            # Management of tools added by libexts
            # WARNING : actually if several binpkgs provide the same tool, the
            # last loaded one will be used
            if hasattr(cls, "scons_tools"):
                import racy.renv.environment
                racy.renv.environment.add_tool(cls.scons_tools)

            if hasattr(cls, "scons_env"):
                import racy.renv.environment
                vars = dict(cls.scons_env)
                for var, val in vars.items():
                    if isinstance(val,basestring) and (var.endswith('DIR')):
                        vars[var] = LibExt.absolutize(val,libext(name,False).basepath)

                racy.renv.environment.add_var(vars)


    def load_binpkgs(self, path):
        from racy.renv.options import get_option
        arch     = get_option('ARCH')
        debug    = get_option('DEBUG') != 'release'
        platform = get_option('PLATFORM')
        modules  = []

        for root, dirs, files in os.walk(path):
            if '__init__.py' in files:
                dirs[:] = []
                modules.append(os.path.split(root))

        import imp
        import types
        for path, name in modules:
            desc = imp.find_module(name, [path])

            try:
                module = imp.load_module(name, *desc)
            finally:
                fp = desc[0]
                if fp:
                    fp.close()

            for key, obj in module.__dict__.items():
                if not key.startswith('_'):
                    if isinstance(obj,(types.ClassType,types.TypeType)):
                        is_usable = (
                                obj.arch == arch,
                                obj.platform == platform,
                                obj.debug == debug,
                                )
                        if all(is_usable):
                            srcpath = os.path.join(path,name)
                            obj.__path__ = [srcpath]
                            self(obj, srcpath)



    def is_available(self, lib, compiler=None, version=None):
        if version is None:
            version = getattr(lib,'version',version)
            version = getattr(version,'normalized',version)
        lib = getattr(lib,'name',lib).lower()

        libreg = self.libs
        available = libreg.has_key(lib)

        if available:
            comp = compiler if compiler else sorted(libreg[lib])[-1]
            available = available and libreg[lib].has_key(comp)
            if version:
                available = available and libreg[lib][comp].has_key(version)

        return available


    def configure(self, prj, lib, opts = []):
        if hasattr(lib, '__iter__'):
            for el in lib:
                self.configure(prj, el, opts)
        else:
            libname = getattr(lib,'name',lib).lower()
            libreg  = self.libs
            libext  = None

            if libname in libreg and libreg[libname]:
                from racy.renv.options import get_option

                comp = prj.compiler

                if comp not in libreg[libname]:
                    comp_avail = [el for el in libreg[libname] 
                                        if str(el) != UNSPECIFIED_COMPLIER]
                    if comp_avail:
                        comp = sorted(comp_avail)[-1]
                    else:
                        comp = UNSPECIFIED_COMPLIER
                
                lib_avail = libreg[libname][comp]

                binpkg_versions = get_option('BINPKG_VERSIONS')

                if getattr(lib,'version',''):
                    version = lib.version.normalized
                else:
                    last = sorted(lib_avail)[-1]
                    version = binpkg_versions.get(libname, last)

                if version != binpkg_versions.setdefault(libname,version):
                    msg = ( 'Libext <{libext}> required version {req} (in {prj} '
                            '[{prj.opts_source}]) is in conflict with currently'
                            'configured version {current}. (You may need to '
                            'update your "BINPKG_VERSIONS" variable)' 
                            )
                    raise racy.LibExtException, msg.format(
                                    libext  = libname,
                                    prj     = prj,
                                    req     = version,
                                    current = binpkg_versions[libname],
                                    )
                
                version = binpkg_versions[libname]
                factory = lib_avail[version]
                libext = factory(libname, get_option('DEBUG') != 'release')
                libext.__src__ = factory.__src__
        
            else: 
                msg = ( 'Libext <{libext}> not found, '
                        'required by {prj} ({prj.opts_source})' )
                raise racy.LibExtException, msg.format(libext=lib,prj=prj)


            if libext:
                depends_opts = list(set(opts + ['nolink']))

                if 'forcelink' in opts:
                    opts = list( set(opts) - set(['nolink']) )

                self.configure(prj, libext.depends_on, depends_opts)
                libext.configure(prj.env, opts)

                self.configured.setdefault(libname, libext)



register = register()


def load_binpkgs():
    register.load_binpkgs(racy.renv.dirs.binpkg)

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os
import traceback
import functools

from collections import defaultdict


import racy

from libext import LibExt


class register(object):
    libs = defaultdict(dict)

    def __call__(self, cls, src=None):
        if issubclass(cls, LibExt):
            src = traceback.extract_stack()[-2][0] # caller's file


        for name in cls.register_names:
            name = name.lower()
            if not isinstance(cls.version, racy.rutils.Version):
                cls.version = racy.rutils.Version(cls.version)
            version = cls.version
            nv =version.normalized

            if nv in self.libs[name]:
                overrided = self.libs[name][nv]
                msg = ('<{lib}-{version}> libext will be overrided. '
                       'Previously defined in <"{fileorig}">. '
                       'New definition in <"{file}">.')
                msg = msg.format(
                        lib      = name,
                        version  = nv,
                        fileorig = overrided.__src__,
                        file     = src
                        )
                racy.print_warning("Overrided libext", msg)

            libext = cls
            if not issubclass(cls, LibExt):
                libext = functools.partial(LibExt, infosource=cls)

            libext.__src__ = src
            self.libs[name][nv] = libext


register = register()



def load_libext(path):
    def get_libext_files(pth):
        import re
        pth = racy.rutils.iterize(pth)
        file_re = re.compile("^\w+$")
        res = []
        for p in pth:
            libext_files = os.walk(p).next()[2]
            libext_files = [ os.path.join(p,f) 
                    for f in libext_files if file_re.match(f) ]
            res += libext_files
        return res

    predefs = {
            "LibExt"   : LibExt,
            "register" : register
            }
    for f in get_libext_files(path):
        execfile(f, predefs) 


def load_binpkgs(path):
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
                        register(obj, srcpath)



def is_available(lib, version=None):
    if version is None:
        version = getattr(lib,'version',version)
        version = getattr(version,'normalized',version)
    lib = getattr(lib,'name',lib).lower()

    reg = register.libs
    available = reg.has_key(lib)
    if version:
        available = available and reg[lib].has_key(version)

    return available
 

def configure(prj, lib, opts = []):
    if hasattr(lib, '__iter__'):
        for el in lib:
            configure(prj, el)
    else:
        libname  = getattr(lib,'name',lib).lower()
        if libname in register.libs:
            from racy.renv.options import get_option
            
            binpkg_versions = get_option('BINPKG_VERSIONS')

            if getattr(lib,'version',''):
                version = lib.version.normalized
            else:
                versions = register.libs[libname]
                last = sorted(versions)[-1]
                version = binpkg_versions.get(libname, last)

            if version != binpkg_versions.setdefault(libname,version):
                msg = ( 'Libext <{libext}> required version {req} (in {prj} '
                        '[{prj.opts_path}]) is in conflict with currently'
                        'configured version {current}' )
                raise racy.LibExtException, msg.format(libext=libname, prj=prj,
                        req=version, current=binpkg_versions[libname])
            
            version = binpkg_versions[libname]
            factory = register.libs[libname][version]
            libext = factory(libname, get_option('DEBUG') != 'release')
            libext.__src__ = factory.__src__
    
            depends_opts = list(set(opts + ['nolink']))

            if 'forcelink' in opts:
                opts = list( set(opts) - set(['nolink']) )

            configure(prj, libext.depends_on, depends_opts)
            libext.configure(prj.env, opts)

            configure.configured.setdefault(libname, libext)
        else: 
            msg = ( 'Libext <{libext}> not found, '
                    'required by {prj} ({prj.opts_path})' )
            raise racy.LibExtException, msg.format(libext=lib,prj=prj)

configure.configured = {}


#try:
    #import libs
    #load_libext(libs.__path__)
    #del libs
#except ImportError:
    #pass

try:
    load_binpkgs(racy.renv.dirs.binpkg)
except racy.EnvError:
    pass

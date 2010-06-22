# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import re

import os

import racy
from racy.renv   import constants
from racy.renv.options import get_option
from racy.rtools import get_tool
from racy.rtools import common

import SCons
msvc = get_tool('SCons.Tool.msvc')
msvs = get_tool('SCons.Tool.msvs')
vc = get_tool('SCons.Tool.MSCommon.vc')

exists = msvc.exists


class MsvcFlags(common.Flags):
    CXXFLAGS         = ['/GR']
    CXXFLAGS_RELEASE = ['/W3','/EHs','/Zm600','/MD','/Oi','/Ot','/Ob2','/TP']
    CXXFLAGS_DEBUG   = ['/W3','/EHsc','/MDd','/Od']
    CFLAGS           = []
    CFLAGS_RELEASE   = ['/MD']
    CFLAGS_DEBUG     = ['/MDd']
    CPPDEFINES       = [
                        'WIN32',
                        '_MBCS',
                        'NOMINMAX',
                       ]
    CPPDEFINES_RELEASE = []
    CPPDEFINES_DEBUG   = []
    LINKFLAGS      = []

    WARNINGSASERRORS_FLAGS = ['/WX']
    OPTIMIZATION_FLAGS     = ['/O${OPTIMIZATIONLEVEL}']

    LINKFLAGS_NOCONSOLE  = ['/subsystem:windows']
    CPPDEFINES_NOCONSOLE = ['_WINDOWS']

    LINKFLAGS_CONSOLE  = ['/subsystem:console']
    CPPDEFINES_CONSOLE = []

    CXXFLAGS_BUNDLE   = ['/EHsc']
    CPPDEFINES_BUNDLE = ['_USRDLL']

    CXXFLAGS_SHARED   = ['/EHsc']
    CPPDEFINES_SHARED = ['_USRDLL']

    CXXFLAGS_EXEC = ['/GA']

    CPPDEFINES_RACY_VISIBILITY = [
            ('_API_EXPORT'      , r'__declspec(dllexport)'),
            ('_API_IMPORT'      , r'__declspec(dllimport)'),
            ('_CLASS_API_EXPORT', r''),
            ('_CLASS_API_IMPORT', r''),
            ('_TEMPL_API_EXPORT', r''),
            ('_TEMPL_API_IMPORT', r'export/**/"C++"'),
                ]

class Msvc71(MsvcFlags):
    CXXFLAGS_RELEASE = ['/Og','/Gi']
    CXXFLAGS_DEBUG   = ['/Z7','/Wp64']

class Msvc9(MsvcFlags):
    CXXFLAGS_RELEASE = ['/Z7']
    CXXFLAGS_DEBUG =   ['/Z7']





def generate(env):
    """Add Builders and construction variables for msvc to an Environment."""

    msvc.generate(env)
    env.__class__.ManageOption = manage_options
    env.__class__.InstallFileFilter = install_file_filter

    MSVC_VERSION = env['MSVC_VERSION']
    # print [v.version for v in vs.get_installed_visual_studios()]
    versions_list = vc.cached_get_installed_vcs()
    if MSVC_VERSION not in versions_list:
        msg = ('VC version {ver} not installed.'
              ' Availables versions are : {list}')
        msg = msg.format(ver = MSVC_VERSION, list=versions_list)
        raise racy.ToolError('msvc', msg)
        
    # Run manifest tool as part of the link step
    # The number at the end of the line indicates the file type (1: EXE; 2:DLL).
    if re.match('^9', MSVC_VERSION):
         MTCOM = 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;'
         env['LINKCOM']   = [env['LINKCOM']  , MTCOM + '1']
         env['SHLINKCOM'] = [env['SHLINKCOM'], MTCOM + '2']
    env['WINDOWS_INSERT_MANIFEST'] = True
    

    if re.match('^7', MSVC_VERSION):
        FlagsGenerator = Msvc71
    if re.match('^9', MSVC_VERSION):
        FlagsGenerator = Msvc9

    flags = env.__class__.Flags = FlagsGenerator()
    common.merge_flags(env, flags)

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = 'cl'
    env['TOOLINFO']['VERSION'] = MSVC_VERSION



def manage_options(env, prj, options):
    common.manage_options(env, prj, options)

    if env.get('DEBUG') != 'release' :
        env['PDB'] = os.path.join(prj.build_dir, prj.full_name + '.pdb')

    if int(options.get('OPTIMIZATIONLEVEL')) > 2:
        msg = 'CL does not support an optimization level > 2'
        raise racy.ToolError('msvc', msg)

    nolib = options.get('NOLIB',[])
    if nolib:
        nolib = ['/nodefaultlib:"{0}"'.format(lib) for lib in nolib]
        env.AppendUnique(LINKFLAGS = nolib)

    rc_file = os.path.join(prj.vc_dir, prj.name + '.rc' )
    if os.path.exists( rc_file ):
        res_file = env.RES(rc_file)
        prj.special_source.append(res_file)
        
    def_files = [os.path.join(p, prj.name + '.def') for p in prj.src_path]
    if any(map(os.path.exists, def_files)):
        env['WIN32_INSERT_DEF']        = 1
        constants.CXX_SOURCE_EXT      += [env['WIN32DEFSUFFIX'][1:]]


def install_file_filter(env, f):
    to_install = [ '.exe', '.dll', '.pdb']
    res = hasattr(f,'get_path')
    if res:
        res = any(f.get_path().endswith(ext) for ext in to_install)
    return res
            




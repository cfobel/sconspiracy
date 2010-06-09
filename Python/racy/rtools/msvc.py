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
from racy.rutils import merge_lists_of_dict, is_true

import SCons
msvc = get_tool('SCons.Tool.msvc')
msvs = get_tool('SCons.Tool.msvs')
vc = get_tool('SCons.Tool.MSCommon.vc')

exists = msvc.exists

def generate(env):
    """Add Builders and construction variables for msvc to an Environment."""

    msvc.generate(env)
    env.__class__.ManageOption = manage_options
    env.__class__.InstallFileFilter = install_file_filter

    # print [v.version for v in vs.get_installed_visual_studios()]
    versions_list = vc.cached_get_installed_vcs()
    if env['MSVC_VERSION'] not in versions_list:
        msg = ('VC version {ver} not installed.'
              ' Availables versions are : {list}')
        msg = msg.format(ver = env['MSVC_VERSION'], list=versions_list)
        raise racy.ToolError('msvc', msg)
        
    # Run manifest tool as part of the link step
    # The number at the end of the line indicates the file type (1: EXE; 2:DLL).
    if re.match('^9', env['MSVC_VERSION']):
         MTCOM = 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;'
         env['LINKCOM']   = [env['LINKCOM']  , MTCOM + '1']
         env['SHLINKCOM'] = [env['SHLINKCOM'], MTCOM + '2']
    env['WINDOWS_INSERT_MANIFEST'] = True
    
    CFLAGS = []
    CXXFLAGS = [
            '/GR', 
            ]

    CPPDEFINES = [
            'WIN32',
            '_MBCS',
            'NOMINMAX',
            ]

    LINKFLAGS  = []

    if env.get('DEBUG') == 'release' :
        if env['MSVC_VERSION'] < 8:
            CXXFLAGS += ['/Og','/Gi']
        elif re.match('^9', env['MSVC_VERSION']):
            CXXFLAGS += ['/Z7']

        merge_lists_of_dict(locals(), constants.COMMON_RELEASE)

        CXXFLAGS += ['/W3','/EHs','/Zm600','/MD','/Oi','/Ot','/Ob2','/TP']
        CFLAGS += ['/MD']
    else :
        merge_lists_of_dict(locals(), constants.COMMON_DEBUG)

        CXXFLAGS += ['/W3','/EHsc','/MDd','/Od']
        CFLAGS += ['/MDd']

        if re.match('^[78]', env['MSVC_VERSION']):
            CXXFLAGS += ['/Z7','/Wp64']
        elif re.match('^9', env['MSVC_VERSION']):
            CXXFLAGS += ['/Z7']
        else :
            CXXFLAGS += ['/Zi']

    CPPDEFINES += [ ('__ARCH__' , r'\"{0}\"'.format(get_option('ARCH'))) ]
    
    names = ['CPPDEFINES','LINKFLAGS','CXXFLAGS','CFLAGS']
    attrs = [locals()[n] for n in names]
    env.MergeFlags(dict(zip(names,attrs)), unique=True)

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = "cl"
    env['TOOLINFO']['VERSION'] = env['MSVC_VERSION']



def manage_options(env, prj, options):
    CXXFLAGS   = []
    LINKFLAGS  = []
    CPPDEFINES = []
    if env.get('DEBUG') != 'release' :
        env['PDB'] = os.path.join(prj.build_dir, prj.full_name + ".pdb")

    if is_true(options.get('WARNINGSASERRORS', 'no')):
        CXXFLAGS += ['/WX']

    if str(options.get('OPTIMIZATIONLEVEL')) in ['1','2']:
        CXXFLAGS += ['/O{0}'.format(options['OPTIMIZATIONLEVEL'])]

    if is_true( options.get('CONSOLE') ):
        LINKFLAGS += ['/subsystem:console']
    else:
        LINKFLAGS  += ['/subsystem:windows','/incremental:yes']
        CPPDEFINES += ['_WINDOWS']

    nolib = options.get('NOLIB',[])
    nolib = ['/nodefaultlib:"{0}"'.format(lib) for lib in nolib]
    LINKFLAGS += nolib

    if prj.is_shared or prj.is_bundle :
        if re.match('^[789]', env['MSVC_VERSION']) :
            CXXFLAGS += ['/EHsc']
        else :
            CXXFLAGS += ['/GD','/GX']
        CPPDEFINES += ['_USRDLL']
    else :
        CXXFLAGS += ["/GA"]


    if options.get('USEVISIBILITY') == "racy":
        CPPDEFINES += [
            ('_API_EXPORT'      , r'__declspec(dllexport)'),
            ('_API_IMPORT'      , r'__declspec(dllimport)'),
            ('_CLASS_API_EXPORT', r''),
            ('_CLASS_API_IMPORT', r''),
            ('_TEMPL_API_EXPORT', r''),
            ('_TEMPL_API_IMPORT', r'export/**/"C++"'),
                ]

    env.Append( 
                CXXFLAGS   = CXXFLAGS  ,
                LINKFLAGS  = LINKFLAGS ,
                CPPDEFINES = CPPDEFINES
                )

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
    res = hasattr(f,"get_path")
    if res:
        res = any(f.get_path().endswith(ext) for ext in to_install)
    return res
            




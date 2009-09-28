# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import re

import os

from racy.renv   import constants
from racy.rtools import get_tool
from racy.rutils import merge_lists_of_dict, is_true

msvc = get_tool('SCons.Tool.msvc')

exists = msvc.exists

def generate(env):
    """Add Builders and construction variables for msvc to an Environment."""

    msvc.generate(env)
    env.__class__.ManageOption = manage_options

    # Run manifest tool as part of the link step
    # The number at the end of the line indicates the file type (1: EXE; 2:DLL).
#    if '8' in env['MSVS']['VERSION'] :
#        MTCOM = 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;'
#        env['LINKCOM']   = [env['LINKCOM']  , MTCOM + '1']
#        env['SHLINKCOM'] = [env['SHLINKCOM'], MTCOM + '2']
    env['WINDOWS_INSERT_MANIFEST'] = True

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
        if env['MSVS']['VERSION'] < 8:
            CXXFLAGS += ['/Og','/Gi']

        merge_lists_of_dict(locals(), constants.COMMON_RELEASE)

        CXXFLAGS += ['/W3','/EHs','/Zm600','/MD','/Oi','/Ot','/Ob2','/TP']
        #CXXFLAGS += [ '/O{0}'.format(env['OPTIMIZATIONLEVEL']) , ]
    else :
        merge_lists_of_dict(locals(), constants.COMMON_DEBUG)

        CXXFLAGS += ['/W3','/EHsc','/MDd','/Od']

        if re.match('^[78]', env['MSVS']['VERSION']):
            CXXFLAGS += ['/Z7','/Wp64']
        else :
            CXXFLAGS += ['/Zi']

    names = ['CPPDEFINES','LINKFLAGS','CXXFLAGS']
    attrs = [locals()[n] for n in names]
    env.MergeFlags(dict(zip(names,attrs)), unique=True)

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = "cl"
    env['TOOLINFO']['VERSION'] = env['MSVS']['VERSION']


def manage_options(env, prj, options):
    CXXFLAGS = []
    LINKFLAGS = []
    CPPDEFINES = []
    if env.get('DEBUG') != 'release' :
        env['PDB'] = os.path.join(prj.build_dir, prj.full_name + ".pdb")

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
        if re.match('^[78]', env['MSVS']['VERSION']) :
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

    env.Append( CXXFLAGS   = CXXFLAGS  ,
                LINKFLAGS  = LINKFLAGS ,
                CPPDEFINES = CPPDEFINES
                )

    rc_file = os.path.join(prj.vc_dir, prj.name + '.rc' )
    if os.path.exists( rc_file ):
        res_file = env.RES(rc_file)
        prj.special_source.append(res_file)


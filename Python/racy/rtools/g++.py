# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from racy.renv         import constants
from racy.renv.options import get_option
from racy.rtools       import get_tool
from racy.rutils       import merge_lists_of_dict, is_true

gplusplus = get_tool('SCons.Tool.g++')

exists = gplusplus.exists


def generate(env):
    """Add Builders and construction variables for g++ to an Environment."""

    compiler = get_option("CXX")
    if compiler:
        gplusplus.compilers = [compiler]
    gplusplus.generate(env)
    env.__class__.ManageOption = manage_options
    env.__class__.InstallFileFilter = install_file_filter

    CFLAGS = [
            '-pipe',
            ]
    CXXFLAGS = [
            '-pipe'             ,
            '-Winvalid-pch'     ,
            '-Wunknown-pragmas' ,
            ]

    CPPDEFINES = []
    LINKFLAGS  = []
    
    if get_option('PLATFORM') == constants.LINUX:
        CPPDEFINES += [
                '__linux' ,
                ]
        LINKFLAGS += [
                '-fpic'               ,
                '-fno-stric-aliasing' ,
                '-fno-common'         ,
                ]

    elif get_option('PLATFORM') == constants.MACOSX:
        LINKFLAGS += [
                '-no-cpp-precomp'              ,
                '-headerpad_max_install_names' ,
                ]

        CPPDEFINES += [
                '__MACOSX__' ,
                ]

    if env.get('DEBUG') == 'release' :
        merge_lists_of_dict(locals(), constants.COMMON_RELEASE)
    else :
        merge_lists_of_dict(locals(), constants.COMMON_DEBUG)

        gdb_level = 'gdb3'
        if get_option('PLATFORM') == constants.MACOSX:
            gdb_level = 'gdb2'
        CXXFLAGS  += [ '-O0', '-g' + gdb_level ]
        CFLAGS  += [ '-O0', '-g' + gdb_level ]

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = 'gcc'
    env['TOOLINFO']['VERSION'] = env['CXXVERSION']


    if get_option('ARCH') == '32':
        arch_option = ['-m32']
    elif get_option('ARCH') == '64':
        arch_option = ['-m64']

    CFLAGS    += arch_option
    CXXFLAGS  += arch_option
    LINKFLAGS += arch_option
    
    CPPDEFINES += [ ('__ARCH__' , r'\"{0}\"'.format(get_option('ARCH'))) ]


    names = ['CPPDEFINES','LINKFLAGS','CXXFLAGS', 'CFLAGS']
    attrs = [locals()[n] for n in names]
    env.MergeFlags(dict(zip(names,attrs)), unique=True)


def manage_options(env, prj, options):
    CPPDEFINES = []
    CXXFLAGS   = []
    CFLAGS   = []

    if is_true(options.get('WARNINGSASERRORS', 'no')):
        CXXFLAGS += ['-Werror']

    if 'OPTIMIZATIONLEVEL' in options:
        CXXFLAGS += ['-O{0}'.format(options['OPTIMIZATIONLEVEL'])]
        CFLAGS += ['-O{0}'.format(options['OPTIMIZATIONLEVEL'])]

    if options.get('USEVISIBILITY') == 'racy':
        CPPDEFINES += [
            ('_API_EXPORT'      , r'__attribute__\(\(visibility\(\"default\"\)\)\)'),
            ('_CLASS_API_EXPORT', r'__attribute__\(\(visibility\(\"default\"\)\)\)'),

            ('_API_IMPORT'      , ''),
            ('_CLASS_API_IMPORT', ''),

            ('_TEMPL_API_EXPORT', ''),
            ('_TEMPL_API_IMPORT', r'extern\/\*\*\/\"C++\"'),
                ]
        CXXFLAGS += [
                '-fvisibility=hidden'        ,
                '-fvisibility-inlines-hidden',
                '-fvisibility-ms-compat'     ,
                ]

    env.Append(CPPDEFINES = CPPDEFINES,
               CXXFLAGS   = CXXFLAGS,
               CFLAGS     = CFLAGS
               )

    if get_option('PLATFORM') == constants.MACOSX:
        if prj.is_bundle or prj.is_shared:
            import os
            libname = ''.join(['lib',prj.full_name,'.dylib'])
            if prj.is_bundle:
                install_path = os.path.join('@executable_path', '..',
                                        'Bundles', prj.versioned_name, libname)
            else:
                install_path = os.path.join('@executable_path', '..',
                                        'Libraries', libname)

            
            flags = [
                    '-dynamic',
                    '-nostartfiles',
                    '-install_name', install_path,
                    '-multiply_defined','suppress',
#                    '/usr/lib/dylib1.o', #??
                    ]
            env.Append(SHLINKFLAGS = flags)


def install_file_filter(env, f):
    return hasattr(f,"get_path")



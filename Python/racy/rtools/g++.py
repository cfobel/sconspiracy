# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from racy.renv         import constants
from racy.renv.options import get_option
from racy.rtools       import common, get_tool

gplusplus = get_tool('SCons.Tool.g++')

exists = gplusplus.exists

class GccFlags(common.Flags):
    CXXFLAGS         = [
                        '-pipe',
                        '-Winvalid-pch',
                        '-Wunknown-pragmas',
                       ]
    CXXFLAGS_DEBUG   = ['-O0']

    CFLAGS           = ['-pipe']
    CFLAGS_DEBUG     = ['-O0']

    ARCH_FLAGS         = ['-m${ARCH}']

    WARNINGSASERRORS_FLAGS = ['-Werror']
    OPTIMIZATION_FLAGS     = ['-O${OPTIMIZATIONLEVEL}']

    CXXFLAGS_RACY_VISIBILITY = [
                '-fvisibility=hidden',
                '-fvisibility-inlines-hidden',
                '-fvisibility-ms-compat',
                ]
    CPPDEFINES_RACY_VISIBILITY = [
            ('_API_EXPORT'      , r'__attribute__\(\(visibility\(\"default\"\)\)\)'),
            ('_CLASS_API_EXPORT', r'__attribute__\(\(visibility\(\"default\"\)\)\)'),

            ('_API_IMPORT'      , ''),
            ('_CLASS_API_IMPORT', ''),

            ('_TEMPL_API_EXPORT', ''),
            ('_TEMPL_API_IMPORT', r'extern\/\*\*\/\"C++\"'),
                ]

class GccFlagsOsX(GccFlags):
    CFLAGS_DEBUG  = ['-ggdb2']
    CPPDEFINES    = ['__MACOSX__']
    LINKFLAGS     = [
                     '-no-cpp-precomp',
                     '-headerpad_max_install_names',
                    ]

    LINKFLAGS_BUNDLE = [
            '-dynamic',
            '-nostartfiles',
            '-install_name',
            '@executable_path/../Bundles/${PRJ.versioned_name}/lib${PRJ.full_name}.dylib',
            '-multiply_defined','suppress',
            ]
    LINKFLAGS_SHARED = [
            '-dynamic',
            '-nostartfiles',
            '-install_name',
            '@executable_path/../Libraries/lib${PRJ.full_name}.dylib',
            '-multiply_defined','suppress',
            ]

class GccFlagsLinux(GccFlags):
    CFLAGS_DEBUG  = ['-ggdb3']
    CPPDEFINES    = ['__linux']
    LINKFLAGS     = [
                     '-fpic',
                     '-fno-stric-aliasing',
                     '-fno-common',
                    ]



def generate(env):
    """Add Builders and construction variables for g++ to an Environment."""

    compiler = get_option("CXX")
    if compiler:
        gplusplus.compilers = [compiler]
    gplusplus.generate(env)
    env.__class__.ManageOption = manage_options
    env.__class__.InstallFileFilter = install_file_filter

    if get_option('PLATFORM') == constants.LINUX:
        FlagsGenerator = GccFlagsLinux
    elif get_option('PLATFORM') == constants.MACOSX:
        FlagsGenerator = GccFlagsOsX

    flags = env.__class__.Flags = FlagsGenerator()
    common.merge_flags(env, flags)

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = 'gcc'
    env['TOOLINFO']['VERSION'] = env['CXXVERSION']


def manage_options(env, prj, options):
    common.manage_options(env, prj, options)

def install_file_filter(env, f):
    return hasattr(f,"get_path")



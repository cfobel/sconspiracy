# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
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
                'posix'   ,
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

        CXXFLAGS  += [ '-O0', '-ggdb3' ]

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = 'gcc'
    env['TOOLINFO']['VERSION'] = env['CXXVERSION']


    if get_option('ARCH') == '32':
        CXXFLAGS  += ['-m32']
        LINKFLAGS += ['-m32']
    elif get_option('ARCH') == '64':
        CXXFLAGS  += ['-m64']
        LINKFLAGS += ['-m64']


    names = ['CPPDEFINES','LINKFLAGS','CXXFLAGS']
    attrs = [locals()[n] for n in names]
    env.MergeFlags(dict(zip(names,attrs)), unique=True)


def manage_options(env, prj, options):
    CPPDEFINES = []
    CXXFLAGS   = []
    if 'OPTIMIZATIONLEVEL' in options:
        CXXFLAGS += ['-O{0}'.format(options['OPTIMIZATIONLEVEL'])]

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
               CXXFLAGS   = CXXFLAGS
               )

    if get_option('PLATFORM') == constants.MACOSX:
        if prj.is_bundle:
            import os
            libname = ''.join(['lib',prj.full_name,'.dylib'])
            install_path = os.path.join('Bundles', prj.versioned_name, libname)
            flags = [
                    '-dynamic',
                    '-nostartfiles',
                    '-install_name', install_path,
                    '-multiply_defined','suppress',
                    ]
            env.Append(SHLINKFLAGS = flags)


##             # FIXME : not sure that -pg is a POSIX option.
##             if env['DEBUG'] == 'full' :
##                 env.Append(CXXFLAGS   = '-Wall' )
##                 #==========================================
##                 #
## #                env['CXXFLAGS'] += ' -include mpatrol.h '
## #                env.Append( LIBS = [ 'mpatrol', 'bfd' ] )
##                 #
##                 #==========================================
##             if env['DEBUG'] == 'profil' :
##                 env['CXXFLAGS'] += ' -pg -gfull '
##             elif env['DEBUG'] == 'mpatrol' :
##                 #env['CXXFLAGS'] += ' -DLD_PRELOAD -DUSEDEBUG -DLOGALL -fcheck-memory-usage -impatrol.h'
##                 env['CXXFLAGS'] += ' -Wall '
## #                env['CXXFLAGS'] += ' -DLD_PRELOAD -include mpatrol.h '
## #                env.Append( LIBS = [ 'mpatrol', 'bfd' ] )
##             elif env['DEBUG']=='leaktracer' :
##                 env['CXXFLAGS'] += ' -DLD_PRELOAD '
##                 env.Append( LIBS = [ 'LeakTracer' ] )

## #         '-m32'
## #         '-m64'
## # 
## ### # #Bundle/Shared
## # 
## # 
## # #    if (env['TYPE']=='shared' or env['TYPE']=='bundle') and unittest == 0:
## # #        installPath = ''
## # #        if env['TYPE']=='bundle':
## # #            installPath = '@executable_path/' + 'Bundles/' + myLibFinal.split('_')[0] + '_' + myLibFinal.split('_')[1] + '/lib' + myLibFinal + '.dylib'
## # #            env.Append( LIBS = [ 'dl' ] )
## # #        else:
## # #            installPath = '@executable_path/' + 'Librairies/' + 'lib' + myLibFinal + '.dylib'
## # #        env['LINKFLAGS']   += ' -dynamic -nostartfiles -dynamiclib -install_name ' + installPath
## # #        env['SHLINKFLAGS'] += ' -multiply_defined suppress '
## # #        env['SHLIBSUFFIX']  = '.dylib'
## # 
## #

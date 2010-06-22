# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import string
from racy.rutils import is_true, uniq


class Flags(object):
    """Define a set of compiler options. Each class member not stating with
    '_' must be a list. In each subclass instance, the parent's member will be
    appended to the subclass's one before beeing returned"""

    CXXFLAGS           = []
    CXXFLAGS_RELEASE   = []
    CXXFLAGS_DEBUG     = ['-UNDEBUG']

    CFLAGS             = []
    CFLAGS_RELEASE     = []
    CFLAGS_DEBUG       = []

    CPPDEFINES         = [('__ARCH__' , r'\"${ARCH}\"')]
    CPPDEFINES_RELEASE = ['NDEBUG']
    CPPDEFINES_DEBUG   = ['DEBUG', '_DEBUG']

    LINKFLAGS          = []
    LINKFLAGS_RELEASE  = []
    LINKFLAGS_DEBUG    = []

    CXXFLAGS_BUNDLE           = []
    CXXFLAGS_BUNDLE_RELEASE   = []
    CXXFLAGS_BUNDLE_DEBUG     = []
    LINKFLAGS_BUNDLE          = []
    LINKFLAGS_BUNDLE_RELEASE  = []
    LINKFLAGS_BUNDLE_DEBUG    = []
    CPPDEFINES_BUNDLE         = []
    CPPDEFINES_BUNDLE_RELEASE = []
    CPPDEFINES_BUNDLE_DEBUG   = []

    CXXFLAGS_SHARED           = []
    CXXFLAGS_SHARED_RELEASE   = []
    CXXFLAGS_SHARED_DEBUG     = []
    LINKFLAGS_SHARED          = []
    LINKFLAGS_SHARED_RELEASE  = []
    LINKFLAGS_SHARED_DEBUG    = []
    CPPDEFINES_SHARED         = []
    CPPDEFINES_SHARED_RELEASE = []
    CPPDEFINES_SHARED_DEBUG   = []

    CXXFLAGS_STATIC           = []
    CXXFLAGS_STATIC_RELEASE   = []
    CXXFLAGS_STATIC_DEBUG     = []
    LINKFLAGS_STATIC          = []
    LINKFLAGS_STATIC_RELEASE  = []
    LINKFLAGS_STATIC_DEBUG    = []
    CPPDEFINES_STATIC         = []
    CPPDEFINES_STATIC_RELEASE = []
    CPPDEFINES_STATIC_DEBUG   = []

    CXXFLAGS_EXEC           = []
    CXXFLAGS_EXEC_RELEASE   = []
    CXXFLAGS_EXEC_DEBUG     = []
    LINKFLAGS_EXEC          = []
    LINKFLAGS_EXEC_RELEASE  = []
    LINKFLAGS_EXEC_DEBUG    = []
    CPPDEFINES_EXEC         = []
    CPPDEFINES_EXEC_RELEASE = []
    CPPDEFINES_EXEC_DEBUG   = []

    CXXFLAGS_CONSOLE           = []
    CXXFLAGS_CONSOLE_RELEASE   = []
    CXXFLAGS_CONSOLE_DEBUG     = []
    LINKFLAGS_CONSOLE          = []
    LINKFLAGS_CONSOLE_RELEASE  = []
    LINKFLAGS_CONSOLE_DEBUG    = []
    CPPDEFINES_CONSOLE         = []
    CPPDEFINES_CONSOLE_RELEASE = []
    CPPDEFINES_CONSOLE_DEBUG   = []

    CXXFLAGS_NOCONSOLE           = []
    CXXFLAGS_NOCONSOLE_RELEASE   = []
    CXXFLAGS_NOCONSOLE_DEBUG     = []
    LINKFLAGS_NOCONSOLE          = []
    LINKFLAGS_NOCONSOLE_RELEASE  = []
    LINKFLAGS_NOCONSOLE_DEBUG    = []
    CPPDEFINES_NOCONSOLE         = []
    CPPDEFINES_NOCONSOLE_RELEASE = []
    CPPDEFINES_NOCONSOLE_DEBUG   = []

    WARNINGSASERRORS_FLAGS = []
    OPTIMIZATION_FLAGS     = []

    CPPDEFINES_RACY_VISIBILITY = []
    CXXFLAGS_RACY_VISIBILITY   = []


    def __getattribute__(self, attr):
        if attr[0] in string.ascii_uppercase:
            mro = self.__class__.mro()
            mro.remove(object)
            res = []
            for cls in reversed(mro):
                res += getattr(cls, attr)
            res = uniq(res)

        else:
            res = super(Flags, self).__getattribute__(attr)

        return res

    def format(self, attr, **kwargs):
        def f(s):
            return s.format(**kwargs)
        return map(f, getattr(self, attr))

    def get_flags(self, attr, is_debug):
        res = getattr(self, attr, [])
        if is_debug:
            res += getattr(self, attr+'_DEBUG', [])
        else:
            res += getattr(self, attr+'_RELEASE', [])
        return res



def get_flags(bases):
    return type("CompilerFlags", tuple(bases), {})

def merge_flags(env, flags, names = ['CPPDEFINES', 'LINKFLAGS', 'CXXFLAGS', 'CFLAGS']):
    is_debug = env.get('DEBUG') != 'release'
    for name in names:
        if isinstance(name, tuple):
            name, scons_var = name
        else:
            scons_var = name
        env.AppendUnique(**{scons_var : flags.get_flags(name, is_debug)})

def manage_options(env, prj, options):
    flags = env.__class__.Flags
    env['PRJ'] = prj
    flag_names = []
    if 'OPTIMIZATIONLEVEL' in options:
        env['OPTIMIZATIONLEVEL'] = options['OPTIMIZATIONLEVEL']
        flag_names += [('OPTIMIZATIONLEVEL_FLAGS', 'CXXFLAGS')]

    if is_true(options.get('WARNINGSASERRORS', 'no')):
        flag_names += [('WARNINGSASERRORS_FLAGS', 'CXXFLAGS')]

    if options.get('USEVISIBILITY') == 'racy':
        flag_names += [('CPPDEFINES_RACY_VISIBILITY', 'CPPDEFINES')]
        flag_names += [('CXXFLAGS_RACY_VISIBILITY', 'CXXFLAGS')]

    if prj.is_bundle:
        flag_names += [('CXXFLAGS_BUNDLE',  'SHCXXFLAGS')]
        flag_names += [('LINKFLAGS_BUNDLE', 'SHLINKFLAGS')]
        flag_names += [('CPPDEFINES_BUNDLE', 'CPPDEFINES')]
    elif prj.is_shared:
        flag_names += [('CXXFLAGS_SHARED',  'SHCXXFLAGS')]
        flag_names += [('LINKFLAGS_SHARED', 'SHLINKFLAGS')]
        flag_names += [('CPPDEFINES_SHARED', 'CPPDEFINES')]
    elif prj.is_static:
        flag_names += [('CXXFLAGS_STATIC',  'CXXFLAGS')]
        flag_names += [('LINKFLAGS_STATIC', 'LINKFLAGS')]
        flag_names += [('CPPDEFINES_STATIC', 'CPPDEFINES')]
    elif prj.is_exec:
        flag_names += [('CXXFLAGS_EXEC',    'CXXFLAGS')]
        flag_names += [('LINKFLAGS_EXEC',   'LINKFLAGS')]
        flag_names += [('CPPDEFINES_EXEC',   'CPPDEFINES')]

        if is_true( options.get('CONSOLE') ):
            flag_names += [('CXXFLAGS_CONSOLE',    'CXXFLAGS')]
            flag_names += [('LINKFLAGS_CONSOLE',   'LINKFLAGS')]
            flag_names += [('CPPDEFINES_CONSOLE',   'CPPDEFINES')]
        else:
            flag_names += [('CXXFLAGS_NOCONSOLE',    'CXXFLAGS')]
            flag_names += [('LINKFLAGS_NOCONSOLE',   'LINKFLAGS')]
            flag_names += [('CPPDEFINES_NOCONSOLE',   'CPPDEFINES')]



    merge_flags(env, flags, flag_names)


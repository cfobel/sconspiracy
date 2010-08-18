# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


__all__ = ['dirs']


from options import Paths
dirs = Paths()
del Paths

class simple_memoize(object):
    """Simple Memoization decorator. avoid importing racy.rutils"""
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__  = func.__doc__
        self.has_res  = False
    def __call__(self):
        try:
            return self.res
        except:
            self.res = self.func()
            return self.res


@simple_memoize
def system():
    """Returns the system (linux, darwin, windows)."""
    import platform
    return platform.system().lower()

@simple_memoize
def is_linux():
    return system() == "linux"
@simple_memoize
def is_darwin():
    return system() == "darwin" 
@simple_memoize
def is_windows():
    return system() == "windows"

@simple_memoize
def platform():
    """Returns the platform racy' name."""
    from racy.renv import constants

    return constants.SYSTEMS_RACY_NAMES[system()]

@simple_memoize
def architecture():
    """Returns the architecture of the python interpreter, used for default
    compilation architecture"""
    import platform
    return platform.architecture()[0][:-3]

LD_VAR = {
        "linux"  : 'LD_LIBRARY_PATH'  ,
        "darwin" : 'DYLD_LIBRARY_PATH',
        "windows": 'PATH'             ,
        }[system()]

@simple_memoize
def toolpath():
    import racy.rtools
    return racy.rtools.__path__


def get_scons_env(*args, **kw):
    env = environment.Environment(*args, **kw)

    return env


from target import TargetDB
TARGETS = TargetDB()
ARGUMENTS = {}

def register_args(args):
    ARGUMENTS.update(args)

def register_targets(targets):
    from target import Target
    targets_obj = [Target(target) for target in targets]
    for target in targets_obj:
        TARGETS[target.name] = target


def register_env():
    import environment

    from SCons.Script import ARGUMENTS, COMMAND_LINE_TARGETS

    register_args(ARGUMENTS)
    register_targets(COMMAND_LINE_TARGETS)


def check_env():
    import racy.renv.configs.commandline
    racy.renv.configs.commandline.check_opts(ARGUMENTS)
    for opt, val in ARGUMENTS.items():
        racy.renv.configs.allowedvalues.check_value_with_msg(
            opt,
            val, 
            'commandline argument'
            )
    for target in TARGETS.values():
        racy.renv.configs.commandline.check_prj_opts(target.opts)
        racy.renv.configs.allowedvalues.check_dict_with_msg(
            target.opts, "commandline project's argument"
            )


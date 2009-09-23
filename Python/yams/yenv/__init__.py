# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


__all__ = ['dirs']


from options import Paths
dirs = Paths()
del Paths



def system():
    """Returns the system (linux, darwin, windows)."""
    import platform
    return platform.system().lower()

def platform():
    """Returns the platform yams' name."""
    from yams.yenv import constants

    return constants.SYSTEMS_YAMS_NAMES[system()]

def architecture():
    """Returns the architecture of the python interpreter, used for default
    compilation architecture"""
    import platform
    return platform.architecture()[0][:-3]


def toolpath():
    import yams.ytools
    return yams.ytools.__path__


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
    import yams.yenv.configs.commandline
    yams.yenv.configs.commandline.check_opts(ARGUMENTS)
    for opt, val in ARGUMENTS.items():
        yams.yenv.configs.allowedvalues.check_value_with_msg(
            opt,
            val, 
            'commandline argument'
            )
    for target in TARGETS.values():
        yams.yenv.configs.commandline.check_prj_opts(target.opts)
        yams.yenv.configs.allowedvalues.check_dict_with_msg(
            target.opts, "commandline project's argument"
            )


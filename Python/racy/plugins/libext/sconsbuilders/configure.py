# -*- coding: UTF8 -*-

import os
import SCons


from subprocessbuilder import SubProcessBuilder, SubProcessString
from command import CommandArgs

def find_configure_path(_dir):
    path = None
    for root, dirs, files in os.walk(_dir):
        if "configure" in files:
            path = root
            break
    return path

def Configure(target, source, env):
    assert len(source) == 1

    configure_dir = find_configure_path(source[0].get_abspath())

    command = 'configure'

    args = CommandArgs(target, source, env)

    pwd = configure_dir

    returncode = SubProcessBuilder(
            target, source, env, command, args, pwd,
            path = configure_dir
            )

    return returncode


def ConfigureString(target, source, env):
    """ Information string for Configure """
    prefix = SubProcessString(target, source, env)
    args = CommandArgs(target, source, env)
    return prefix + env.subst('configure '+str(args))



def generate(env):
    action  = SCons.Action.Action(Configure, ConfigureString)
    builder = env.Builder(
            action=action           ,
            #emitter=ConfigureEmitter    ,
            target_factory = env.Value,
            source_factory = env.Dir,
            )

    env.Append(BUILDERS = {'Configure' : builder})



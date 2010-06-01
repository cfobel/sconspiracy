# -*- coding: UTF8 -*-

import os
import SCons


from subprocessbuilder import SubProcessBuilder, SubProcessString

def CommandArgs(target, source, env):
    args = ['-i', source[0].get_abspath()]
    options = env.get('OPTIONS',['-p1'])
    options = map(env.subst, options)
    args.extend(options)
    return args


def Command(target, source, env):
    assert len(source) == 1

    pwd = os.path.abspath(target[0].value)

    command = env.subst('${COMMAND}')

    args = CommandArgs(target, source, env)

    returncode = SubProcessBuilder(target, source, env, command, args, pwd)

    return returncode


def CommandString(target, source, env):
    """ Information string for Command """

    prefix = SubProcessString(target, source, env)
    args = CommandArgs(target, source, env)

    return prefix + env.subst('${COMMAND} '+str(args))




def generate(env):
    action  = SCons.Action.Action(Command, CommandString)
    builder = env.Builder(
            action=action             ,
            target_factory = env.Value,
            source_factory = env.Dir,
            )

    env.Append(BUILDERS = {'Command' : builder})



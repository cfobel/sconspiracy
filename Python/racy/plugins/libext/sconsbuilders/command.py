# -*- coding: UTF8 -*-

import os
import SCons


from subprocessbuilder import SubProcessBuilder, SubProcessString

def CommandArgs(target, source, env):
    args = []
    args.extend([t.value for t in target])
    args.extend(env.get('OPTIONS',[]))
    args = map(env.subst, args)
    return args


def Command(target, source, env):
    """Builder that execute an arbitrary command in the source dir The command
    is the first item of target
    """
    assert len(source) == 1
    assert len(target) >= 1

    pwd = os.path.abspath(source[0].get_abspath())

    #command = env.subst('${COMMAND}')

    args = CommandArgs(target, source, env)

    command = args[0]

    returncode = SubProcessBuilder(target, source, env, command, args, pwd, [pwd])

    return returncode


def CommandString(target, source, env):
    """ Information string for Command """

    prefix = SubProcessString(target, source, env)
    args = CommandArgs(target, source, env)

    return prefix + env.subst(str(args))




def generate(env):
    action  = SCons.Action.Action(Command, CommandString)
    builder = env.Builder(
            action=action             ,
            target_factory = env.Value,
            source_factory = env.Dir,
            )

    env.Append(BUILDERS = {'Command' : builder})



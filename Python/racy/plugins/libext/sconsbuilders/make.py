# -*- coding: UTF8 -*-

import os
import SCons


from subprocessbuilder import SubProcessBuilder, SubProcessString

def find_make_path(_dir):
    path = None
    for root, dirs, files in os.walk(_dir):
        if "Makefile" in files:
            path = root
            break
    return path

def guess_make_cmd():
    import racy.renv as renv
    if renv.is_windows():
        return "nmake"
    else:
        return "make"

def MakeArgs(target, source, env):
    args = []
    args.extend([t.value for t in target])
    options = env.get('OPTIONS',[])
    options = map(env.subst, options)
    args.extend(options)
    return args

def Make(target, source, env):
    assert len(source) == 1

    pwd = find_make_path(source[0].get_abspath())

    command = env.subst('${MAKECOM}')

    args = MakeArgs(target, source, env)

    returncode = SubProcessBuilder(target, source, env, command, args, pwd)

    return returncode


def MakeString(target, source, env):
    """ Information string for Make """
    prefix = SubProcessString(target, source, env)
    args = MakeArgs(target, source, env)
    return prefix + env.subst('${MAKECOM} '+str(args))





def generate(env):
    action  = SCons.Action.Action(Make, MakeString)
    builder = env.Builder(
            action=action           ,
            #emitter=MakeEmitter    ,
            target_factory = env.Value,
            source_factory = env.Dir,
            )

    env['MAKECOM'] = guess_make_cmd()

    env.Append(BUILDERS = {'Make' : builder})



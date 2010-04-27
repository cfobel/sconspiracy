# -*- coding: UTF8 -*-

import os
import SCons

from subprocessbuilder import SubProcessBuilder

def find_make_path(_dir):
    path = None
    for root, dirs, files in os.walk(_dir):
        if "Makefile" in files:
            path = root
            break
    return path


def Make(target, source, env):
    assert len(source) == 1

    make_dir = find_make_path(source[0].get_abspath())

    command = 'make'
    args = []
    args.extend([t.value for t in target])
    args.append(env.subst('${OPTIONS}'))
    pwd = make_dir

    returncode = SubProcessBuilder(target, source, env, command, args, pwd)

    return returncode


def MakeString(target, source, env):
    """ Information string for Make """
    return env.subst('make: $TARGET ${OPTIONS}') #% os.path.basename (str (source[0]))




def generate(env):
    action  = SCons.Action.Action(Make, MakeString)
    builder = env.Builder(
            action=action           ,
            #emitter=MakeEmitter    ,
            target_factory = env.Value,
            source_factory = env.Dir,
            )

    env.Append(BUILDERS = {'Make' : builder})



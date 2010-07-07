# -*- coding: UTF8 -*-

import os
import SCons.Node
import shutil


def CopyArgs(target, source, env):
    args = []
    args.extend(env.get('ARGS',[]))
    args = map(env.subst, args)
    return args


def Copy(target, source, env):

    args = CopyArgs(target, source, env)

    dst = args[-1]
    for src in args[:-1]:
        env.Execute(SCons.Script.Copy(dst, src))

    for t in target:
        env.Execute(SCons.Script.Touch(t))

    return None

def CopyString(target, source, env):
    """ Information string for Copy """
    args = CopyArgs(target, source, env)
    dst = args[-1]
    src = args[:-1]
    s = '[${CURRENT_PROJECT}]: copying '+' '.join(src)+' to '+dst
    return env.subst(s)


def generate(env):
    action  = SCons.Action.Action(Copy, CopyString)
    builder = env.Builder(
            action = action,
            target_factory = env.File,
            )

    env.Append(BUILDERS = {'CopyFile' : builder})



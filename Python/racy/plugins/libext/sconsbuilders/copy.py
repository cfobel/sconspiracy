# -*- coding: UTF8 -*-

import os
import SCons.Node
import shutil

import utils

def CopyArgs(target, source, env):
    args = []
    args.extend(env.get('ARGS',[]))
    args = map(env.subst, args)
    return args[:-1], args[-1]


def Copy(target, source, env):

    src, dst = CopyArgs(target, source, env)

    if len(src) == len(dst) and os.path.exists(dst):
        env.Execute(SCons.Script.Delete(dst)) 

    for s in src:
        env.Execute(SCons.Script.Copy(dst, s))

    assert len(target) == 1
    for t in target:
        utils.write_marker(env, t)

    return None

def CopyString(target, source, env):
    """ Information string for Copy """
    src, dst = CopyArgs(target, source, env)
    s = '[${CURRENT_PROJECT}]: copying '+' '.join(src)+' to '+dst
    return env.subst(s)


def generate(env):
    action  = SCons.Action.Action(Copy, CopyString)
    builder = env.Builder(
            action = action,
            target_factory = env.File,
            )

    env.Append(BUILDERS = {'LibextCopyFile' : builder})



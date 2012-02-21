# -*- coding: UTF8 -*-

import os
import SCons.Node

import utils

def MkdirArgs(target, source, env):
    args = []
    args.extend(env.get('ARGS',[]))
    args = map(env.subst, args)
    return args


@utils.marker_decorator
def Mkdir(target, source, env):

    for d in MkdirArgs(target, source, env):
        env.Execute(SCons.Script.Mkdir(env.Dir(d)))

    return None

def MkdirString(target, source, env):
    """ Information string for Mkdir """
    args = MkdirArgs(target, source, env)

    return env.subst('[${CURRENT_PROJECT}]: mkdir ') + ' '.join(args)


def generate(env):
    action  = SCons.Action.Action(Mkdir, MkdirString)
    builder = env.Builder( action = action )

    env.Append(BUILDERS = {'Mkdir' : builder})



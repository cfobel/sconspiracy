# -*- coding: UTF8 -*-

import os
import SCons.Node
import shutil

import utils

def DeleteArgs(target, source, env):
    args = []
    args.extend(env.get('ARGS',[]))
    return env.subst(args)


@utils.marker_decorator
def Delete(target, source, env):
    files = DeleteArgs(target, source, env)

    not_found = [ f for f in files if not os.path.exists(f)]
    if not_found:
        msg = '{0} does not exists'
        raise SCons.Errors.StopError( msg.format(not_found) )

    map(os.unlink, files)

    return None

def DeleteString(target, source, env):
    """ Information string for Delete """
    files = DeleteArgs(target, source, env)
    s = '[${CURRENT_PROJECT}]: Delete '+' '.join(files)
    return env.subst(s)


def generate(env):
    action  = SCons.Action.Action(Delete, DeleteString)
    builder = env.Builder(
            action = action,
            target_factory = env.File,
            )

    env.Append(BUILDERS = {'LibextDelete' : builder})



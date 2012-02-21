# -*- coding: UTF8 -*-

import os
import SCons

import command


def Patch(target, source, env):
    assert len(source) == 1

    patch_pwd = os.path.abspath(source[0].get_abspath())

    return command.Command( target, source, env,
                            pwd = patch_pwd,
                            command = env['PATCHCOM'],
                            lookup_path = [] )


def PatchString(target, source, env):
    return 'patch ' + command.CommandString(target, source, env)


def generate(env):
    action  = SCons.Action.Action(Patch, PatchString)
    builder = env.Builder(
            action=action           ,
            target_factory = env.File,
            source_factory = env.Dir,
            )

    env['PATCHCOM'] = 'patch'

    env.Append(BUILDERS = {'Patch' : builder})



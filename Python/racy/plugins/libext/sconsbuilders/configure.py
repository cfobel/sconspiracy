# -*- coding: UTF8 -*-

import os
import SCons

import command

class ConfigureNotFound(SCons.Warnings.Warning):
    pass

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
    if not configure_dir:
        msg = "Could not find configure script in {0} dir."
        raise SCons.Errors.StopError(
            ConfigureNotFound, msg.format(source[0].get_abspath()) )


    return command.Command( target, source, env,
                            command = 'configure',
                            pwd = configure_dir,
                            lookup_path = [configure_dir] )


def ConfigureString(target, source, env):
    return 'configure ' + command.CommandString(target, source, env)


def generate(env):
    action  = SCons.Action.Action(Configure, ConfigureString)
    builder = env.Builder(
            action=action             ,
            #emitter=ConfigureEmitter  ,
            target_factory = env.File ,
            source_factory = env.Dir  ,
            )
    env.Append(BUILDERS = {'Configure' : builder})



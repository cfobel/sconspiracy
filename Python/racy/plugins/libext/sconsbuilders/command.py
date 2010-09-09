# -*- coding: UTF8 -*-

import os
import SCons

import utils

from subprocessbuilder import SubProcessBuilder, SubProcessString

def CommandArgs(target, source, env, command=None):
    args = []
    command = env.get('COMMAND', command)
    if command:
        args.append(command)
    args.extend(env.get('ARGS',[]))
    args = map(env.subst, args)
    return args


def Command(target, source, env, **kwargs):
    """Builder that execute an arbitrary command in the source dir.
    The target file is a marker to help SCons to know about the command
    execution state(failed, succes, last execution)
    """
    assert len(source) == 1
    assert len(target) == 1

    command     = kwargs.get('command',None)
    pwd         = kwargs.get('pwd',None)
    lookup_path = kwargs.get('lookup_path',None)

    try:
        if pwd is None:
            pwd = os.path.abspath(source[0].get_abspath())

        args = CommandArgs(target, source, env, command)

        command = args[0]
        args = args[1:]

        if lookup_path is None:
            lookup_path = [pwd]

        returncode, stdout, stderr = SubProcessBuilder(env, command, args,
                pwd, lookup_path)

        assert len(target) == 1
        marker_file = target[0]

        marker_extra = {
                'stdout' : stdout,
                'stderr' : stderr,
                }
        if returncode:
            marker_extra['fileprefix'] = "error.{0}.".format(returncode)

    except Exception, e:
        marker_extra['fileprefix'] = "error."
        raise e

    finally:
        utils.write_marker(env, marker_file, **marker_extra)

    return returncode


def CommandString(target, source, env):
    """ Information string for Command """
    args = CommandArgs(target, source, env)
    return ' '.join([SubProcessString(target, source, env) , ' '.join(args)])



def generate(env):
    action  = SCons.Action.Action(Command, CommandString)
    builder = env.Builder(
            action = action          ,
            target_factory = env.File,
            source_factory = env.Dir ,
            )

    env.Append(BUILDERS = {'SysCommand' : builder})



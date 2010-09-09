# -*- coding: UTF8 -*-

import os
import subprocess
import SCons

from racy.rutils import is_iterable

###############################################################################

class CommandNotFound(SCons.Warnings.Warning):
    pass

###############################################################################

def SubProcessBuilder(env, command, args, pwd, path = []):

    if is_iterable(path):
        path = os.pathsep.join(path)
    path = os.pathsep.join([path, os.environ['PATH'], env['ENV']['PATH']])

    cmd = env.WhereIs(command, path=path)

    if cmd is None:
        msg = ("command '{0}' not found: you may need to complete your PATH")
        raise SCons.Errors.StopError(
            CommandNotFound, msg.format(command) )

    cmd = [cmd] + args
    cmd = filter(lambda x:x, cmd)

    environment = dict((k,str(v)) for k,v in env['ENV'].items())

    popen_kwargs = {
            'stdout' : subprocess.PIPE,
            'stderr' : subprocess.PIPE,
            }

    process = subprocess.Popen(
                cmd,
                cwd = pwd,
                env = environment,
                **popen_kwargs
                )

    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


###############################################################################

def SubProcessString(target, source, env):
    return env.subst('[${CURRENT_PROJECT}]:')




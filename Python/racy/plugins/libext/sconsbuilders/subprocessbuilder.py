# -*- coding: UTF8 -*-

import os
import subprocess

from racy.rutils import is_iterable

def SubProcessBuilder(env, command, args, pwd, path = [], stdout = 'STDOUT'):

    if is_iterable(path):
        path = os.pathsep.join(path)
    path = os.pathsep.join([path, os.environ['PATH'], env['ENV']['PATH']])

    cmd = [ env.WhereIs(command, path=path) ]

    cmd.extend(args)

    environment = dict((k,str(v)) for k,v in env['ENV'].items())

    cmd = filter(lambda x:x, cmd)


    stdout_is_file = False
    kwargs = {}
    if stdout is None:
        kwargs['stdout'] = subprocess.PIPE
    elif stdout is not None and stdout is not 'STDOUT':
        stdout_is_file = True
        #exceptions catched by scons
        kwargs['stdout'] = open(env.subst(stdout), 'w')

    process = subprocess.Popen(
                cmd,
                cwd = pwd,
                env = environment,
                **kwargs
                )

    process.communicate()

    if stdout_is_file:
        kwargs['stdout'].close()

    return process.returncode


def SubProcessString(target, source, env):
    return env.subst('[${CURRENT_PROJECT}]:')




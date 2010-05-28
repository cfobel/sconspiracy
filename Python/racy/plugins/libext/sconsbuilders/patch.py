# -*- coding: UTF8 -*-

import os
import SCons


from subprocessbuilder import SubProcessBuilder, SubProcessString

def PatchArgs(target, source, env):
    args = ['-i', source[0].get_abspath()]
    options = env.get('OPTIONS',['-p1'])
    options = map(env.subst, options)
    args.extend(options)
    return args


def Patch(target, source, env):
    assert len(source) == 1

    pwd = os.path.abspath(target[0].value)

    command = env.subst('${PATCHCOM}')

    args = PatchArgs(target, source, env)

    returncode = SubProcessBuilder(target, source, env, command, args, pwd)

    return returncode


def PatchString(target, source, env):
    """ Information string for Patch """

    prefix = SubProcessString(target, source, env)
    args = PatchArgs(target, source, env)

    return prefix + env.subst('${PATCHCOM} '+str(args))




def generate(env):
    action  = SCons.Action.Action(Patch, PatchString)
    builder = env.Builder(
            action=action           ,
            #emitter=PatchEmitter    ,
            target_factory = env.Value,
            source_factory = env.File,
            )

    env['PATCHCOM'] = 'patch'

    env.Append(BUILDERS = {'Patch' : builder})



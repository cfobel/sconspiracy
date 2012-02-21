# -*- coding: UTF8 -*-

import os
import SCons


import command

def find_make_path(env, _dir):
    path = None
    makefile = env['MAKEFILE']
    for root, dirs, files in os.walk(_dir):
        if makefile in files:
            path = root
            break
    return path

def guess_make_cmd():
    import racy.renv as renv
    if renv.is_windows():
        return "nmake"
    else:
        return "make"

#def MakeEmitter(target, source, env):
    #return [env.Value(env.subst('${MAKECOM}'))] + target, source

def Make(target, source, env):
    assert len(source) == 1

    make_pwd = find_make_path(env, source[0].get_abspath())

    return command.Command( target, source, env,
                            pwd = make_pwd,
                            command = env['MAKECOM'],
                            lookup_path = [] )


def MakeString(target, source, env):
    """ Information string for Make """
    return command.CommandString(target, source, env)





def generate(env):
    action  = SCons.Action.Action(Make, MakeString)
    builder = env.Builder(
            action=action             ,
            #emitter=MakeEmitter       ,
            target_factory = env.File,
            source_factory = env.Dir  ,
            )

    env['MAKECOM'] = guess_make_cmd()
    env['MAKEFILE'] = 'Makefile'

    env.Append(BUILDERS = {'Make' : builder})



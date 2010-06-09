# -*- coding: UTF8 -*-

import os
import SCons

import command
from subprocessbuilder import SubProcessBuilder, SubProcessString

def find_cmake_path(_dir):
    path = None
    for root, dirs, files in os.walk(_dir):
        if "CMakeLists.txt" in files:
            path = root
            break
    return path


def CMakeEmitter(target, source, env):
    #target = [ env.Dir(os.path.join(source[0].get_abspath(), '..','build') ) ]
    for node in target:
        env.Clean(node, node)
    env.Clean(target[0], env.Dir(env['CMAKE_BUILD_PATH']))
    return target, source



def CMake(target, source, env):
    assert len(source) == 1

    cmake_prj_path   = find_cmake_path(env.subst(source[0].get_abspath()))
    cmake_build_path = env.Dir(env['CMAKE_BUILD_PATH']).get_abspath()
    ARGS = env.get('ARGS',[])
    ARGS.append(cmake_prj_path)
    env['ARGS'] = ARGS

    wasdir = os.path.isdir(cmake_build_path)
    if not wasdir:
        env.Execute(SCons.Script.Mkdir(cmake_build_path))

    try:
        returncode = command.Command( target, source, env,
                                  command = 'cmake',
                                  pwd = cmake_build_path,
                                  lookup_path = [] )
    except Exception, e:
        if not wasdir:
            env.Execute(SCons.Script.Delete(cmake_build_path))
        raise e

    if returncode and not wasdir:
        env.Execute(SCons.Script.Delete(cmake_build_path))

    return returncode


def CMakeString(target, source, env):
    return 'cmake ' + command.CommandString(target, source, env)



def generate(env):
    action  = SCons.Action.Action(CMake, CMakeString)
    builder = env.Builder(
            action=action           ,
            emitter=CMakeEmitter    ,
            target_factory = env.File,
            source_factory = env.Dir,
            )

    env.Append(BUILDERS = {'CMake' : builder})



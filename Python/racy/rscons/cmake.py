# -*- coding: UTF8 -*-

import os
import SCons

from subprocessbuilder import SubProcessBuilder

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
    return target, source



def CMake(target, source, env):
    assert len(source) == 1

    cmake_prj_path   = find_cmake_path(source[0].get_abspath())
    cmake_build_path = target[0].get_abspath()

    wasdir = target[0].isdir()
    if not wasdir:
        env.Execute(SCons.Script.Mkdir(cmake_build_path))

    command = 'cmake'
    args = []
    args.extend(env.subst('${OPTIONS}').split())
    args.append(cmake_prj_path)
    pwd = cmake_build_path

    try:
        returncode = SubProcessBuilder(target, source, env, command, args, pwd)
    except:
        print "wasdir "  + str(wasdir)
        if not wasdir:
            env.Execute(SCons.Script.Delete(cmake_build_path))


    return returncode


def CMakeString(target, source, env):
    """ Information string for CMake """
    return env.subst('Cmake: $TARGET ${OPTIONS}') #% os.path.basename (str (source[0]))




def generate(env):
    action  = SCons.Action.Action(CMake, CMakeString)
    builder = env.Builder(
            action=action           ,
            emitter=CMakeEmitter    ,
            target_factory = env.Dir,
            source_factory = env.Dir,
            )

    env.Append(BUILDERS = {'CMake' : builder})



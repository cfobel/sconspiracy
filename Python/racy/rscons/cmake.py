# -*- coding: UTF8 -*-

import os
import subprocess

import SCons.Node
import SCons.Script


def find_cmake_path(dir):
    path = None
    for root, dirs, files in os.walk(dir):
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

    env.Execute(SCons.Script.Mkdir(cmake_build_path))

    cmd = [  env.WhereIs('cmake', path=os.environ['PATH']) ]

    cmd.append(cmake_prj_path)
    cmd.append(env.subst('${OPTIONS}'))

    environment = {}
    for k,v in env['ENV'].items():
        environment[k] = str(v)

    cmake = subprocess.Popen(cmd,
                             cwd = cmake_build_path,
                             env = environment
                            )

    cmake.communicate()

    return cmake.returncode


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



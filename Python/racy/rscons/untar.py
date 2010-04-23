# -*- coding: UTF8 -*-

import os
#import SCons.Action
import SCons.Node

def UnTarEmitter(target, source, env):
    assert len(target) <= 1 # Until multiple target is managed
    newTarget = []

    root = ''
    if target:
        root = target[0].get_abspath()

    for s in source:
        extract_path = os.path.basename(s.get_abspath())
        extract_path = os.path.splitext(extract_path)[0]
        extract_path = os.path.join(root, extract_path)
        newTarget.append(env.Dir(extract_path))

    for node in newTarget:
        env.Clean(node, node)

    return newTarget, source


def UnTar(target, source, env):
    # Code to build "target" from "source" here
    import tarfile
    sourceTar = tarfile.open(source[0].get_abspath(),'r')
    sourceTar.extractall(path=target[0].get_abspath())
    sourceTar.close()
    return None

def UnTarString(target, source, env):
    """ Information string for UnTar """
    return 'Extracting %s' % os.path.basename (str (source[0]))


def generate(env):
    action  = SCons.Action.Action(UnTar, UnTarString)
    builder = env.Builder(
            action=action,
            src_suffix='.tar.gz',
            emitter=UnTarEmitter
            )

    env.Append(BUILDERS = {'UnTar' : builder})



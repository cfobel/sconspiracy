# -*- coding: UTF8 -*-

import os
#import SCons.Action
import SCons.Node

def UnZipEmitter(target, source, env):
    assert len(target) <= 1 # Until multiple target is managed

    for node in target:
        env.Clean(node, node)

    return target, source


def UnZip(target, source, env):
    # Code to build "target" from "source" here
    import zipfile
    sourceZip = zipfile.ZipFile(source[0].get_abspath(),'r')
    sourceZip.extractall(path=target[0].get_abspath())
    sourceZip.close()
    return None

def UnZipString(target, source, env):
    """ Information string for UnZip """
    return 'Extracting %s' % os.path.basename (str (source[0]))


def generate(env):
    action  = SCons.Action.Action(UnZip, UnZipString)
    builder = env.Builder(
            action         = action,
            emitter        = UnZipEmitter,
            target_factory = env.Dir,
            )

    env.Append(BUILDERS = {'UnZip' : builder})



# -*- coding: UTF8 -*-

import os
import SCons.Node

def write(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

def WriteArgs(target, source, env):
    files = []
    files.extend(env.get('FILES',[]))
    files = map(env.subst, files)
    contents = []
    contents.extend(env.get('CONTENTS',[]))
    contents = map(env.subst, contents)
    return files, contents

def Write(target, source, env):
    # we don't use target and source as usual : we may apply several times this
    # builder on the same source/target (or the source may be the target), 
    # that's not possible for scons
    files, contents = WriteArgs(target, source, env)

    for f, c in zip(files, contents):
        write(c, f)

    for t in target:
        env.Execute(SCons.Script.Touch(t))

    return None

def WriteString(target, source, env):
    """ Information string for Write """
    files = WriteArgs(target, source, env)[0]
    files = ' '.join(files)
    return ' '.join(['Writing file(s)', files])


def generate(env):
    action  = SCons.Action.Action(Write, WriteString)
    builder = env.Builder( action = action )

    env.Append(BUILDERS = {'Write' : builder})



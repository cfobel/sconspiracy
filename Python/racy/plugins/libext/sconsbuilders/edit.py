# -*- coding: UTF8 -*-

# imported for disponibility in builder's expressions
import re
import os

import SCons.Node
import StringIO
import functools

import utils

def apply_expression(expr, source, target, mode='eval'):
    # inspired from http://code.activestate.com/recipes/437932/
    codeobj = compile(expr, 'EditBuilder', mode)
    output = StringIO.StringIO()

    def exec_mode(_codeobj, _globals, _locals):
        exec(_codeobj, _globals, _locals)
        return _locals['line']

    def eval_mode(_codeobj, _globals, _locals):
        return eval(_codeobj, _globals, _locals)

    with open(source, 'rb') as f:
        input = enumerate(f)

        write = output.write
        locals_vars = {}
        if mode == 'exec':
            callback = exec_mode
        else:
            callback = eval_mode

        for numz, line in input:
            locals_vars.update({
                'line'  : line[:-1],
                'num'   : numz + 1,
                'words' : [w for w in line.strip().split(' ') if w],
                })
            result = callback(codeobj, {'os':os, 're':re}, locals_vars)
            if result is None or result is False:
                continue
            elif isinstance(result, list) or isinstance(result, tuple):
                result = ' '.join(map(str, result))
            else:
                result = str(result)
            write(result)
            if not result.endswith('\n'):
                write('\n')

    output.seek(0)
    with open(target, 'wb') as f:
        f.writelines(output.readlines())


def EditArgs(target, source, env):
    files = []
    files.extend(env.get('FILES',[]))
    files = map(env.subst, files)
    expr = []
    expr.extend(env.get('EXPR',[]))
    expr = map(functools.partial(env.subst, raw=1), expr)
    mode = env.get('MODE','eval')
    return files, expr, mode

def Edit(target, source, env):
    # we don't use target and source as usual : we may apply several times this
    # builder on the same source/target (or the source may be the target), 
    # that's not possible for scons
    

    files, expr, mode = EditArgs(target, source, env)

    for f in files:
        for e in expr:
            apply_expression(e, f, f, mode)

    assert len(target) == 1
    for t in target:
        utils.write_marker(env, t)

    return None

def EditString(target, source, env):
    """ Information string for Edit """
    files, expr, mode = EditArgs(target, source, env)
    files = ' '.join(files)
    expr = ' '.join(expr)
    s = ' '.join(['Editing file(s)', files, '<<', expr, '>>'])
    return env.subst('[${CURRENT_PROJECT}]: ') + s


def generate(env):
    action  = SCons.Action.Action(Edit, EditString)
    builder = env.Builder( action = action )

    env.Append(BUILDERS = {'Edit' : builder})




import SCons
import pprint
import os

from hashlib import md5



def write(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

###############################################################################

markers = {}

def marker(command, prj, options):
    res      = '{dir}/{file}'
    cmd      = '{cmd}_{prj}_{hash}'
    info     = '{prj}\n\n{cmd} {opt}'
    options  = ' '.join(options)
    digest   = md5(options).hexdigest()
    filename = cmd.format(
                 cmd  = command,
                 prj  = prj,
                 hash = digest,
                 )
    res = res.format(
            dir  = '${BUILD_DIR}/',
            file  = filename,
            )
    markers[filename] = info.format(
            cmd  = command,
            prj  = prj,
            opt  = options,
            )
    return res

###############################################################################

def write_marker(env, filename, fileprefix=None, **kwargs):
    separator = '='*79 + '\n'
    content = [ 
            '{info}',
            '{sep}ENV:\n{sep}{env}',
            ]
    content.extend([''.join(['{sep}',k,':\n{sep}{',k,'}']) for k in kwargs])
    content = '\n\n'.join(content)

    for k,v in kwargs.items():
        if not v:
            kwargs[k] = '<empty>'

    info = markers.get(filename.name, '<No informations available>')
    content = content.format(
            info = env.subst(info, raw=1),
            env  = pprint.pformat(env.Dictionary()),
            sep  = separator,
            **kwargs
            )
    filepath = filename.get_abspath()

    if fileprefix:
        filedir = os.path.dirname(filepath)
        filebase = os.path.basename(filepath)
        filepath = os.path.join(filedir, fileprefix + filebase)

    write(content, filepath)


def marker_decorator(func):
    def decorated(target, source, env, **kwargs):
        assert len(target) == 1
        marker_file  = target[0]
        marker_extra = {}
        if 'marker_extra' in func.func_code.co_varnames:
            kwargs['marker_extra'] = marker_extra
        try:
            return func(target, source, env, **kwargs)
        except Exception, e:
            marker_extra['fileprefix'] = 'error.'
            marker_extra['exception']  = str(e)
            raise e
        finally:
            write_marker(env, marker_file, **marker_extra)

    return decorated

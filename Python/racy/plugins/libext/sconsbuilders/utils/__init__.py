
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
        filepath = os.path.join(filedir, fileprefix + filepath)

    write(content, filepath)


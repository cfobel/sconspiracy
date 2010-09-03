
import SCons
import pprint

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

def write_marker(env, filename):
    content = '{info}\n\n---ENV---\n{env}\n---------'
    info = markers.get(filename.name, 'Unknown ??')
    content = content.format(
            info = env.subst(info, raw=1),
            env  = pprint.pformat(env.Dictionary())
            )
    write(content, filename.get_abspath())
    #env.Execute(SCons.Script.Touch(filename))


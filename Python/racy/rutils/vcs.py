import os
import subprocess

import racy

def find_vcs_dirs(path, vcs=['.hg']):
    found_dirs = []
    for root, dirs, files in os.walk(path, topdown=True):
        vcs_dot_dirs = set(dirs).intersection(vcs)
        found_dirs.extend(map(lambda p:os.path.join(root,p), vcs_dot_dirs))
        if vcs_dot_dirs:
            dirs[:] = []
        #map(dirs.remove,vcs_dot_dirs)

    return found_dirs

def get_hg_informations(path):
    cmd_log = [
            'log', '-r', '.',
            ('--template=date: {date|isodate}\nchangeset: {node}\nbranch: '
             '({branch})\ntags: {tags}\n')
            ]
    cmd_url = [ 'showconfig', 'paths.default']

    def hg(cmd):
        hg = ['hg', '--cwd', path]
        p = subprocess.Popen(hg + cmd, stdout=subprocess.PIPE)
        output = p.communicate()[0]
        return output

    res = map(hg, [cmd_url, cmd_log])

    url = res[0]
    repo = path
    if url:
        repo = url.rstrip('/').split('/')[-1]

    res[0] = repo
    return res


def get_repo_informations(dirs=None):
    try:
        repos = [ path
            for lst in map(find_vcs_dirs, dirs)
            for path in lst]
        infos = map(get_hg_informations, repos)

        if infos:
            res = map(''.join, infos)
            infos = '\n'.join(res)

    except Exception, e:
        racy.print_warning("repo informations",
                "Repository informations unavailable")
        infos = "unavailable"


    if infos:
        global get_repo_informations
        get_repo_informations = lambda x=None : infos
        return infos



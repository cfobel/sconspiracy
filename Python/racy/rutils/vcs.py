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


class HgInfo:
    UNAVAILABLE = "repository informations unavailable"

    def __init__(self, dirs):
        self.processes = {}
        self.infos = None

        def get_hg_processes(path):
            cmd_log = [
                    'log', '-r', '.',
                    ('--template=date: {date|isodate}\nchangeset: {node}\nbranch: '
                    '({branch})\ntags: {tags}\n')
                    ]
            cmd_url = [ 'showconfig', 'paths.default']

            def hg(cmd):
                hg = ['hg', '--cwd', path]
                p = subprocess.Popen(hg + cmd, stdout=subprocess.PIPE)
                return p

            processes = self.processes[path] = map(hg, [cmd_url, cmd_log])
            return processes

        try:
            map(get_hg_processes, dirs)
        except Exception, e:
            self.infos = self.UNAVAILABLE


    def __call__(self):
        if self.infos is None:
            if self.processes:

                def get_repo_info(args):
                    path, processes = args
                    res = [p.communicate()[0] for p in processes]

                    url = res[0]
                    repo = path
                    if url:
                        repo = url.rstrip('/').split('/')[-1]

                    res[0] = repo
                    return res

                infos = map(get_repo_info, self.processes.items())

                if infos:
                    res = map(''.join, infos)
                    self.infos = infos = '\n'.join(res)

        return self.infos



def init_repo_informations(dirs=None):
    global get_repo_informations
    get_repo_informations = HgInfo(dirs)



def get_repo_informations(dirs=None):
    init_repo_informations(dirs)
    return get_repo_informations()


# -*- coding: UTF8 -*-

from collections import namedtuple
from subprocess import Popen, PIPE
import os




Lib = namedtuple('Lib', 'name path')

def get_lib_deps(lib):
    otool = Popen(['otool', '-L', lib], stdout=PIPE)
    output = otool.communicate()[0]
    libs = [l.strip().split()[0] for l in output.splitlines()[1:]]
    libs = [Lib(name=os.path.basename(lib), path=lib) 
            for lib in libs if lib and not lib.startswith('@')]
    return dict(libs)

def find_libs(path, ext='.dylib'):
    libs = []
    if os.path.isfile(path):
        libs += [Lib(name=os.path.basename(path), path=path)]
    else:
        for (root, dirs, files) in os.walk(path):
            files = [Lib(name = f, path=os.path.join(root,f)) for f in files]
            libs += [f for f in files if f.name.endswith(ext)]
    return dict(libs)


def get_install_name_tool_args(lib, lib_db_set, lib_db_dict, executable_path, ignored = None):
    lib_file = lib_db_dict[lib]
    lib_deps = get_lib_deps(lib_file)
    lib_deps_set = set(lib_deps)
    inter = lib_db_set.intersection(lib_deps_set)
    if ignored is not None:
        ignored.update(lib_deps_set.difference(lib_db_set))
    relpath = os.path.relpath
    librelpath = lambda path : relpath( path, executable_path )
    res = [('-id', os.path.join( '@executable_path', librelpath(lib_file)))]
    res += [ ( '-change', lib_deps[item], os.path.join( '@executable_path',
        librelpath(lib_db_dict[item]))) for item in inter]
    return res


def main():
    from optparse import OptionParser
    import sys

    usage = "usage: %prog [options] binary_or_dir ..."
    parser = OptionParser(usage=usage, epilog="ooo")
    parser.add_option("-e", "--executable-path", dest="exec_path",
                    help="executable path", metavar="DIR")
    #parser.add_option("-L", "--library-path", 
    #                action="append", dest="libpath",
    #                help="libraries path", metavar="DIR")

    parser.add_option("-p", "--progress",
                  action="store_true", dest="progress", default=False,
                  help="display progress")

    parser.add_option("-i", "--list-ignored",
                  action="store_true", dest="list_ignored", default=False,
                  help="display ignored libraries")

    parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="verbose output")


    (options, args) = parser.parse_args()


    def print_msg(*a):
        print ' '.join(map(str,a))
    def print_msg_n(*a):
        print ' '.join(map(str,a)),

    def mute(*a):
        pass

    verbose          = mute
    verbose_n        = mute
    progress_print   = mute
    progress_print_n = mute

    if options.verbose:
        verbose   = print_msg
        verbose_n = print_msg_n

    if options.progress:
        progress_print   = print_msg
        progress_print_n = print_msg_n


    libs_dict = {}
    for d in args:
        libs_dict.update(find_libs(d))

    libs_set = set(libs_dict)


    ignored = set()
    L = len(libs_set)
    for n,lib in enumerate(libs_set):
        lib_file = libs_dict[lib]
        progress_print_n(' ', '{0}/{1}'.format(n+1,L),'\r')
        sys.stdout.flush()
        if not os.path.islink(lib_file):
            #'install_name_tool -id @executable_path/../$LIBDIR/$i $i'
            #cmd = ' '.join(['install_name_tool -id', ' '.join(change), lib_file])
            #res = Popen(cmd.split(' '), stdout=PIPE).communicate()[0]
            #if res: 
            #    verbose(res)

            changes = get_install_name_tool_args(lib, libs_set, libs_dict, options.exec_path, ignored)
            verbose(lib_file)
            for change in changes:
                #cmd = ' '.join(['install_name_tool', ' '.join(change), lib_file])
                cmd = ('install_name_tool',) + change + (lib_file,)
                res = Popen(cmd, stdout=PIPE).communicate()[0]
                if res: 
                    verbose(res)
    progress_print('')

    if options.list_ignored:
        ignored = sorted([''] + map(str,ignored))
        print 'ignored libraries:', (os.linesep+'  ').join(ignored)

if __name__ == '__main__':
    main()

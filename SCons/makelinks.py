# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

from optparse import OptionParser

parser = OptionParser(
        usage = "usage: %prog src dst",
        description = "Make links in destination to source's trunks",
        version = "0.0",
        )
#parser.add_option("-s", "--src", dest="src",
#                  help="Source directory", metavar="DIR")
#parser.add_option("-d", "--dst", dest="dst",
#                  help="Destination directory", metavar="DIR")


(options, args) = parser.parse_args()

if len (args) != 2:
    parser.error("incorrect number of arguments")

SVN_PATH, DEST_PATH = args


trunks = []
ignores = ['Config', 'DBLib', 'XMLParserMFO']

for root, dirs, files in os.walk(SVN_PATH):
    for el in ['.svn', 'Makefile']:
        if el in dirs:
            dirs.remove(el)
    if 'trunk' in dirs:
        d = list(dirs)
        d.remove('trunk')
        for el in d: dirs.remove(el)
    if root.endswith("trunk") :
        trunks.append(root)

for p in trunks:
    splited = p.split(os.path.sep)
    pth, trash = os.path.split(p)
    link = pth.replace(SVN_PATH, DEST_PATH)
    must_exit_path, name = os.path.split(link)
    if name not in ignores:
        if not os.path.isdir(must_exit_path):
            os.makedirs(must_exit_path)
        if not os.path.islink(link):
            os.symlink(p, link)
            print "link ->", name


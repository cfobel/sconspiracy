# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import subprocess

def symlink(src, dest):
    try:
        from win32file import CreateSymbolicLink
        CreateSymbolicLink(dest, src, 1)
    except
        try:
            process = subprocess.Popen(['mklink','/D', dest, src])
            process.communicate()
        except:
            try:
                process = subprocess.Popen(['linkd', dest, src])
                process.communicate()
            except:
                raise Exception("No installation of mklink or linkd found")



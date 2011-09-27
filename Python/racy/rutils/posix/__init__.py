# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import os
import exceptions

def symlink(src, dest):
    try:
        os.symlink(src, dest)
    except exceptions.OSError, e:
        import errno
        if not e.errno == errno.EEXIST:
            raise e

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


__all__ = ["BaseColorText"]

import sys

class BaseColorText(object):

    cons = None

    def __init__(self, out = sys.stdout, console = 'notused'):
        self.out = out

    def get_bgcolor(self, color):
        attr = 'BACKGROUND_' + color.upper()
        return getattr(self.cons, attr)

    def get_fgcolor(self, color):
        attr = 'FOREGROUND_' + color.upper()
        return getattr(self.cons, attr)


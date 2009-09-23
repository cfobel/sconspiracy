# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import yams

from doxygenproject import DoxygenProject


KEYWORD = DoxygenProject.var_name


class Plugin(yams.yplugins.Plugin):
    name = "doxygen"

    options              = { KEYWORD : 'no' }
    allowed_values       = { KEYWORD : ['no', 'yes'] }
#    commandline_opts     = [ KEYWORD ]
    commandline_prj_opts = [ KEYWORD ]
    descriptions_opts    = { KEYWORD : 'enable/disable Doxygen Generation' }


    def has_additive(self, prj):
        val = prj.get(KEYWORD)
        return val in self.allowed_values[KEYWORD][1:]

    def get_additive(self, prj):
        res = DoxygenProject( prj = prj )
        return [res]




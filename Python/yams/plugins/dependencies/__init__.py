# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import yams

from dependenciesproject import DepedenciesProject


KEYWORD = DepedenciesProject.var_name


class Plugin(yams.yplugins.Plugin):
    name = "dependencies"

    options              = { KEYWORD : 'no' }
    allowed_values       = { KEYWORD : ['no', 'yes'] }
    commandline_opts     = [ KEYWORD ]
    commandline_prj_opts = [ KEYWORD ]
    descriptions_opts    = { KEYWORD : 'if "yes", Show project dependencies' }


    def has_additive(self, prj):
        val = prj.get(KEYWORD)
        return val in self.allowed_values[KEYWORD][1:]

    def get_additive(self, prj):
        res = DepedenciesProject( prj = prj )
        return [res]




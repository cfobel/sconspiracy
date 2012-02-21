# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from dependenciesproject import DepedenciesProject


KEYWORD = DepedenciesProject.var_name


class Plugin(racy.rplugins.Plugin):
    name = "dependencies"

    options              = { KEYWORD : 'no' }
    allowed_values       = { KEYWORD : ['no', 'yes'] }
    commandline_opts     = [ KEYWORD ]
    commandline_prj_opts = [ KEYWORD ]
    descriptions_opts    = { KEYWORD : 'if "yes", Show project dependencies' }

    additive = True

    def has_additive(self, prj):
        val = prj.get(KEYWORD)
        return val  == 'yes'

    def get_additive(self, prj):
        res = DepedenciesProject( prj = prj )
        return [res]




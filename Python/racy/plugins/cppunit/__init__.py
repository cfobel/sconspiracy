# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from cppunitproject import CppUnitProject


KEYWORD = CppUnitProject.test_type_var_name
RUN_KEYWORD = CppUnitProject.test_run_var_name


class Plugin(racy.rplugins.Plugin):
    name = "cppunit"

    options              = {
            KEYWORD     : 'no',
            RUN_KEYWORD : 'no',
            }

    allowed_values       = {
            KEYWORD     : ['no', 'exec', 'xml', 'shared'] ,
            RUN_KEYWORD : ['no', 'yes']
            }

    commandline_opts     = [ KEYWORD , RUN_KEYWORD ]
    commandline_prj_opts = [ KEYWORD , RUN_KEYWORD ]
    descriptions_opts    = {
            KEYWORD     : 'enable/disable CppUnit Tests'         ,
            RUN_KEYWORD : 'Run CppUnit Tests (xml and exec only)',
            }


    def has_additive(self, prj):
        val         = prj.get(KEYWORD)
        test_file   = CppUnitProject.get_options_file(prj)
        file_exists = os.path.isfile(test_file)
        return val in self.allowed_values[KEYWORD][1:] and file_exists

    def get_additive(self, prj):
        res = CppUnitProject( prj = prj )
        return [res]



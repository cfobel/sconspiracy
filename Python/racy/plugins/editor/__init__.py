# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import os
import racy
from os.path import join as opjoin
from editor_project import EditorProject 

KEYWORD = EditorProject.var_name
PATH_KEYWORD = EditorProject.path_project


class Plugin(racy.rplugins.Plugin):
    name = 'editor'
    editor_list = ['none', 'qtcreator', 'eclipse']



    options              = { 
                            KEYWORD : 'none', 
                            PATH_KEYWORD : '' 
                           }
    allowed_values       = { 
                            KEYWORD : editor_list
                           }

    commandline_opts     = [ KEYWORD, PATH_KEYWORD ] 
    commandline_prj_opts = [ KEYWORD, PATH_KEYWORD ] 
    descriptions_opts    = { KEYWORD :'enable / disable editor generation',
                             PATH_KEYWORD : 'generate editor file for the specified path'
                           }


    def has_additive(self, prj):
        val = prj.get(KEYWORD)

        return val in self.allowed_values[KEYWORD][1:]

    def get_additive(self, prj):
        res = EditorProject(prj) 
        
        return [res]




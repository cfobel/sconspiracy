# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import os
import racy
from os.path import join as opjoin
 
from ide_project import IdeProject



class Plugin(racy.rplugins.Plugin):
    name = 'IDE'
    prj_user_format = 'PRJ_USER_FORMAT'
    editor_list = ['none', 'qtcreator', 'eclipse']



    options              = { 
                            name  : 'none', 
                            prj_user_format : '$(PRJ_TYPE)_$(PRJ_NAME)'
                           }
    allowed_values       = { 
                             name: editor_list
                           }

    commandline_opts     = [ prj_user_format ] 
    commandline_prj_opts = [ name, prj_user_format ] 
    descriptions_opts    = { name :'create ide project',
                             prj_user_format : 'Preferencies formated project name'
                           }


    def has_additive(self, prj):
        val = prj.get(self.name)

        return val in self.allowed_values[self.name][1:]

    def get_additive(self, prj):
        if prj.type not in ['shared','exec', 'bundle']:
            return [] 
        res = IdeProject(prj) 
        return [res]

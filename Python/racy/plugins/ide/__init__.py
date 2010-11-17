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
    editor_list = ['none', 'qtcreator', 'eclipse', 'graphviz']



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
                             prj_user_format : 
    """Preferencies formated project name.
    You can used this variable like this:
    $( VARIABLE )
    PRJ_NAME           : project base name.
    RACY_CMD           : racy command.
    PRJ_TYPE           : project type.
    OS_NAME            : os name.
    SEP                : os depend separator (/ or \\).
    PATHSEP            : path separator ( : ).
    CALLING_PROJECT    : the main project.
    PROJECT_SPLIT_PATH : list of element in prj_path,
                         the first element is the last directory
                         in RACY_SRC_DIR path.
    """
                           }


    def has_additive(self, prj):
        val = prj.get(self.name)

        return val in self.allowed_values[self.name][1:]

    def get_additive(self, prj):
        if prj.type not in ['shared','exec', 'bundle']:
            return [] 
        res = IdeProject(prj) 
        return [res]

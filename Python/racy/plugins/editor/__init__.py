# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import os
import racy
from os.path import join as opjoin
 
from qtcreator import QtCreatorProject
from eclipse   import EclipseProject



class Plugin(racy.rplugins.Plugin):
    name = 'EDITOR'
    editor_list = ['none', 'qtcreator', 'eclipse']



    options              = { 
                            name  : 'none', 
                           }
    allowed_values       = { 
                             name: editor_list
                           }

    commandline_opts     = [ name ] 
    commandline_prj_opts = [ name ] 
    descriptions_opts    = { name :'enable / disable editor generation',
                           }


    def has_additive(self, prj):
        val = prj.get(self.name)

        return val in self.allowed_values[self.name][1:]

    def get_additive(self, prj):
        if prj.type not in ['shared','exec', 'bundle']:
            return [] 
        if(prj.get_lower(self.name) == 'qtcreator'): 
            res = QtCreatorProject(prj) 
            return [res]

        elif(prj.get_lower(self.name) == 'eclipse'): 
                res = EclipseProject
                return [res]




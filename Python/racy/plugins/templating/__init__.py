# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import os
import racy
import racy.renv as renv

import racy.renv.target
from os.path import join as opjoin
 
from ide_project import IdeProject
from dev_project import DevProject
from global_dico import *


class Plugin(racy.rplugins.Plugin):
    name = 'TEMPLATING'

    options = {}
    allowed_values= {}
    commandline_opts = []
    commandline_prj_opts = []
    descriptions_opts = {}


    def __init__(self):

        dico_options = get_dico_prj_options(dico_prj_template)

        for type_prj, options in dico_options.items():
            
            if options.has_key('default_value'):
                self.options[type_prj] = options['default_value']
            else:
                self.options[type_prj] =  ''

            if options.has_key('allowed_value'):
                self.allowed_values[type_prj] = options['allowed_value']

            if options.has_key('commandline_opts') and options['commandline_opts']:
                self.commandline_opts.append( type_prj )
 
            if options.has_key('commandline_prj_opts') and options['commandline_prj_opts']:
                self.commandline_prj_opts.append( type_prj)

            if options.has_key('descriptions_opts') :
                self.descriptions_opts[type_prj] = options['descriptions_opts']
            b
            b
            b
            b
            else:
                self.descriptions_opts[type_prj] = '' 


    def get_env_addon(self, env):
        prj = DevProject()
        res = []
        for i in racy.renv.TARGETS.values():
           if i.opts.has_key('CREATE_PRJ'):
               tmp = i.opts['CREATE_PRJ']
               res += prj.create_prj(i.name, tmp)


        return res

    def has_env_addon(self, env):
        for i in racy.renv.TARGETS.values():

            if i.opts.has_key('CREATE_PRJ'):
                return True

        return False


    def has_additive(self, prj):
        val = prj.get('IDE')
    
        return val in self.allowed_values['IDE'][1:]

    def get_additive(self, prj):
        if prj.type not in ['shared','exec', 'bundle']:
            return [] 
        res = IdeProject(prj) 
        return [res]

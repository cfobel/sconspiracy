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
from wix_project import WixProject
from cmake_project import CMakeProject
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
            else:
                self.descriptions_opts[type_prj] = '' 


    def get_env_addon(self, env):
        prj = DevProject()
        res = []
        for i in racy.renv.TARGETS.values():
            if i.opts.has_key('CREATE_PRJ'):
               tmp = i.opts['CREATE_PRJ']
               res += prj.create_prj(i.name, tmp)


        for i,j in racy.renv.ARGUMENTS.items():
            if i == 'CREATE_SRV' :
               res += prj.create_srv(j)
        
        return res

    def has_env_addon(self, env):
        for i in racy.renv.TARGETS.values():

            if i.opts.has_key('CREATE_PRJ'):
                return True

        for i,j in racy.renv.ARGUMENTS.items():
            if i == 'CREATE_SRV':
                return True


        return False


    def has_additive(self, prj):
        if not prj.get('IDE') == 'none':
            val = prj.get('IDE')
            res = val in self.allowed_values['IDE'][1:]
        elif prj.get('CMAKE') == 'yes':
            val = 'yes'
            res = True
        else:
            val = prj.get_lower('CREATE_WIX')
            res = val == 'yes'
        return res

    def get_additive(self, prj):
        if prj.get_lower('TYPE') not in ['shared','exec', 'bundle']:
            return []
        if not prj.get_lower('IDE') == 'none':
            res = IdeProject(prj) 
        elif prj.get_lower('CMAKE') == 'yes':
            res = CMakeProject(prj)
        else:
            res = WixProject(prj)
        return [res]

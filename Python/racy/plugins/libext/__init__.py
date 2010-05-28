# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from libextproject import LibextProject



class Plugin(racy.rplugins.Plugin):
    name = "Libext"

    #options              = { KEYWORD : {} }
    #allowed_values       = { KEYWORD : ['no', 'yes'] }
    #allowed_values       = { KEYWORD : [] }
    #commandline_opts     = [ KEYWORD ]
    #commandline_prj_opts = [ KEYWORD ]
    #descriptions_opts    = { KEYWORD : 'description of Libext Project' }

    def init(self):
        import racy.renv.configs.allowedvalues as allowed_values
        allowed_values.TYPE += LibextProject.LIBEXT


    def has_replacement(self, prj):
        res = False
        try:
            res = prj.type in LibextProject.LIBEXT
        except racy.ConfigError, e:
            """prj may raise if prj.type is invalid. We don't want to manage 
            this here"""

        return res

    def get_replacement(self, prj):
        kwargs = {
                'build_options' : prj._opts_source,
                'prj_path'      : prj._project_dir,
                'platform'      : prj._platform   ,
                'cxx'           : prj._compiler   ,
                'debug'         : prj._debug      ,
                'config'        : prj._config     ,
                'projects_db'   : prj.projects_db ,
                'env'           : prj.env         ,
                }

        res = LibextProject( **kwargs )
        return [res]

    #----------------------------------------
    def has_env_addon(self, env):
        return True

    def get_env_addon(self, env):

        from sconsbuilders import cmake, configure, make, patch, untar, url

        for builder in [cmake, configure, make, patch, untar, url]:
            builder.generate(env)

        return []



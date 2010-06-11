# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from libextproject import LibextProject


CLEAN_DOWNLOADS = 'CLEAN_DOWNLOADS'

class Plugin(racy.rplugins.Plugin):
    name = "Libext"

    options              = { CLEAN_DOWNLOADS : 'no' }
    allowed_values       = { CLEAN_DOWNLOADS : ['no', 'yes'] }
    commandline_opts     = [ CLEAN_DOWNLOADS ]
    commandline_prj_opts = [ CLEAN_DOWNLOADS ]
    descriptions_opts    = { CLEAN_DOWNLOADS :
       'libext plugin : if no, downloaded files will not be removed on clean.'
    }

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

        modules = [
                'cmake',
                'command',
                'configure',
                'edit',
                'make',
                'patch',
                'untar',
                'unzip',
                'url'
                ]

        import sconsbuilders
        builders = __import__ ('sconsbuilders', globals(), fromlist = modules)
        for module in modules:
            builder = getattr(builders, module)
            builder.generate(env)

        return []



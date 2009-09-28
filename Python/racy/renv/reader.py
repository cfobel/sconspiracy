# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import ydefaults

class ConfigReader(object):

    def __init__(self):
        mods = ydefaults.get_racy_option( "CONFIG_IMPORTED_MODULES" )
        mods = dict( [ (mod, __import__(mod)) for mod in mods ] )

        self.__config_imported_modules__ = mods


    def __call__(self, file, globals, locals):
        globals.update(self.__config_imported_modules__)
        execfile (file, globals, locals)

        import racy.renv.configs.default as defaults
        defaults.check_deprecated(locals, file)

        return locals


read_config = ConfigReader()

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import ydefaults

class ConfigReader(object):

    def __init__(self):
        mods = ydefaults.get_racy_option( "CONFIG_IMPORTED_MODULES" )
        mods = dict( [ (mod, __import__(mod)) for mod in mods ] )

        self.__config_imported_modules__ = mods


    def __call__(self, _file, _globals, _locals):
        _globals.update(self.__config_imported_modules__)
        execfile (_file, _globals, _locals)

        import racy.renv.configs.default as defaults
        defaults.check_deprecated(_locals, _file)

        return _locals


read_config = ConfigReader()

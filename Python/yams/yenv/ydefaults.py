# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from yams import NotUsed

YAMS_DEFAULTS = {
    'CONFIG_IMPORTED_MODULES' : ["sys", "os", "yams"],
        }

def get_yams_option(opt):
    return YAMS_DEFAULTS.get(opt, None)





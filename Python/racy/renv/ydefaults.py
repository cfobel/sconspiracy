# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from racy import NotUsed

RACY_DEFAULTS = {
    'CONFIG_IMPORTED_MODULES' : ["sys", "os", "racy"],
        }

def get_racy_option(opt):
    return RACY_DEFAULTS.get(opt, None)





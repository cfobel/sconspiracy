# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from yams import Undefined
from yams.yenv import constants
LOGLEVEL      = constants.LOGLEVEL.keys()


ARCH          = ['32','64']
DEBUG         = ['full','release']
DISTRIB       = ['yes','no']

TOOL          = ['auto','g++','msvc']

TYPE          = [
                'exec','shared','static','bundle',
                'bin_shared', 'bin_bundle', 'bin_exec', 'bin_libext',
                ]


USEVISIBILITY = [
        'yes',
        'yams', # XXX: Transitionnal, will be removed
        'no'
        ]
CONSOLE       = ['yes','no']
#TEST          = ['no', 'exec', 'xml', 'shared']

#OPTIMIZATIONLEVEL = 0


BUILD         = ['yes','no']
BUILDDEPS     = ['yes','no']
BUILDPKG      = ['yes','no']
YAMS_DEBUG    = ['yes','no']


from yams import ConfigError

def checkvalue( key, value, exceptions = {}):
    """Return True if <value> is in local variable <key>, or if no local 
    variable matches <key>, or if <value> matches exceptions[key].
    """
    import yams.yenv.configs.allowedvalues as vars
    if exceptions.get(key, Undefined) == value:
        return True
    v = getattr(vars, key, Undefined)
    return v == Undefined or value in v


def check_value_with_msg(opt, val, location, exceptions = {},
        except_class = ConfigError):
    """Raise an exception if checkvalue return False."""
    import yams.yenv.configs.allowedvalues as vars
    if not checkvalue(key = opt, value = val, exceptions = exceptions):
        allowed = getattr(vars, opt, None)
        msg = ( "Value '{value}' not allowed for option '{opt}', in <{loc}>. "
                "Allowed values are : {allow}").format(
                                                    value = val, 
                                                    opt   = opt, 
                                                    loc   = location,
                                                    allow = allowed
                                                    )
        raise except_class, msg

def check_dict_with_msg(d, location, exceptions = {},
        except_class = ConfigError):
    """Check every item in d. Raise an exception if checkvalue return 
    False.
    """
    import yams
    for opt, val in d.items():
        yams.yenv.configs.allowedvalues.check_value_with_msg(
            opt          = opt,
            val          = val, 
            location     = location,
            exceptions   = exceptions,
            except_class = except_class
            )

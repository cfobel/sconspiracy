# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******



import imp
import os

from functools import partial

from racy import ConfigVariantError
from racy.renv import constants
from racy.renv.reader import read_config


DEFAULT_CONFIG = 'default'
INVALID_NAMES = [
        "__init__.py",
        "commandline",
        "allowedvalues",
        None,
        "",
        ]

RACY_DEFAULTS_PATH = os.path.dirname(__file__)


def get_config(name, 
        path = None, _locals = None, _globals = None, 
        raise_on_not_found = True, write_postfix=False,
        read_default = True, include_defaults = True,
        default_config = DEFAULT_CONFIG, defs = None):
    """Get and returns variables defined in <name> file.

    If read_default is True, read default_config first.

    if _locals or/and _globals is given, put results in them.

    if 'raise_on_not_found' is True, raise an ConfigVariantError exception if 
    the config file is not found.

    if 'write_postfix' is True, put 'name' in _locals['POSTFIX'] *before* 
    reading config file.

    updates '_locals' with definitions in config
    updates 'defs' with definitions in config
    """

    if os.path.isabs(name) and path is None:
        path = os.path.dirname(name)
        name = os.path.basename(name)

    if name in INVALID_NAMES:
        msg = 'Invalid configuration name: <{0}>'.format(name)
        raise ConfigVariantError, msg
    
    if not path:
        path = RACY_DEFAULTS_PATH

    if _globals is None: _globals = {}
    if _locals  is None:  _locals = {}

    config_file = os.path.join(path,name)

    if not os.path.isfile(config_file):
        if raise_on_not_found:
            msg = 'Configuration <{0}> not available.'.format(config_file)
            raise ConfigVariantError, msg
    else:
        # exec 'default' first if needed
        if read_default and name is not default_config:
            source = _globals
            if include_defaults:
                source = _locals
            get_config(default_config, _locals = source, 
                    raise_on_not_found = False)

        if write_postfix:
            if 'POSTFIX' in _locals:
                _locals['POSTFIX'] += [name]
            else:
                _locals['POSTFIX'] = [name]

        res = {}
        globals_env = dict(_globals)
        globals_env.update(_locals)
        read_config(config_file, globals_env, res)

        _locals.update(res)
        if defs is not None:
            defs.update(res)

    return _locals




# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os


import racy

from racy              import rutils, NotUsed, ConfigVariantError, Undefined
from racy.renv.configs import allowedvalues
from racy.rutils       import memoize

import configs
import reader


exceptionnal_case = {'TYPE': 'no type defined'}


@memoize
def get_racy_default(opt, config, 
        default=NotUsed, prj=NotUsed, option_value=Undefined):

    if config is None:
        config = get_option('CONFIG',config=configs.DEFAULT_CONFIG)

    try:
        defaults_source = configs.get_config(config)
    except ConfigVariantError, e:
        defaults_source = configs.get_config(configs.DEFAULT_CONFIG)


    res = defaults_source.get(opt)

    allowedvalues.check_value_with_msg(opt, res, config, exceptionnal_case)

    return res


@memoize
def get_file_options(opt, files):
    """Get the dictionnary of the first existing file in files if opt is None,
    else the value of the option 'opt'."""
    res = {}

    options_file = rutils.get_first_existing_file(files)
    if options_file is not None:
        reader.read_config(options_file, {}, res)
    if opt is not None:
        res = res.get(opt,{})


    return res

@memoize
def get_user_options(opt, config, default, prj=NotUsed, option_value=Undefined):
    """Lookup for a user.options file in RACY_CONFIG_DIR. Get the user 
    option 'opt' if exists. A user option is overrided by a user config option
    """
    import racy.renv as renv

    files = [
            ( renv.dirs.config, 'user.options'),
            ]

    file_opts = get_file_options(None, files)
    res = file_opts.get(opt, default)

    options_file = rutils.get_first_existing_file(files)
    ckconfig = config
    if options_file is not None:
        ckconfig = ":".join([options_file, config])
    allowedvalues.check_value_with_msg(opt, res, ckconfig, exceptionnal_case)

    try:
        old_res = res

        loc = renv.dirs.user_configs
        source = configs.get_config(config, path=loc,
                include_defaults = False)

        res = source.get(opt, res)

        if old_res != res:
            ckconfig = ":".join([loc,config])
            allowedvalues.check_value_with_msg(opt, res, ckconfig, 
                                                exceptionnal_case)
    except ConfigVariantError, e:
        pass # user-config 'config' is inexistant

    return res


@memoize
def get_user_prj_options(opt, config, default, prj, option_value=Undefined):
    """Lookup for a user.prj.options file in RACY_CONFIG_DIR. Get the user 
    option 'opt' for 'prj' if exists.
    """
    import racy.renv as renv
    files = [
            ( renv.dirs.config, 'user.prj.options'),
            ]
    res = default
    
    if prj is not None and get_racy_default('ALLOW_USER_OPTIONS', config):
        res = get_file_options(opt, files).get(prj.base_name, default)

    options_file = rutils.get_first_existing_file(files)
    if options_file is not None:
        config = ":".join([options_file, config])
    allowedvalues.check_value_with_msg(opt, res, config)

    return res


#@memoize
def get_commandline_options(opt, default, option_value=Undefined,
                            config=NotUsed, prj=NotUsed ):
    from racy import renv
    res = default

    # the right for opt to be in ARGUMENTS has already been checked
    # the value validity of the option too.
    res = renv.ARGUMENTS.get(opt,res)

    return res


#@memoize
def get_commandline_prj_options(opt, prj, default, option_value=Undefined,
                            config=NotUsed ):
    from racy import renv
    # The right for opt to be in TARGETS[prj.base_name] has already been
    # checked.
    # The value's validity of the option too.
    res = default
    if prj:
        res = renv.TARGETS.get(prj.base_name).opts.get(opt,res)

    return res


@memoize
def get_overrided_project_value(opt, config, default, option_value,
                                        prj=NotUsed):
    override = get_racy_default('OVERRIDE_PROJECT_VALUE', config)
    res = override.get(opt, option_value 
            if option_value is not Undefined and option_value else default)
    allowedvalues.check_value_with_msg(opt, res, config+":OVERRIDE_PROJECT_VALUE")
    return res


@memoize
def check_deprecated(opt, config, prj, default=NotUsed, option_value=Undefined):
    deprecated = get_racy_default('DEPRECATED', config)

    if deprecated.has_key(opt):
        import warnings
        msg = [
            ('<{0}> option is deprecated (config <{1}>) and not'
             'supported anymore.').format(opt, config)
            ]
        msg += [deprecated[opt]]
        location = prj.full_name if prj else 'config '+ config
        warnings.warn_explicit(
            " ".join(msg),
            DeprecationWarning,
            '[{0}]:'.format(location), 
            0
            )


@memoize
def get_option(opt, prj=None, default=None, option_value=Undefined, config=None):
    if config is None:
        config = get_option('CONFIG',config=configs.DEFAULT_CONFIG)

    kwargs = {
            'opt'          : opt,
            'config'       : config,
            'default'      : default,
            'option_value' : option_value,
            'prj'          : prj,
            }

    funcs = [
            check_deprecated,
            get_racy_default,
            get_user_options,
            get_overrided_project_value,
            get_user_prj_options,
            get_commandline_options,
            get_commandline_prj_options,
            ]

    for f in funcs:
        avant = kwargs['default']
        kwargs['default'] = f(**kwargs)

    res = kwargs['default']

    return res



import constants

class Paths(object):
    var_names = {
        'dev'       : 'RACY_DEV_DIR'      ,
        'config'    : 'RACY_CONFIG_DIR'   ,
        'build'     : 'RACY_BUILD_DIR'    ,
        'install'   : 'RACY_INSTALL_DIR'  ,
        'binpkg'    : 'RACY_BINPKGS_DIR'  ,
        'code'      : 'RACY_CODE_DIRS'    ,
        }

    var_multipath = [ 'code' ]

    def get_path(self, name):
        var_names = self.var_names
        res = None
        if var_names.has_key(name):
            vn = var_names[name]
            if name == 'config':
                res = get_racy_default(vn, configs.DEFAULT_CONFIG)
            else:
                res = get_option( vn )
            if not res:
                res = os.environ.get(vn,'')
                if name in self.var_multipath:
                    res = res.split(os.pathsep)
        else:
            raise racy.EnvError, "{0} path undefined".format(name)

        if not rutils.is_iterable(res):
            res = os.path.expanduser(res)
            ckres = [res]
        else:
            res = [os.path.expanduser(r) for r in res]
            ckres = res
        for p in ckres:
            if not os.path.isdir(p):
                msg = '{0}="{1}" is not a dir.'.format(vn,p)
                racy.print_warning('Environment warning',msg)
                #raise racy.EnvError, msg

        if vn.endswith('DIRS'):
            res = rutils.iterize(res)

        if rutils.is_iterable(res):
            return [os.path.abspath(p) for p in res]
        else:
            return os.path.abspath(res)

    def __get_var(var, root = None):
        def f1(self):
            return self.get_path(var)
            return path
        def f2(self): #derived path
            import racy.renv as renv
            alternatives = {
                    'lib' : {constants.MACOSX : 'Libraries'}
                    }
            name = alternatives.get(var,{}).get(renv.platform(),var)
            return os.path.join(getattr(self,root), name)
            
        f = f2 if root is not None else f1
        return f

    config         = property(__get_var('config'))
    build          = property(__get_var('build'))
    install        = property(__get_var('install'))
    binpkg         = property(__get_var('binpkg'))
    code           = property(__get_var('code'))

    user_configs   = property(__get_var( 'configs', root='config' ))

    install_bin    = property(__get_var( 'bin'     , root='install'))
    install_binpkg = property(__get_var( 'Pkgs'    , root='install'))
    install_bundle = property(__get_var( 'Bundles' , root='install'))
    install_doc    = property(__get_var( 'doc'     , root='install'))
    install_lib    = property(__get_var( 'lib'     , root='install'))
    install_share  = property(__get_var( 'share'   , root='install'))



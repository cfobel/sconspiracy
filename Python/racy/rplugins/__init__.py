# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from racy.rutils import memoize


def must_be_overloaded(func):
    def new_func(self, *a,**kw):
        msg = "{0.__name__} of {1.__class__} is not implemented"
        raise racy.RacyPluginError, msg.format(func, self)
    return new_func

@racy.no_undef_attr_read
@racy.no_undef_attr_write
class Plugin(object):
    name = ""

    options              = {}
    allowed_values       = {}
    commandline_opts     = []
    commandline_prj_opts = []
    commandline_prj_args = []
    descriptions_opts    = {}
    

    #----------------------------------------
    def has_additive(self, prj):
        return False

    @must_be_overloaded
    def get_additive(self, prj):
        return []


    #----------------------------------------
    def has_replacement(self, prj):
        return False

    @must_be_overloaded
    def get_replacement(self, prj):
        return []


    #----------------------------------------
    def has_env_addon(self, env):
        return False

    @must_be_overloaded
    def get_env_addon(self, env):
        return []
    
    #----------------------------------------

    def __load__(self):
        def list_extend_uniq(src,dst):
            """Extends src with dst, check for duplicates. Returns duplicates
            values
            """
            res = []
            for el in src:
                if el not in dst: dst.append(el)
                else: res.append(el)
            return res

        def already_defined_exception(defs, attr):
            msg = ("Plugin '{plug.name}' is redefining <Plugin.{attr}>"
                   " existing values : {defs}")
            msg = msg.format(plug=self, defs=defs, attr=attr)
            raise racy.RacyPluginError, msg

        def register_list(src_name, dst):
            src = getattr(self, src_name)
            defined = list_extend_uniq( src, dst )
            if defined: 
                already_defined_exception(defined, src_name)

        def register_dict(src_name, dst):
            src = getattr(self, src_name)
            defined  = list_extend_uniq( src.keys(), dst.keys())
            if defined: 
                already_defined_exception(defined, src_name)
            dst.update(src)


        import racy.renv.configs.default       as default
        register_dict("options", default.__dict__ )


        import racy.renv.configs.allowedvalues as allowedvalues
        register_dict("allowed_values", allowedvalues.__dict__ )


        import racy.renv.configs.commandline   as commandline
        register_list("commandline_opts", 
                        commandline.ALLOWED_COMMANDLINE_OPTIONS)

        register_list("commandline_prj_opts", 
                        commandline.ALLOWED_COMMANDLINE_PRJ_OPTIONS)

        register_dict("descriptions_opts", 
                        commandline.COMMANDLINE_OPTIONS_DESC)



d = dir

class PluginRegistry(object):

    plugins = {}

    def load_dir(self, dir):
        """Find dirs (non recursive) and load each plugin found in the dir"""
        import imp

        if not os.path.isdir(dir):
            raise racy.RacyPluginError, "{0} isn't a directory, can't load_dir"

        walker = os.walk(dir)
        root, dirs, files = walker.next()
        racy.rutils.remove_vcs_dirs(dirs)

        for dir in dirs:
            try:
                fp, pathname, description = imp.find_module(dir, [root])
            except ImportError, e:
                pass

            try:
                plugin = imp.load_module(dir, fp, pathname, description)
                self.load_plugin(plugin)
            except Exception, e:
                tb = str(e) + os.linesep + ''.join(racy.get_last_exception_traceback())
                msg = "Unable to load '{plug}' plugin : {err}".format(
                        plug = dir, err=tb )
                racy.print_warning('Plugin load', msg, wrap=False)
            finally:
                if fp:
                    fp.close()



    def load_plugin(self, plugin):
        import types
        if isinstance(plugin, types.ModuleType):
            if not hasattr(plugin, "Plugin"):
                msg = "<{0.__file__}> doesn't define a Racy plugin"
                raise racy.RacyPluginError, msg.format(plugin)

            plug = plugin.Plugin()
            plugin.Plugin = plug
            name = plug.name
            if not self.plugins.has_key(name):
                self.plugins[name] = plugin
                plug.__load__()
                racy.rlog.info.log('Loaded Plugin', plug.name)
            else:
                oldpl = self.plugins[name]
                msg = ("<{name}> plugin already registered."
                       "Defined here : {plg.__file__}. "
                       "Redefined here : {old.__file__}. "
                       )
                raise racy.RacyPluginError, msg.format(
                        plg  = plugin,
                        old  = oldpl,
                        name = name
                        )
        else:
            msg = ("<{0}> is not a python module, "
                   "can't load as SConspiracy plugin.")
            raise racy.RacyPluginError, msg.format(plugin)



    def obj_eligible_plugins(self, obj, entry):
        def check(plugin,o):
            method = 'has_' + entry
            return getattr(plugin.Plugin,method)(o)
        
        plugins = [p for p in self.plugins.values() if check(p,obj)]
        return plugins

    def get_plugins_result(self, obj, entry):
        def get_prj(plugin,o):
            method = 'get_' + entry
            return getattr(plugin.Plugin,method)(o)
        res = []
        for p in self.obj_eligible_plugins(obj, entry):
            res += get_prj(p,obj)
        return res

    def get_additive_projects(self, prj):
        return self.get_plugins_result(prj, "additive")

    def get_replacement_projects(self, prj):
        return self.get_plugins_result(prj, "replacement")

    def get_env_addons(self, env):
        return self.get_plugins_result(env, "env_addon")


register = PluginRegistry()
del PluginRegistry



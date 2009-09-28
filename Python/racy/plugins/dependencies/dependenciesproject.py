# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 

import racy
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once


class DepedenciesError(racy.RacyProjectError):
    pass

DEPENDENCIES_PLUGIN_PATH = os.path.dirname(__file__)

class DepedenciesProject(ConstructibleRacyProject):
    var_name = 'DEPS'

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = ('DepedenciesProject take a '
                   'ConstructibleRacyProject as first argument')
            raise DepedenciesError( self, msg )

        opt_file = prj.opts_path

        super(DepedenciesProject, self).__init__(
                                        options_file = opt_file, 
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )

    @property
    def name (self):
        name = super(DepedenciesProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(DepedenciesProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result


    @memoize
    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        deps = self.rec_deps
        libs    = [dep for dep in deps if dep.is_lib]
        bundles = [dep for dep in deps if dep.is_bundle]
        execs   = [dep for dep in deps if dep.is_exec]
        libs    = ['lib-' + lib.name for lib in libs]
        bundles = ['bundle-' + bun.name for bun in bundles]
        execs   = ['exec-' + ex.name for ex in execs]
        uses = set()
        for dep in deps:
            uses.update([ u for u in dep.uses ])
        msg = ' '.join(bundles + libs + execs)
        racy.print_msg(self.base_name + ':' + msg)
        racy.print_msg(self.base_name + ' libext:' + ' '.join(uses))
        return result

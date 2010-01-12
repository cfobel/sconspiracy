# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 

from os.path import join as opjoin

import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once


class CppUnitError(racy.RacyProjectError):
    pass

CPPUNIT_PLUGIN_PATH = os.path.dirname(__file__)


class QtProject(ConstructibleRacyProject):

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = ('QtProject take a '
                   'ConstructibleRacyProject as first argument')
            raise CppUnitError( self, msg )

        opt_file = self.get_options_file(prj)


        super(CppUnitProject, self).__init__(
                                        options_file = opt_file, 
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )

        print "trace"


    #@memoize
    #def result (self, deps_results):
        #res = super(CppUnitProject, self).result(deps_results=deps_results)

        #if self.get_lower(self.test_run_var_name) == 'yes':
            #if self.type == 'shared':
                #raise CppUnitError(self, "Cannot run a shared CppUnit test.")
            #run_env = self.env.Clone()

            #dirs = racy.renv.dirs
            #install_lib = opjoin(dirs.install,"lib")

            #env_var = {
             #"linux"  : 'LD_LIBRARY_PATH'  ,
             #"darwin" : 'DYLD_LIBRARY_PATH',
             #"windows": 'PATH'             ,
            #}
            #env_var = env_var[racy.renv.system()]

            #run_env.AppendENVPath(env_var, install_lib)
            #run_test = run_env.Alias('run'+self.name, res, res[0].abspath)
            #run_env.AlwaysBuild(run_test)

            #res += run_test

        #return res

    #@memoize
    #def install (self, opts = []):
        #return super(CppUnitProject, self).install(opts = [])


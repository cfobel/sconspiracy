# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
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


class CppUnitProject(ConstructibleRacyProject):
    cppunit_test_dir    = 'tu'
    cppunit_option_file = 'cppunit.options'

    test_type_var_name = 'CPPUNIT'
    test_run_var_name  = 'CPPUNIT_RUN'

    @staticmethod
    def get_options_file(prj):
        opt_file = opjoin(
                    prj.get_path(constants.TEST_PATH), 
                    CppUnitProject.cppunit_option_file
                    )
        return opt_file


    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = ('CppUnitProject take a '
                   'ConstructibleRacyProject as first argument')
            raise CppUnitError( self, msg )

        opt_file = self.get_options_file(prj)


        super(CppUnitProject, self).__init__(
                                        build_options = opt_file, 
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )


    def get_path (self, path = ""):
        """Returns <project>/test/[path]"""
        root = super(CppUnitProject, self).get_path(constants.TEST_PATH)
        path = opjoin(root, self.cppunit_test_dir, path)
        return os.path.abspath(os.path.normpath(path))


    @cached_property
    def classtest (self):
        return self.get('CLASSTEST')

#    @cached_property
    @property
    def test_type (self):
        return self.get_lower(self.test_type_var_name)

    @cached_property
    def type (self):
        return self.test_type if self.test_type == "shared" else "exec"


#    @cached_property
    @property
    def name (self):
        name = super(CppUnitProject, self).name
        return LibName.SEP.join( [self.cppunit_test_dir, self.test_type, name])

    @cached_property
    def sources(self):
        files = ['{0}.cpp'.format(cls) for cls in self.classtest]

        testfiles = super(CppUnitProject,self).sources
        testfiles  = [f for f in testfiles if os.path.basename(f) in files]
        testfiles += [ self.runner_src ]

        return testfiles

    @cached_property
    def runner_src_path(self):
        return opjoin(CPPUNIT_PLUGIN_PATH, 'rc')

    @cached_property
    def runner_src(self):
        sources = {
            'shared':'testRunnerShared.cpp',
            'exec'  :'testRunnerExec.cpp'  ,
            'xml'   :'testRunnerXML.cpp'   ,
            }
        runner = sources.get(self.test_type)
        runner = opjoin(self.runner_build_dir, runner)
        return runner


    @cached_property
    def runner_build_dir(self):
        return opjoin(self.build_dir, 'CPPUnit_runner')

    @run_once
    def configure_env(self):
        racy.rlibext.register.configure(self, ['cppunit'])

        super(CppUnitProject, self).configure_env()

        self.variant_dir( self.runner_build_dir, self.runner_src_path )


    @memoize
    def result (self, deps_results):
        res = super(CppUnitProject, self).result(deps_results=deps_results)
        return res

    @memoize
    def install (self, opts = []):
        if rutils.is_true(self.get('BUILD')):
            res = super(CppUnitProject, self).install(opts = opts)
        else:
            res = []

        if self.get_lower(self.test_run_var_name) == 'yes':
            if self.type == 'shared':
                raise CppUnitError(self, "Cannot run a shared CppUnit test.")
            run_env = self.env.Clone()

            dirs = racy.renv.dirs
            install_bin = opjoin(dirs.install,"bin")
            install_lib = opjoin(dirs.install,"lib")

            run_env.AppendENVPath(racy.renv.LD_VAR, install_lib)
            execpath = opjoin(install_bin, self.full_name)
            run_test = run_env.Alias('run-'+self.name, res, execpath)
            if res:
                run_env.Depends(run_test, res[0])
            run_env.AlwaysBuild(run_test)

            res += run_test

        return res


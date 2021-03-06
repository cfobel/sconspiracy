# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

from SCons.Environment import Environment as Env
from SCons import Action

env_vars  = {}
env_tools = [ 'default' ]

def add_tool(tool):
    env_tools = list(set(env_tools + tool))

def add_var(vars):
    env_vars.update(vars)

def CopyBuilder (target, source, env):
    from racy import rutils
    rutils.copy(
            src = source[0].abspath,
            dst = target[0].abspath,
            preserve_links = True,
            preserve_relative_links_only = True,
            )

class Environment(Env):
    def __init__(self, *args, **kwargs):
        from os.path           import abspath, dirname, join

        import racy


        import racy.renv as renv
        import racy.rlog as rlog

        from racy.renv         import constants
        from racy.renv.options import get_option
        from racy.rproject     import RacyProjectsDB

        kwargs['toolpath'] = renv.toolpath() + kwargs.get('toolpath',[])
        self._callbacks = []

        for opt in ['DEBUG', 'TOOL', 'MSVC_VERSION','MSSDK_VERSION']:
            kwargs[opt] = get_option(opt)


        kwargs.setdefault('tools',[])
        kwargs['tools'] += env_tools
        kwargs.update(env_vars)

        kwargs['ARCH'] = get_option('ARCH')
        cxx = get_option('CXX')
        if cxx :
            kwargs['CXX'] = cxx

        Env.__init__(self, *args, **kwargs)

        FLAGS = (
                  '$( ${{_concat(INCPREFIX, {0}, INCSUFFIX, '
                  '__env__, RDirs, TARGET, SOURCE)}} $)'
                 )

        self['CPP_LIBEXT_PATH'] = []
        self['_CPPINCFLAGS'] = (
                FLAGS.format('CPPPATH')
                + FLAGS.format('CPP_LIBEXT_PATH')
                    )


        act = self.Action( CopyBuilder, "Install '$$SOURCE' as '$$TARGET'")
        self.__CopyBuilder__ = self.Builder(
                action = act,
                source_factory = self.Entry,
                target_factory = self.Entry,
                )

        res = racy.rplugins.register.get_env_addons(self)
       
        if True in res:
            racy.exit_racy(0)

        self['_FORCE_INCLUDE'] = '${_defines(FORCE_INCLUDE_PREFIX, FORCE_INCLUDE, FORCE_INCLUDE_SUFFIX, __env__)}'
        self['_CCCOMCOM'] = self['_CCCOMCOM'] + ' ${_FORCE_INCLUDE}'

        if not self.GetOption('help'):
            tool = self['TOOL']
            if tool == 'auto':
                tool = constants.SYSTEM_DEFAULT_TOOL[renv.system()]
            self.Tool(tool)

            self.Decider('MD5-timestamp')


            self.prj_db = db = RacyProjectsDB(env = self)
            self.lookup_list.append( db.target_lookup )


        num_jobs = get_option('JOBS')
        if num_jobs == 'auto':
            import multiprocessing
            num_jobs = multiprocessing.cpu_count()
        self.SetOption('num_jobs', num_jobs)
        
        # allow use of cached md5 after 600 sec (instead of 2 days).
        self.SetOption('max_drift', 600)
        
        racy_db_file_default = join(racy.renv.dirs.build, '.sconsign.dblite')

        racy_db_file = get_option('RACY_DBFILE')
        if not racy_db_file:
            racy_db_file = racy_db_file_default

        self.SConsignFile(racy_db_file)
        rlog.info.log(".sconsign file", racy_db_file)

        import os
        from racy.renv.configs.commandline import get_opts_help
        self.Help( (os.linesep*2).join(get_opts_help()) )

        map(lambda f:f(self), self._callbacks)
        del self._callbacks




    def WriteFile(self, target, content):
        def writer(target, source, env):
            for t in target:
                output = file(str(t), "w")
                output.write(content)
                output.close()

        act = self.Action(writer, "Writing file '{0}'".format(target))
        bld = self.Builder(action = act)
        return bld(self, target, None)


    def CopyFile(self, target, source):
        import os
        from racy import rutils
        target = rutils.iterize(target)
        source = rutils.iterize(source)
        if len(target) != len(source):
            # let scons manage error
            Environment.InstallAs(self, target, source)

        res = []
        for src, dst in zip(source, target):
            res += self.__CopyBuilder__(self, dst, src)
        return list(set(res))



# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from SCons.Environment import Environment as Env
from SCons import Action

def CopyBuilder (target, source, env):
    from yams import yutils
    yutils.copy(
            src = source[0].abspath,
            dst = target[0].abspath,
            preserve_links = True,
            preserve_relative_links_only = True,
            )

class Environment(Env):
    def __init__(self, *args, **kwargs):
        from os.path           import abspath, dirname, join

        import yams
        import yams.yenv as yenv
        import yams.ylog as ylog

        from yams.yenv         import constants
        from yams.yenv.options import get_option
        from yams.yproject     import YamsProjectsDB

        kwargs['toolpath'] = yenv.toolpath() + kwargs.get('toolpath',[])

        for opt in ['DEBUG', 'TOOL', 'MSVS_VERSION']:
            kwargs[opt] = get_option(opt)

        Env.__init__(self, *args, **kwargs)


        act = self.Action( CopyBuilder, "Install file '$$SOURCE' as '$$TARGET'")
        self.__CopyBuilder__ = self.Builder(action = act)

        yams.yplugins.register.get_env_addons(self)

        if not self.GetOption('help'):
            tool = self['TOOL']
            if tool == 'auto':
                tool = constants.SYSTEM_DEFAULT_TOOL[yenv.system()]
            self.Tool(tool)

            lib_dirs = [yenv.dirs.libext]
            lib_path = [ join(p, 'lib'    ) for p in lib_dirs]
            cpp_path = [ join(p, 'include') for p in lib_dirs]

            self.AppendUnique( LIBPATH = lib_path )
            self.AppendUnique( CPPPATH = cpp_path )

            self.Decider('MD5-timestamp')

            self.prj_db = db = YamsProjectsDB(env = self)
            self.lookup_list.append( db.target_lookup )

        num_jobs = get_option('JOBS')
        if num_jobs == 'auto':
            import multiprocessing
            num_jobs = multiprocessing.cpu_count()
        self.SetOption('num_jobs', num_jobs)
        
        # allow use of cached md5 after 600 sec (instead of 2 days).
        # Speed up about a few seconds
        self.SetOption('max_drift', 600)
        
        sconsign_file = self.GetOption('file')
        if sconsign_file:
            yams_sconsdir     = dirname(sconsign_file[0])
        else:
            yams_sconsdir     = '.'
        yams_sconsignfile = join(yams_sconsdir,'.sconsign.dblite')
        yams_sconsignfile = abspath(yams_sconsignfile)
        self.SConsignFile(yams_sconsignfile)
        ylog.info.log(".sconsign file", yams_sconsignfile)

        import os
        from yams.yenv.configs.commandline import get_opts_help
        self.Help( (os.linesep*2).join(get_opts_help()) )



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
        from yams import yutils
        target = yutils.iterize(target)
        source = yutils.iterize(source)
        if len(target) != len(source):
            # let scons manage error
            Environment.InstallAs(self, target, source)

        res = []
        for src, dst in zip(source, target):
            res += self.__CopyBuilder__(self, dst, src)
        return list(set(res))



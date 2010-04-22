# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 

from os.path import join as opjoin

import racy

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once


class LibextError(racy.RacyProjectError):
    pass

DOXYGEN_PLUGIN_PATH = os.path.dirname(__file__)

class LibextProject(ConstructibleRacyProject):
    doxygen_dir    = 'Dox'
    var_name = 'LIBEXT'
    LIBEXT    = ('libext', )

    def __init__(self, *args, **kwargs):
        super(LibextProject, self).__init__( *args, **kwargs )


    @cached_property
    def conf (self):
        return self.get(self.var_name)

    @cached_property
    def url_source (self):
        import racy.rscons.url
        url = self.conf['URL_SOURCE']
        url = racy.rscons.url.URL(url)
        return url

    @cached_property
    def url_source_type (self):
        return self.conf['SOURCE_TYPE']

    @cached_property
    def download_target (self):
        path = [self.build_dir, 'Download']
        fmt = "{0.name}_{0.version}.{0.url_source_type}"
        path.append(fmt.format(self))
        return os.path.join(*path)


    @run_once
    def configure_env(self):
        super(LibextProject, self).configure_env()

    def build(self, *a, **k):
        res = self.env.Download( 
                self.env,
                source = self.url_source ,
                target = self.download_target
                )
        return res

    @memoize
    def result(self, deps_results=True):
        prj = self
        env = self.env

        result = []
        self.configure_env()


        sources = []


        #result = env.Doxygen( 
                    #target = env['ENV']['DOX_OUTPUTDIR'],
                    #source = sources,
                    #)

        for node in result:
            env.Clean(node, node)

        return result


    #@cached_property
    #def install_path(self):
        #install_dir = racy.renv.dirs.install_doc
        #return install_dir


    @memoize
    def install (self, opts = ['rc','deps']):
        prj = self
        env = self.env

        result = prj.build(build_deps='deps' in opts)

        #if result:
            #import shutil
            #shutil.rmtree(env['ENV']['DOX_OUTPUTDIR'], ignore_errors=True)
            #shutil.rmtree(opjoin(prj.install_path,prj.full_name), ignore_errors=True)
            #result = env.Install(dir = prj.install_path, source = result)
            #for node in result:
                #env.Clean(node, node)
        #else:
            #result = []

        return result

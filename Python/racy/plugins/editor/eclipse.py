# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 
import shutil
import random
import string

from string import Template
from os.path import join as opjoin

import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once


class EclipseProjectError(racy.RacyProjectError):
    pass

ECLIPSE_PLUGIN_PATH = os.path.dirname(__file__)
CPROJECT_FILE = ".cproject"
PROJECT_FILE  = ".project"

class EclipseProject(ConstructibleRacyProject):

    var_name = 'ECLIPSE_PRJ'


    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = ('EclipseProject take a '
                   'ConstructibleRacyProject as first argument')
            raise EclipseProjectError( self, msg )

        opts = prj.opts_source

        super(EclipseProject, self).__init__(
                                        build_options = opts, 
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )

    @property
    def name (self):
        name = super(EclipseProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(EclipseProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result

    def get_rc_path(self):
        return opjoin(ECLIPSE_PLUGIN_PATH, 'rc')

        
    def clean_project(self, racy_project):
        project_path   = os.path.normpath(racy_project.root_path)
        project_dest   = os.path.join(project_path, PROJECT_FILE)
        cproject_dest  = os.path.join(project_path, CPROJECT_FILE)
        if os.path.exists(project_dest):
            os.remove(project_dest)
            racy.print_msg('remove: ' + project_dest)
  
        if os.path.exists(cproject_dest):
            os.remove(cproject_dest)
            racy.print_msg('remove: ' + cproject_dest)
    
    
    def create(self, racy_project):
        # "Emilie style" project name:
        # SrcDir_SrcLib_core_fwData
        # "Standard style" project name:
        # lib-fwData
        
        format="{type}-{prjname}"
        format="{srcdir}_{prjpath}"
        
        type_tr = {"shared":"lib", "static":"lib"}
        
        project_path = os.path.normpath(racy_project.root_path)
        base_name = racy_project.base_name

        prjname = racy_project.base_name
        prjpath = project_path
        srcdir  = 'unknown'
        type    = racy_project.type.lower()
        type    = type_tr.get(racy_project.type.lower(),type)
        
        
        for path in racy.renv.dirs.code:
            if prjpath.startswith(path):
                srcdir = os.path.normpath(path)        
        
        prjpath = prjpath[len(srcdir):]
        prjpath = prjpath.replace(os.path.sep, '_').strip('_')
        
        for dir in ('rd', 'fw4spl'):
            if dir in project_path:
                srcdir = dir
        
        kwargs = {
            "srcdir"  : srcdir,
            "type"    : type,
            "prjname" : prjname,
            "prjpath" : prjpath,
        }


        #create Install/Editor
        path_root = opjoin(racy.renv.dirs.install, 'Editor')

        if not os.path.exists(path_root):
            os.mkdir(path_root)

        #create Install/Editor/proj
        path_gen = opjoin(path_root, base_name)

        if not os.path.exists(path_gen):
            os.mkdir(path_gen)

        #create Install/Editor/proj/eclipse
        path_gen = opjoin(path_gen, self.var_name.lower())

        if not os.path.exists(path_gen):
            os.mkdir(path_gen)


        
        project_name = format.format(**kwargs)
        project_src  = os.path.join(self.get_rc_path(), PROJECT_FILE)
        cproject_src = os.path.join(self.get_rc_path(), CPROJECT_FILE)
        
        project_dest   = os.path.join(path_gen, PROJECT_FILE)
        cproject_dest  = os.path.join(path_gen, CPROJECT_FILE)
        
        
        if os.path.exists(project_dest) or os.path.exists(cproject_dest):
            racy.print_msg('project already exists in: ' + racy_project.base_name)
            return 0
        
        cmd = "make"
        if racy.renv.system() == 'windows':
            cmd = "racy.bat"
        else:
            cmd = "racy"
            
        if not os.path.exists(project_path):
            return -1
        
        #exemple:
        #$PFX_PRJNAME = lib-fwCore
        #$PRJNAME = fwCore
        #$CMD = racy.bat
        #$ID_CCONFIG_1 = 1293762299
        #$ID_CCONFIG_2 = 531078234
        #$ID_PROJECT = 3753198652
        
        random.seed()
        rand_range = [100000000, 9999999999]
        rand_id_1 = random.randint(*rand_range);
        rand_id_2 = random.randint(*rand_range);
        rand_id_3 = random.randint(*rand_range);
        dico = dict(
                PFX_PRJNAME  = project_name,
                PRJNAME      = racy_project.base_name,
                CMD          = cmd,
                ID_CCONFIG_1 = str(rand_id_1),
                ID_CCONFIG_2 = str(rand_id_2),
                ID_PROJECT   = str(rand_id_3)
                )
        
        ##########################################
        # configure .cproject file
        ##########################################       
        in_file = open(project_src, "r")
        out_file = open(project_dest, "w")
        
        tpl = Template(in_file.read())
        in_file.close()
        res_tpl = tpl.safe_substitute(dico)
        out_file.write(res_tpl) 
        out_file.close()
        ##########################################
        
        
        ##########################################
        # configure .cproject file
        ##########################################      
        in_file  = open(cproject_src, "r")
        out_file = open(cproject_dest, "w")
        
        tpl = Template(in_file.read())
        in_file.close()
        res_tpl = tpl.safe_substitute(dico)
        out_file.write(res_tpl)
            
        out_file.close()
        ##########################################

        
    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        deps = self.rec_deps
        
        if self.get_lower(self.var_name) == "clean" :
            self.clean_project(self)
        else:
            self.create(self)

        return result

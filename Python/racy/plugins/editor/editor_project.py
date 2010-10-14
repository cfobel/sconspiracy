import os
import shutil
import string
import random

from string  import Template
from os.path import join as opjoin
from glob    import glob
import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once

from qtcreator import QtCreatorProject
from eclipse   import EclipseProject

class EditorProjectError(racy.RacyProjectError):
    pass

EDITOR_PLUGIN_PATH = os.path.dirname(__file__)
CPROJECT_FILE = ".cproject"
PROJECT_FILE  = ".project"


class EditorProject(ConstructibleRacyProject):
    
    var_name = 'EDITOR'
    path_project = "EDITOR_GEN"

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = 'Editor take a ConstructibleRacyProject as first argument'
            raise EditorProjectError(self, msg)

        opts = prj.opts_source

        super(EditorProject, self).__init__(
                                        build_options = opts,
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )
                                          
    @property
    def name (self):
        name = super(EditorProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(EditorProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result
    

    def listdir(self,path,root_path ): 
        directory = []

        l = glob(path+'\\*') 

        for i in l: 
            if os.path.isdir(i):
                tmp = i.replace(root_path, '')
                directory.append(tmp[1:])
                directory.extend(self.listdir(i, root_path))
        return directory

    

    def get_rc_path(self):
        return opjoin(EDITOR_PLUGIN_PATH, 'rc')

        
    def clean_project(self, racy_project):
        project_path   = os.path.normpath(racy_project.root_path)
        project_dest   = os.path.join(project_path, PRO_FILE) 
        if os.path.exists(project_dest):
            os.remove(project_dest)
            racy.print_msg('remove: ' + project_dest)

    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        deps = self.rec_deps

        type = self.get_lower(self.var_name)
        if type == "clean" :
            self.clean_project(self)
        else:

            if type == "qtcreator":
                project = QtCreatorProject(self)
                project.install()

            if type == "eclipse":
                project = EclipseProject(self)
                project.install()
        
        
        return result

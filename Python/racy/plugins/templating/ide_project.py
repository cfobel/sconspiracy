import os
import shutil
import string

from os.path import join as opjoin
import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once
from global_dico import *
from templating  import *

class IdeProjectError(racy.RacyProjectError):
    pass

class IdeProject(ConstructibleRacyProject):
    
    var_name = 'IDE_PRJ'
    prj = ''

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = 'IDE take a ConstructibleRacyProject as first argument'

            raise IdeProjectError(self, msg)

        opts = prj.opts_source

        self.prj = prj
        self.graphviz_buffer = ''

        super(IdeProject, self).__init__(
                                        build_options = opts,
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )


    @property
    def name (self):
        name = super(IdeProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(IdeProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result
    
    def split_project_path(self, path):
        
        res = []
        for i in racy.renv.dirs.code:
            if path.startswith(i):
                temp = path.replace(i, '')
                def_dir = i.split(os.path.sep)[-1]

        res = temp.split(os.path.sep)
        res[0] = def_dir
        
        return res


    def create_prj (self, prj):


        # This dictionary contains all supported ide

       
        prj_deps = []
        

        for i in prj.rec_deps:
            if i.get_lower('TYPE') == 'bin_libext':
                target = ''
            else:
                target = i.target_path 

            prj_deps.append( { 'PRJ_NAME' : i.base_name , 
                'PRJ_TYPE' : i.get_lower('TYPE'), 'PRJ_TARGET': target, })
            

        # this dictionary contains all varibles for templates
        dico = {
            'PRJ_INSTALL_DIR' : prj.install_path,
            'PRJ_ROOT_DIR'    : prj.root_path,
            'PRJ_NAME'        : prj.base_name,
            'PRJ_TARGET'      : prj.target_path,
            'HEADERS'         : prj.get_includes(False),
            'SOURCES'         : prj.get_sources(False),
            'OTHERS_FILE'     : prj.get_others(),
            'PRJ_TYPE'        : prj.get_lower('TYPE'),
            'RACY_CLEAN_CMD'  : racy.get_racy_cmd() +' '+ prj.base_name,
            'CALLING_PROJECT' : self.prj.base_name,
            'DEPS_INCLUDES'   : prj.deps_include_path,
            'DEPS'            : prj_deps,
            'PROJECT_SPLIT_PATH' : self.split_project_path(prj.root_path), 
            }
        print self.prj.target_path




        dico.update(dico_g)

        deps = prj.rec_deps
        compiler_path = opjoin(racy.get_bin_path(), 'racy')


        ide_type = self.prj.get_lower('IDE')
        dico_vars = dico

        #Create user_prj_name
        prj_format = self.prj.get_lower('PRJ_USER_FORMAT')
        prj_format = prj_format.replace('(', '{')
        prj_format = prj_format.replace(')', '}')
        prj_format = prj_format.upper()


        dico_vars['PRJ_USER_FORMAT'] = apply_template(
                                        prj_format,dico_vars) 

        dico_prj = get_dico_prj(dico_prj_template['dico_ide'], ide_type)
        
        # Added vars 
        if dico_prj.has_key('vars'):
                dico_vars_template = add_vars(dico_prj['vars'], dico_vars)
        
        racy.print_msg('Create {0} project : {1}'.format(
                                    ide_type , prj.base_name))


        # Added dirs
        if dico_prj.has_key('dirs'):
            dico_vars= add_dirs_template(dico_prj['dirs'], dico_vars)

         # Added template_prj
        if dico_prj.has_key('template_prj'):
            add_template_prj(dico_prj['template_prj'], dico_vars)



    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        
        
        for i in self.prj.rec_deps:
            if i.type in ['exec', 'bundle', 'shared']:
                self.create_prj(i)

        self.create_prj(self.prj)

        return result

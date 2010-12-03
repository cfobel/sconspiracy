import os
import shutil
import string
import uuid
from os.path import join as opjoin
import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once
from global_dico import *
from templating  import *

class WixProjectError(racy.RacyProjectError):
    pass

class WixProject(ConstructibleRacyProject):
    
    var_name = 'WIX_PRJ'
    prj = ''
    call_prj_deps ={}
    qt = False
    wx = False

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = 'WIX take a ConstructibleRacyProject as first argument'

            raise WixProjectError(self, msg)

        opts = prj.opts_source

        self.prj = prj
        self.graphviz_buffer = ''
        

        super(WixProject, self).__init__(
                                        build_options = opts,
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )


    @property
    def name (self):
        name = super(WixProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(WixProject, self).configure_env()

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
            prj_deps.append( { 'PRJ_NAME' : i.base_name , 
                'PRJ_TYPE' : i.get_lower('TYPE'), })
        
        self.call_prj_deps[prj.base_name] = { 
                    'PRJ_NAME'      : prj.base_name,
                    'PRJ_FULL_NAME' : prj.full_name,
                    'PRJ_VERSION_NAME' : prj.versioned_name,
                    'PRJ_TYPE'      : prj.get_lower('TYPE'), 
                    'PRJ_TARGET'    : prj.target_path,
                    'GUID'          : uuid.uuid4(),
                    }

 
        # this dictionary contains all varibles for templates
        dico = {
            'PRJ_INSTALL_DIR' : prj.install_path,
            'PRJ_VERSION_NAME' : prj.versioned_name,
            'PRJ_ROOT_DIR'    : prj.root_path,
            'PRJ_NAME'        : prj.base_name,
            'PRJ_FULL_NAME'   : prj.full_name,
            'HEADERS'         : prj.get_includes(False),
            'SOURCES'         : prj.get_sources(False),
            'OTHERS_FILE'     : prj.get_others(),
            'PRJ_TYPE'        : prj.get_lower('TYPE'),
            'RACY_CLEAN_CMD'  : racy.get_racy_cmd() +' '+ prj.base_name,
            'CALLING_PROJECT' : self.prj.base_name,
            'CALLING_PROJECT_VERSION_NAME' : self.prj.versioned_name,
            'CALLING_PROJECT_FULL_NAME' : self.prj.full_name,
            'CALLING_PROJECT_DEPS' : self.call_prj_deps,
            'DEPS_INCLUDES'   : prj.deps_include_path,
            'VERSION'         : prj.version,
            'DEPS'            : prj_deps,
            'PROJECT_SPLIT_PATH' : self.split_project_path(prj.root_path), 
            }




        dico.update(dico_g)

        deps = prj.rec_deps
        compiler_path = opjoin(racy.get_bin_path(), 'racy')


        dico_vars = dico
        dico_prj  = dico_prj_template['dico_create_wix']['true'] 
        dico_vars = self.gen_file(dico_vars, dico_prj)

        dest_file = dico_vars[dico_vars["TEMP_DIR"] + "/call.wxs"]
        #os.system("candle.exe " + dico_vars['PRJ_NAME'] + '.wxs')
        #os.system("light.exe "  + dico_vars['PRJ_NAME'] + '.wixobj')
 
       
        if dico_vars['PRJ_NAME'] == dico_vars['CALLING_PROJECT']:
            os.system("candle.exe " +
            dico_vars['CALLING_PROJECT_FULL_NAME'] + '.wxs')
         #   os.system("light.exe -ext WixUIExtension -cultures:en-us "  + 
          #  dico_vars['CALLING_PROJECT_FULL_NAME'] + '.wixobj') 


    def create_libext(self,prj):
        targets = self.create_target(prj)

        if not targets == []:
 
            self.call_prj_deps[prj.base_name] = { 
                    'PRJ_NAME'      : prj.base_name,
                    'PRJ_FULL_NAME' : prj.full_name,
                    'PRJ_VERSION_NAME' : prj.versioned_name,
                    'PRJ_TYPE'      : prj.get_lower('TYPE'), 
                    }
           
            dico = {
                'PRJ_NAME' : prj.base_name,
                'PRJ_VERSION_NAME' : prj.versioned_name,
                'PRJ_FULL_NAME' : prj.full_name,
                'GUID' : uuid.uuid4(),
                'GUID1': uuid.uuid4(),
                'CALLING_PROJECT_VERSION_NAME' : self.prj.versioned_name,
                'CALLING_PROJECT' : self.prj.base_name,
                'TARGETS':  targets}

            dico.update(dico_g)
            
            dico_prj = {
                'dirs':
                    [
                        ('WIX_DIR'   ,'${WIX_INSTALL_DIR}/${CALLING_PROJECT}/'),
                        ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/'),
                        ('TEMP_DIR' , '${ROOT_TMP_DIR}/wix/'),
                    ],
                'template_prj':
                    [
                        ('${TEMP_DIR}/libext.wxs', '${WIX_DIR}/${PRJ_NAME}.wxs'),
                    ]
            }

            dico_vars = self.gen_file(dico, dico_prj)
            dest_file = dico_vars[dico_vars["TEMP_DIR"] + "/libext.wxs"]

        #    os.system("candle.exe " + dico_vars['PRJ_NAME'] + '.wxs')
         #   os.system("light.exe "  + dico_vars['PRJ_NAME'] + '.wixobj')

    def create_target(self, prj):
        targets = []
        
        if prj.base_name.count('_') > 0:
            base = prj.base_name.split('_')[0]
        else:
            base = prj.base_name
        dir_target = racy.renv.dirs.binpkg

        if prj.get_lower("DEBUG") == "full":
            dir_target = opjoin(dir_target, "debug")
        else:
            dir_target = opjoin(dir_target, "release")

#Exception pour Qt et Wx
        if base.startswith("wx") and self.qt== False:
            base ='wx'
            self.qt = True
        elif base.startswith("qt") and self.wx == False:
            base ='qt'
            self.wx = True


        tmp = dir_target
        for i in os.listdir(dir_target):
            if i.startswith(base):
                dir_target = opjoin(dir_target, i, 'bin')
        
        if dir_target == tmp:
            targets = []
        else:
            dir_depend = os.path.split(dir_target)[0]

            dir_depend,name = os.path.split(dir_depend)
            
            for i in os.listdir(dir_target)  :
                if not i.endswith('exe'):
                    targets.append(opjoin(dir_target,i))

                 
        
        return targets

        

    
    def gen_file(self, dico_vars, dico_prj):
        # Added vars 
        if dico_prj.has_key('vars'):
                dico_vars_template = add_vars(dico_prj['vars'], dico_vars)
        

        # Added dirs
        if dico_prj.has_key('dirs'):
            dico_vars= add_dirs_template(dico_prj['dirs'], dico_vars)

         # Added template_prj
        if dico_prj.has_key('template_prj'):
            add_template_prj(dico_prj['template_prj'], dico_vars)

        return dico_vars
    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        
        
        for i in self.prj.rec_deps:
            if i.get_lower('TYPE') in ['exec', 'bundle', 'shared']:
                self.create_prj(i)
            else:
                self.create_libext(i)

        self.create_prj(self.prj)
   
        return result

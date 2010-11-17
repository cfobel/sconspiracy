import os
import shutil
import string

from os.path import join as opjoin
import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once

from mako.template import Template

from mako import exceptions

from mako.exceptions import RichTraceback

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


    def apply_template(self, string, dico):
        temp = Template(string)
        res =''
        try:
            res = temp.render(**dico)
        except:
            print exceptions.text_error_template().render()

        return res
            
    def apply_file_template(self, name, dico):
        temp = Template(filename = name)
        res = ''
        try:
            res = temp.render(**dico)
        except:
            print exceptions.text_error_template().render()

        return res
 
    def add_vars(self, dico_vars_prj, dico_vars):
        for  key , value in dico_vars_prj:
            temp_key             = self.apply_template(key, dico_vars)
            dico_vars[temp_key]  = self.apply_template(value, dico_vars)
        return dico_vars

    def add_dirs(self, dico_dir, dico_vars):
        for  key , value in dico_dir:
            temp_key             = self.apply_template(key, dico_vars)
            dico_vars[temp_key]  = self.apply_template(value, dico_vars)

            if not os.path.exists(dico_vars[temp_key]):
                try:
                    os.makedirs(dico_vars[temp_key])
                   
                except:
                    pass   
        return dico_vars

    def add_template_prj(self, dico_template, dico_vars):
        for key , value in dico_template:
            temp_key             = self.apply_template(key, dico_vars)
            dico_vars[temp_key]  = self.apply_template(value, dico_vars)
            file_content = self.apply_file_template(temp_key, dico_vars)
            rutils.put_file_content(dico_vars[temp_key] , file_content)
 
    def create_prj (self, prj):


        # This dictionary contains all supported ide

        if os.name == 'nt':
            qt_default_dir = opjoin(os.environ['APPDATA'],'Nokia','qtcreator')
        else:
            qt_default_dir = opjoin(os.path.expanduser("~"),'.config',
                                            'Nokia', 'qtcreator')
        
        prj_deps = []
        for i in prj.rec_deps:
            prj_deps.append( { 'PRJ_NAME' : i.base_name , 
                'PRJ_TYPE' : i.get_lower('TYPE'), 'PRJ_TARGET': '' , })
            

        # this dictionary contains all varibles for templates
        dico = {
            'RACY_INSTALL_DIR': racy.renv.dirs.install,
            'PRJ_INSTALL_DIR' : prj.install_path,
            'PRJ_ROOT_DIR'    : prj.root_path,
            'IDE_INSTALL_DIR' : opjoin(racy.renv.dirs.install, 'ide'), 
            'PRJ_NAME'        : prj.base_name,
            'HEADERS'         : prj.get_includes(False),
            'SOURCES'         : prj.get_sources(False),
            'OTHERS_FILE'     : prj.get_others(),
            'RACY_CMD'        : racy.get_racy_cmd(),
            'RACY_CLEAN_CMD'  : racy.get_racy_cmd() +' '+ prj.base_name,
            'RACY_BIN_PATH'   : racy.renv.dirs.install_bin,
            'RACY_BUNDLE_PATH': racy.renv.dirs.install_bundle,
            'PRJ_TYPE'        : prj.get_lower('TYPE'),
            'OS_NAME'         : racy.renv.system(), #windows, darwin, linux
            'SEP'             : os.sep,
            'PATHSEP'         : os.pathsep,
            'IDE_PLUGIN_PATH' : os.path.dirname(__file__),
            'CALLING_PROJECT' : self.prj.base_name,
            'DEPS_INCLUDES'   : prj.deps_include_path,
            'DEPS'            : prj_deps,
            'CALLING_PROJECT_TARGET' : '',
            }


        dico_ide = {
       
        'qtcreator' :  
            {
                'dirs':
                    [
                        ('QT_DIR'   ,'${IDE_INSTALL_DIR}/qtcreator/${PRJ_NAME}/'),
                        ('TEMP_DIR' ,'${IDE_PLUGIN_PATH}/rc/qtcreator/'     ),
                        ('OS_DIR'   , qt_default_dir,                   ),
                    ]
                ,
                'template_prj':
                    [
                    
                        ('${TEMP_DIR}/template.pro'     , 
                                '${QT_DIR}/${PRJ_NAME}.pro'     ),
                        ('${TEMP_DIR}/template.pro.user',
                                '${QT_DIR}/${PRJ_NAME}.pro.user'),
                        ('${TEMP_DIR}/template.qws'     ,
                                '${OS_DIR}/${PRJ_NAME}.qws'     ),
                    ]
              
            },

        'eclipse' :
           { 
                'dirs':
                    [
                       ( 'EC_DIR'     , ('${IDE_INSTALL_DIR}/eclipse/'
                                         '${CALLING_PROJECT}/${PRJ_USER_FORMAT}/')
                       ),
                       ( 'LAUNCH_DIR' , ('${IDE_INSTALL_DIR}/eclipse/'
                                         '${CALLING_PROJECT}/.metadata/.plugins/'
                                          'org.eclipse.debug.core/.launches/')
                       ),
                       ( 'TEMP_DIR'   , '${IDE_PLUGIN_PATH}/rc/eclipse/'       ),
                    ]
                
                ,
                'template_prj':
                    [
                        ('${TEMP_DIR}/template.project'       ,
                            '${EC_DIR}/.project'               ),
                        ('${TEMP_DIR}/template.cproject'      ,
                           '${EC_DIR}/.cproject'               ),
                        ('${TEMP_DIR}/template_exec.launch' ,
                           '${LAUNCH_DIR}/exec.launch'         ),
                    ]
           },

        'graphviz' :
           {
                'dirs':
                    [
                       ( 'GRAPHVIZ_DIR' , ('${IDE_INSTALL_DIR}/graphviz/'
                                         '${CALLING_PROJECT}/'
                       )),
                       ( 'TEMP_DIR'   , '${IDE_PLUGIN_PATH}/rc/graphviz/'),
                    ],
                'template_prj':
                    [
                        ('${TEMP_DIR}/template.dot'            ,
                         '${GRAPHVIZ_DIR}/${CALLING_PROJECT}.dot'),
                    ]
           }
        }



        deps = prj.rec_deps
        compiler_path = opjoin(racy.get_bin_path(), 'racy')


        ide_type = self.prj.get_lower('IDE')
        dico_vars = dico

        #Create user_prj_name
        prj_format = self.prj.get_lower('PRJ_USER_FORMAT')
        prj_format = prj_format.replace('(', '{')
        prj_format = prj_format.replace(')', '}')
        prj_format = prj_format.upper()

        dico_vars['PRJ_USER_FORMAT'] = self.apply_template(
                                        prj_format,dico_vars) 


        # Added vars 
        if dico_ide[ide_type].has_key('vars'):
                dico_vars = self.add_vars(dico_ide[ide_type]['vars'], dico_vars)
        
        racy.print_msg('Create {0} project : {1}'.format(
                                    ide_type , prj.base_name))


        # Added dirs
        if dico_ide[ide_type].has_key('dirs'):
            dico_vars = self.add_dirs(dico_ide[ide_type]['dirs'], dico_vars)

         # Added template_prj
        if dico_ide[ide_type].has_key('template_prj'):
            self.add_template_prj(dico_ide[ide_type]['template_prj'], dico_vars)



    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        
        
        for i in self.prj.rec_deps:
            if i.type in ['exec', 'bundle', 'shared']:
                self.create_prj(i)

        self.create_prj(self.prj)

        return result

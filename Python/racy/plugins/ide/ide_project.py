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

    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)


        # This dictionary contains all supported ide

        if os.name == 'nt':
            qt_default_dir = opjoin(os.environ['APPDATA'],'Nokia','qtcreator')
            ext = '.bat'
            ext_exec = '.exe'
        else:
            qt_default_dir = opjoin(os.path.expanduser("~"),'.config',
                                            'Nokia', 'qtcreator')
            ext = ''
            ext_exec = ''

            ide_dir = opjoin(racy.renv.dirs.install, 'ide')

            # this dictionary contains all varibles for templates
            dico = {
                'INSTALL_DIR'     : racy.renv.dirs.install,
                'INSTALL_PRJ_DIR' : self.prj.install_path,
                'ROOT_DIR'        : self.prj.root_path,
                'IDE_DIR'         : ide_dir, 
                'PRJ_NAME'        : self.prj.base_name,
                'EXEC'            : self.prj.full_name + ext_exec,
                'EXEC_PATH'       : opjoin(self.prj.install_path, 
                                     self.prj.full_name) + ext_exec, 
                'HEADERS'         : self.prj.get_includes(False),
                'SOURCES'         : self.prj.get_sources(False),
                'COMPILE_CMD'     : opjoin(racy.get_bin_path(), 'racy') + ext,
                'CLEAN_CMD'       : opjoin(racy.get_bin_path(), 'racy') + ext +' '+ self.prj.base_name,
                'BIN_PATH'        : racy.renv.dirs.install_bin,
                'BUNDLE_PATH'     : racy.renv.dirs.install_bundle,
                'LAUNCHER_PATH'   : opjoin(racy.renv.dirs.install_bin,
                                    self.prj.projects_db['launcher'].full_name)
                                         + ext_exec,
                'TYPE'            : self.prj.get_lower('TYPE'),
                'PROFILE'         : opjoin(self.prj.install_path, 'profile.xml'),
                'OS'              : os.name,
                'OS_DIR'          : qt_default_dir,
                'IDE_PRJ_PATH'    : opjoin(ide_dir,self.prj.get_lower('IDE'),
                                    self.prj.base_name, self.prj.base_name),

                'PLUGIN_PATH'     : os.path.dirname(__file__),
                'ROOT_PROJECT'    : 'fwData',
                'DEPENDENCIES'    : [i.include_path for i in self.prj.rec_deps],

                }
            print dico['DEPENDENCIES']
            dico_ide = {
           
            'qtcreator' :  
                [
                    ('dirs',
                        [
                            ('QT_DIR'   ,'${IDE_DIR}/qtcreator/${PRJ_NAME}/'),
                            ('TEMP_DIR' ,'${PLUGIN_PATH}/rc/qtcreator/'      ),
                        ]
                    )
                    ,
                    ('vars',
                        [
                            ('DEPS' , [opjoin(ide_dir,  self.prj.get_lower('IDE')
                                    ,i.base_name, i.base_name)
                                     for i in self.prj.rec_deps],
                            )
                        ]
                    )
                    ,
                    ('template_prj',
                        [
                        
                            ('${TEMP_DIR}/template.pro'     , 
                                    '${QT_DIR}/${PRJ_NAME}.pro'     ),
                            ('${TEMP_DIR}/template.pro.user',
                                    '${QT_DIR}/${PRJ_NAME}.pro.user'),
                            ('${TEMP_DIR}/template.qws'     ,
                                    '${OS_DIR}/${PRJ_NAME}.qws'     ),
                        ]
                    )
                ],

            'eclipse' :
               [ 
                    ('dirs',
                        [
                           ( 'EC_DIR'   , '${IDE_DIR}/eclipse/${ROOT_PROJECT}/${PRJ_NAME}/'),
                           ( 'TEMP_DIR' , '${PLUGIN_PATH}/rc/eclipse/'       ),
                        ]
                    )
                    ,
                    ('template_prj',
                        [
                            ('${TEMP_DIR}/template.project'  ,
                                '${EC_DIR}/.project'             ),
                            ('${TEMP_DIR}/template.cproject' ,
                               '${EC_DIR}/.cproject'             ),
                        ]
                    )
               ]
            }



            deps = self.prj.rec_deps
            ide_dir = opjoin(racy.renv.dirs.install, 'ide')
            compiler_path = opjoin(racy.get_bin_path(), 'racy')



            if not (self.prj.get_lower('IDE').endswith('clean')):
                ide_type = self.prj.get_lower('IDE')

                racy.print_msg('Create {0} project : {1}'.format(ide_type , self.prj.base_name))

                dico_vars = dico 

               
                for i,j in dico_ide[ide_type]:
                    for k,l in j:
                        
                        if not i == 'vars':
                            temp_key = Template(k)
                            temp_key = temp_key.render(**dico_vars)
                            temp_value =  Template(l)
                            dico_vars[temp_key]  = temp_value.render(**dico_vars)
                        else:
                            dico_vars[k]  = l

                        if i == 'template_prj':
                            # Open template with mako
                            template = Template(filename = temp_key) 

                            #replace template with dictionary
                            template = template.render(**dico_vars)

                            
                            #destination file template
                            try:
                                dest_file = Template(os.path.normpath(dico_vars[temp_key]))
                                dest_file = dest_file.render(**dico_vars)
                            except:
                                print exceptions.text_error_template().render()

                            #open and write destination file
                            rutils.put_file_content(os.path.normpath(dest_file), template)
                        elif i == 'dirs' and not os.path.exists(dico_vars[temp_key]):
                            try:
                                os.makedirs(dico_vars[temp_key])
                            except:
                                pass


        return result

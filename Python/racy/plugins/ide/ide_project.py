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


        # if qtcreator defaulkt dir exist
        if os.path.exists(qt_default_dir):
            eclipse_launch = ('.metadata/.plugins/org.eclipse'
                                '.debug.core/.launches')
            dico_ide = {
           
            'qt' :  
                {
                'rc/qtcreator/template.pro'     :
                       '${IDE_DIR}/qtcreator/${PRJ_NAME}/${PRJ_NAME}.pro',
                'rc/qtcreator/template.pro.user':
                       '${IDE_DIR}/qtcreator/${PRJ_NAME}/${PRJ_NAME}.pro.user',
                'rc/qtcreator/template.qws'     :
                        opjoin(qt_default_dir, '${PRJ_NAME}.qws'),
                },

            'eclipse' :
                {
                'rc/eclipse/template.project' :
                       '${IDE_DIR}/eclipse/${PRJ_NAME}/.project',
                'rc/eclipse/template.cproject' :
                       '${IDE_DIR}/eclipse/${PRJ_NAME}/.cproject',
                'rc/eclipse/template.racy_config.launch' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch 
                       + '/racy_config.launch',
                'rc/eclipse/template.racy_BUILDDEPS=no.launch' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch
                       + '/racy_BUILDDEPS=no.launch',
                'rc/eclipse/template.racy.launch' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch
                       + '/racy.launch',
                 'rc/eclipse/template.racy_BUILDDEPS=no_config.launch' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch
                       + '/racy_BUILDDEPS=no_config.launch',
                  'rc/eclipse/template.launchConfigurationHistory.xml' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch
                       + '/launchConfigurationHistory.xml',
                  'rc/eclipse/template.racy_RELEASE_config.launch' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch
                       + '/racy_RELEASE_config.launch',
                   'rc/eclipse/template.racy_RELEASE.launch' :
                       '${IDE_DIR}/eclipse/' + eclipse_launch
                       + '/racy_RELEASE.launch',
                }


               }



            deps = self.prj.rec_deps
            ide_dir = opjoin(racy.renv.dirs.install, 'ide')
            compiler_path = opjoin(racy.get_bin_path(), 'racy')

            # This dictionary contains all varibles for templates
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
                'COMPILE_CMD'     : compiler_path + ext,
                'CLEAN_CMD'       : compiler_path + ext +' '+ self.prj.base_name,
                'BIN_PATH'        : racy.renv.dirs.install_bin,
                'BUNDLE_PATH'     : racy.renv.dirs.install_bundle,
                'LAUNCHER_PATH'   : opjoin(racy.renv.dirs.install_bin,
                                    self.prj.projects_db['launcher'].full_name)
                                         + ext_exec,
                'TYPE'            : self.prj.get_lower('TYPE'),
                'DEPS'            : [opjoin(ide_dir,  self.prj.get_lower('IDE')
                                    ,i.base_name, i.base_name)
                                     for i in deps],
                'PROFILE'         : opjoin(self.prj.install_path, 'profile.xml'),
                'OS'              : os.name,
                'IDE_PRJ_PATH'    : opjoin(ide_dir,self.prj.get_lower('IDE'),
                                    self.prj.base_name, self.prj.base_name)

                }


            ###
            # Creation  qtcreator file
            ###

            if(self.prj.get_lower('IDE') == 'qtcreator'):
                racy.print_msg('Create qtcreator project : ' + self.prj.base_name)
                
                install_dir = opjoin(dico['IDE_DIR'],'qtcreator', dico['PRJ_NAME'])

                # Create path to destination directorie
                if not os.path.exists(install_dir):
                    os.makedirs(install_dir)
                
                
                           
                for file in dico_ide['qt']:
                    # path to .pro template

                    temp = opjoin(os.path.dirname(__file__),
                            os.path.normpath(file))


                    if os.path.exists(temp):

                        # Open template with mako
                        template_pro = Template(filename = temp) 

                        #replace template with dictionary
                        template = template_pro.render(**dico)

                        #destination file template
                        dest_file = Template(os.path.normpath(dico_ide['qt'][file]))
                        dest_file = dest_file.render(**dico)

                        #open and write destination file
                        rutils.put_file_content(os.path.normpath(dest_file), template)
                    else:
                        racy.print_msg('the template : ' + temp  + ' doesn\'t exist')
            
            ###
            # Clean qtcreator file
            ###
            elif(self.prj.get_lower('IDE') == 'qtcreator-clean'):
                racy.print_msg('Remove qtcreator preferencies: '+
                        self.prj.base_name)        
                install_dir = opjoin(dico['IDE_DIR'],'qtcreator', dico['PRJ_NAME'])

                for file in dico_ide['qt'] :
                    #destination file template
                    dest_file = Template(os.path.normpath(dico_ide['qt'][file]))
               
                    try:
                        file = dest_file.render(**dico)
                        os.remove(file)
                    except  OSError:
                        racy.print_msg('file : ' + file + ' doesn\'t exist')

                try:
                    os.rmdir(install_dir)
                except OSError:
                    pass

                
                try:
                    os.rmdir(opjoin(dico['IDE_DIR'], 'qtcreator'))
                except OSError:
                    pass

            elif(self.prj.get_lower('IDE') == 'eclipse'):
                racy.print_msg('Create eclipse project : ' + self.prj.base_name)

                install_dir = opjoin(dico['IDE_DIR'],'eclipse', dico['PRJ_NAME'])
                # Create path to destination directory

                metadata_dir = opjoin(dico['IDE_DIR'], 'eclipse', '.metadata', '.plugins',
                        'org.eclipse.debug.core', '.launches')
                
                
                if not os.path.exists(install_dir):
                    os.makedirs(install_dir)
                
                if not os.path.exists(metadata_dir):
                    os.makedirs(metadata_dir)
                
                metadata_dir = opjoin(dico['IDE_DIR'], 'eclipse', '.metadata', '.plugins',
                        'org.eclipse.debug.ui')
                
                
                if not os.path.exists(metadata_dir):
                    os.makedirs(metadata_dir)

                           
                for file in dico_ide['eclipse']:
                    # path to .pro template

                    temp = opjoin(os.path.dirname(__file__),
                            os.path.normpath(file))


                    if os.path.exists(temp):

                        # Open template with mako
                        template_pro = Template(filename = temp) 
                        try:
                            #replace template with dictionary
                            template = template_pro.render(**dico)
                        except:
                            traceback = RichTraceback()
                            exit()
                                    
                            #destination file template
                        dest_file = Template(os.path.normpath(dico_ide['eclipse'][file]))
                        dest_file = dest_file.render(**dico)

                        #open and write destination file
                        rutils.put_file_content(os.path.normpath(dest_file), template)
             ###
            # Clean qtcreator file
            ###
            elif(self.prj.get_lower('IDE') == 'eclipse-clean'):
                racy.print_msg('Remove eclipse preferencies: '+
                        self.prj.base_name)        
                install_dir = opjoin(dico['IDE_DIR'],'eclipse', dico['PRJ_NAME'])

                for file in dico_ide['eclipse'] :
                    #destination file template
                    dest_file = Template(os.path.normpath(dico_ide['eclipse'][file]))
               
                    try:
                        file = dest_file.render(**dico)
                        os.remove(file)
                    except  OSError:
                        pass

                try:
                    os.rmdir(install_dir)
                except OSError:
                    pass

                
                try:
                    os.rmdir(opjoin(dico['IDE_DIR'], 'eclipse'))
                except OSError:
                    pass

            else:
                        racy.print_msg('the template : ' + temp  + ' doesn\'t exist')
 
                    
        else:
            racy.print_msg('Default qtcreator directory not found, please \
check your installation')

        return result

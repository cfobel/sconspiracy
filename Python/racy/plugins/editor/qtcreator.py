import os
import shutil
import string

from string  import Template
from os.path import join as opjoin
from glob    import glob
import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once

class QtCreatorProjectError(racy.RacyProjectError):
    pass

QTCREATOR_PLUGIN_PATH = os.path.dirname(__file__)
PREFIX = ' \\\n\t\t'

PREFIX_SESSION  = '<value type="QString">'
SUFFIXE_SESSION = '</value>\n'
DEFAULT_ARG =     '<valuelist key="ProjectExplorer.CustomExecutableRunConfiguration.Arguments" type="QVariantList"/>'
PREFIX_ARG ='<valuelist key="ProjectExplorer.CustomExecutableRunConfiguration.Arguments" type="QVariantList">\n'
SUFFIXE_ARG = '</valuelist>'
 

class QtCreatorProject(ConstructibleRacyProject):
    
    var_name = 'QTCREATOR_PRJ'
    prj = ''

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = 'QTcreator take a ConstructibleRacyProject as first argument'

            raise QtCreatorProjectError(self, msg)

        opts = prj.opts_source

        self.prj = prj

        super(QtCreatorProject, self).__init__(
                                        build_options = opts,
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )


    @property
    def name (self):
        name = super(QtCreatorProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(QtCreatorProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result
    
    def get_rc_path(self):
        return opjoin(QTCREATOR_PLUGIN_PATH, 'rc')

        
    def create(self):
        path = os.path.normpath(self.prj.root_path)
		
        base_dir = racy.renv.dirs.install
        base_name = self.prj.base_name
        src_dir = racy.renv.dirs.code

        path_root = opjoin(base_dir, 'Editor') 

        #create Install/Editor
        if not os.path.exists(path_root):
            os.mkdir(path_root)

        path_gen = opjoin(path_root, base_name)

        #create Install/Editor/proj
        if not os.path.exists(path_gen):
            os.mkdir(path_gen)

        path_gen = opjoin(path_gen, self.var_name.lower())

        #create Install/Editor/proj/qtcreator_prj
        if not os.path.exists(path_gen):
            os.mkdir(path_gen)

        launcher = ''
        for i in self.prj.source_deps:
            if i.full_name.startswith('launcher'):
                launcher = opjoin(i.install_path, i.full_name)

        
        self.create_project(self.prj, path_gen, launcher)
        


        deps = self.prj.rec_deps 
        #create .pro dependencies
      
        pro_depends = [opjoin(path_gen , self.prj.base_name + '.pro')]
        
        for i in deps:

            path_gen = opjoin(path_root, i.base_name)

            #create Install/Editor/proj
            if not os.path.exists(path_gen):
                os.mkdir(path_gen)

            path_gen = opjoin(path_gen, self.var_name.lower())

            #create Install/Editor/proj/qtcreator_prj
            if not os.path.exists(path_gen):
                os.mkdir(path_gen)
       
            base_name = i.base_name
            
            self.create_project(i, path_gen)
        
            pro_depends.append(opjoin(path_gen , i.base_name + '.pro'))
      
        self.create_session(self.prj, pro_depends)
        
    def create_project(self, prj, dest_prefix, launcher = ''):
    
        base_name = prj.base_name
        includes_dir= prj.include_path
        sources_dir = prj.src_path
        src_dir = includes_dir + sources_dir
        type = prj.type

        pro_name      = base_name + '.pro'
        pro_user_name = base_name + '.pro.user'
        
        src_pro_file  = opjoin(self.get_rc_path(), 'template.pro')
        dest_pro_file = opjoin(dest_prefix, pro_name )
        
        src_pro_user_file  = opjoin(self.get_rc_path(), 'template.pro.user')
        dest_pro_user_file = opjoin(dest_prefix, pro_user_name )

        
        install_path = prj.install_path 
        executable = install_path

        argument = ''
        os_ext = ''

        includes = map(str, self.prj.get_includes(False))
        sources = map(str, self.prj.get_sources(False))
        


        if type.lower() == 'exec' :
            
            executable = opjoin(executable, prj.full_name)
            
            if os.name == 'nt':
                os_ext = '.bat'
                executable = executable +  '.exe'

            argument = DEFAULT_ARG
        
        else:
            if type.lower() == 'bundle':
                executable = launcher 
                if os.name == 'nt':
                    os_ext = '.bat'
                    executable = executable + '.exe'       
                           
                    argument = PREFIX_ARG + PREFIX_SESSION

                    argument = argument + install_path 
                    
                    argument = opjoin(argument, 'profile.xml')

                    argument = argument + SUFFIXE_SESSION
                    argument = argument + SUFFIXE_ARG

        
        #create a dico to replace variable in template.pro 
        dico_pro = dict(
                   TARGET  = base_name,
                   DEPENDS = PREFIX.join(src_dir),
                   HEADERS = PREFIX.join(includes),
                   SOURCES = PREFIX.join(sources)
                )
        
        #write the .pro file
        template_file = open(src_pro_file  , 'r')
        apply_pro_file = open(dest_pro_file , 'w')

        temp = Template(template_file.read())
        template_file.close()

        res_temp = temp.safe_substitute(dico_pro)
        apply_pro_file.write(res_temp)
        apply_pro_file.close()

        #create a dico to replace variable in template.pro.user 
        dico_pro_user = dict(
                    ROOT_PATH   = prj.root_path,
                    NAME        = base_name,
                    EXEC        = executable,
                    EXT         = os_ext,
                    TARGET      = base_name, 
                    ARGUMENT    = argument ,
                    INSTALL_DIR = racy.renv.dirs.install,
                    )

        #write the .pro.user file
        template_file = open(src_pro_user_file  , 'r')
        apply_pro_user_file = open(dest_pro_user_file , 'w')

        temp = Template(template_file.read())
        template_file.close()

        res_temp = temp.safe_substitute(dico_pro_user)
        apply_pro_user_file.write(res_temp)
        apply_pro_user_file.close()

    def create_session(self, prj, lib):
        session_name      =  prj.base_name + '.qws'

        if os.name == 'nt':
            prefix_dest_file = opjoin(os.environ['APPDATA'],'Nokia','qtcreator')
        else:
            prefix_dest_file = opjoin(os.path.expanduser('~'), prefix_dest_file, '.config','Nokia','qtcreator')
            

        dest_file_name =  opjoin(prefix_dest_file, session_name)
        
        src_session_file  = opjoin(self.get_rc_path(), 'template_session.qws')
        dest_session_file = dest_file_name
        list_lib = []

        for l in lib:
            list_lib.append(PREFIX_SESSION + l + SUFFIXE_SESSION)

        dico_session = dict(
                   STARTUP_PRJ  = lib[0],
                   LIST_DEPS = '\t '.join(list_lib)
                )
        
        #write the .session file

        template_file = open(src_session_file  , 'r')
        apply_pro_file = open(dest_session_file , 'w')

        temp = Template(template_file.read())
        template_file.close()

        res_temp = temp.safe_substitute(dico_session)
        apply_pro_file.write(res_temp)
        apply_pro_file.close()

    

    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
      
        
        self.create()

        return result

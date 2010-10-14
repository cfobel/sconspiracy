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

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = 'QTcreator take a ConstructibleRacyProject as first argument'

            raise QtCreatorProjectError(self, msg)

        opts = prj.opts_source

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
    

    def listdir(self,path,root_path ): 
        directory = []

        l = glob(path+'\\*') 

        for i in l: 
            if os.path.isdir(i):
                tmp = i.replace(root_path, '')
                directory.append(opjoin(root_path, tmp[1:]))
                
                directory.extend(self.listdir(i, root_path))
        return directory

    def searchdir(self, dir, root_path):
        l = glob(root_path + '\\*')
        directory = [] 
        for i in l:
            if i == opjoin(root_path, dir):
                directory.append( opjoin(root_path, dir))
            else:
                directory.extend( self.searchdir(dir,i))
        
        
        return directory


    def searchfile(self, list_path, root_path):
        headers = []
        sources = []

        for i in list_path:
            tmp = opjoin(root_path, i)
            for j in os.listdir(tmp):
                if not os.path.isdir(j):
                    if j.endswith('.cpp'):
                        sources.append(opjoin(i , j))
                    else:
                        if j.endswith('.h') or j.endswith('.hpp'):
                            headers.append(opjoin(i , j))

            
        return headers, sources

    def get_rc_path(self):
        return opjoin(QTCREATOR_PLUGIN_PATH, 'rc')

        
    def clean_project(self, racy_project):
        project_path   = os.path.normpath(racy_project.root_path)
        project_dest   = os.path.join(project_path, PRO_FILE) 
        if os.path.exists(project_dest):
            os.remove(project_dest)
            racy.print_msg('remove: ' + project_dest)

    def create_session(self, lib, base_name):
    
        session_name      =  base_name + '.qws'
        prefix_dest_file = os.path.expanduser('~')

        if os.name == 'nt':
            prefix_dest_file = opjoin(prefix_dest_file, 'AppData\Roaming\Nokia\qtcreator')
        else:
            prefix_dest_file = opjoin(prefix_dest_file, '.config\Nokia\qtcreator')
            

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
        
        #write the .pro file
        template_file = open(src_session_file  , 'r')
        apply_pro_file = open(dest_session_file , 'w')

        temp = Template(template_file.read())
        template_file.close()

        res_temp = temp.safe_substitute(dico_session)
        apply_pro_file.write(res_temp)
        apply_pro_file.close()

        pass
    
    def create(self, racy_project):
        path = os.path.normpath(racy_project.root_path)
        
        base_dir = racy.renv.dirs.install
        base_name = racy_project.base_name
        src_dir = racy.renv.dirs.code
        version = racy_project.get_lower('VERSION')

        complete_name = ''
        

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

       

        self.create_project(path, racy_project.full_name, base_name, racy_project.type, path_gen, version)
        lib = [opjoin(path_gen,base_name + '.pro')]    
        lib_tmp =  list(racy_project._get_libnames('LIB'))
        lib_tmp.extend(racy_project._get_libnames('BUNDLES'))
        #create .pro dependencies

        for i in lib_tmp:
            i = (i.rsplit('_')[0])

            for directory in src_dir:
                tmp = self.searchdir(i, directory)
                complete_name = tmp
            
            path_gen = opjoin(path_root, i)

            #create Install/Editor/proj
            if not os.path.exists(path_gen):
                os.mkdir(path_gen)

            path_gen = opjoin(path_gen, self.var_name.lower())

            #create Install/Editor/proj/qtcreator_prj
            if not os.path.exists(path_gen):
                os.mkdir(path_gen)
       
            base_name = i
            #FIXME full_name doit changer en fonction de la dependance
            self.create_project(complete_name[0], racy_project.full_name, base_name, racy_project.type, path_gen, version)
            lib.append(opjoin(path_gen , base_name + '.pro'))
        #create .session
        base_name = racy_project.base_name
        self.create_session(lib, base_name)
        
    def create_project(self, root_path, full_name, base_name, type, dest_prefix = '', version = ''):
        pro_name      = base_name + '.pro'
        pro_user_name = base_name + '.pro.user'
        
        src_pro_file  = opjoin(self.get_rc_path(), 'template.pro')
        dest_pro_file = opjoin(dest_prefix, pro_name )
        
        src_pro_user_file  = opjoin(self.get_rc_path(), 'template.pro.user')
        dest_pro_user_file = opjoin(dest_prefix, pro_user_name )

        executable = ''
        argument = ''
        os_ext = ''
 
        if type.lower() == 'exec' :
            executable = opjoin(racy.renv.dirs.install,'bin')
            temp = full_name.lstrip('QTCREATOR_PRJ_')
            
            if os.name == 'nt':
                os_ext = '.bat'
                executable = executable +  '.exe'

            executable = opjoin(executable, temp)
            argument = DEFAULT_ARG
        
        else:
            if type.lower() == 'bundle':
                    executable = opjoin(racy.renv.dirs.install,'bin')
                    
                    temp =[] 
                    if os.name == 'nt':
                        temp = glob(opjoin(executable,'launcher*.exe'))
                        os_ext = '.bat'
                    else:
                        temp =  glob(opjoin(executable,'launcher*'))

                    executable = temp[0]
                    
                    argument = PREFIX_ARG + PREFIX_SESSION

                    tmp = opjoin(racy.renv.dirs.install, 'Bundles')
                    argument = argument + tmp
                    
                    name = base_name + '_' + version 
                    print name
                    argument = opjoin(argument, name)
                    argument = opjoin(argument, 'profile.xml')

                    argument = argument + SUFFIXE_SESSION
                    argument = argument + SUFFIXE_ARG
                    print argument

    
        sub_dir = self.listdir(root_path, root_path)
        headers,sources = self.searchfile(sub_dir, root_path )
       
        #create a dico to replace variable in template.pro 
        dico_pro = dict(
                   TARGET  = base_name,
                   DEPENDS = PREFIX.join(sub_dir),
                   HEADERS = PREFIX.join(headers),
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
                    ROOT_PATH = root_path,
                    NAME      = base_name,
                    EXEC      = executable,
                    EXT       = os_ext,
                    TARGET    = base_name, 
                    ARGUMENT  = argument 
                    )

        #write the .pro.user file
        template_file = open(src_pro_user_file  , 'r')
        apply_pro_user_file = open(dest_pro_user_file , 'w')

        temp = Template(template_file.read())
        template_file.close()

        res_temp = temp.safe_substitute(dico_pro_user)
        apply_pro_user_file.write(res_temp)
        apply_pro_user_file.close()

    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)
        deps = self.rec_deps
        
        if self.get_lower(self.var_name) == "clean" :
            self.clean_project(self)
        else:
            self.create(self)

        return result

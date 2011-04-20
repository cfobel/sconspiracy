import os
import uuid
import functools
from os.path import join as opjoin
import racy
import glob 
import os.path 


from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import memoize, run_once
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
                    }

        profile_without_rc = self.prj.get('WIX_PROFILE').replace("rc",'')
        profile_without_rc = profile_without_rc[1:]
        profile_path = os.path.join('Bundles', self.prj.versioned_name,
                                            profile_without_rc)
        icon_path = self.prj.get('WIX_ICON')
        if icon_path:
            icon_path = self.prj.get_path(icon_path)


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
            'CALLING_PROJECT_VERSION' : self.prj.version,
            'CALLING_PROJECT_PROFILE' : profile_path,
            'CALLING_PROJECT_ICON' : icon_path,
            'DEPS_INCLUDES'   : prj.deps_include_path,
            'VERSION'         : prj.version,
            'ARCH'         : self.prj.get_lower('ARCH'),
            'DEPS'            : prj_deps,
            'PROJECT_SPLIT_PATH' : self.split_project_path(prj.root_path),
            'uuid' : functools.partial(uuid.uuid5, uuid.NAMESPACE_OID),
            }

        dico.update(dico_g)

        dico_vars = dico
        dico_prj  = dico_prj_template['dico_create_wix']['yes']
        dico_vars = self.gen_file(dico_vars, dico_prj)

        racy.print_msg("Create {0} wix file".format(prj.base_name))

    def create_extra_dir(self, tuple_dir_targets):
        folder,targets = tuple_dir_targets

        if not targets == []:

            self.call_prj_deps[folder] = {
                    'PRJ_NAME'      : '',
                    'PRJ_FULL_NAME' : '',
                    'PRJ_VERSION_NAME' : '',
                    }

            dico = {
                'CALLING_PROJECT_VERSION_NAME' : self.prj.versioned_name,
                'CALLING_PROJECT' : self.prj.base_name,
                'TARGETS':  targets,
                'uuid' : functools.partial(uuid.uuid5, uuid.NAMESPACE_OID),
                'EXTRA_NAME' : folder,
                'ARCH'         : self.prj.get_lower('ARCH'),
            }

            dico.update(dico_g)

            dico_prj = {
                'dirs':
                    [
                        ('WIX_DIR'   ,'${WIX_INSTALL_DIR}/${CALLING_PROJECT}/'),
                        ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/'),
                        ('TPL_DIR' , '${ROOT_TMP_DIR}/wix/'),
                    ],
                'template_prj':
                    [
                        ('${TPL_DIR}/extra.wxs', '${WIX_DIR}/${EXTRA_NAME}.wxs'),
                    ]
            }

            self.gen_file(dico, dico_prj)
        racy.print_msg("Create "+ folder+ " wix file")

#    def create_targets(path,self):
#        targets = []
#
#        for i in os.listdir(bin_dir):
#            if not i.endswith('.exe'):
#                targets.append(os.path.join(bin_dir,i))
#
#
#        return targets
#
    def create_targets(self,path):
        targets=[]
        l = glob.glob(path+'\\*')
        for i in l:
            if os.path.isdir(i):
                targets.extend(self.create_targets(i))
            else:
                if not i.endswith('.exe'):
                    targets.append(i)
        return targets


    def create_install_targets(self,list_dir):
        # list targets = [(dir, list_targets),...]
        list_targets = []
        install_dir = racy.renv.dirs.install

        for tdir in list_dir:
            dir_path = opjoin(install_dir,tdir)

            if os.path.exists(dir_path):
                targets = self.create_targets(dir_path)
                list_targets.append((tdir,targets)) 

        return list_targets

    def gen_file(self, dico_vars, dico_prj):
        # Added vars 
        if dico_prj.has_key('vars'):
            dico_vars = add_vars(dico_prj['vars'], dico_vars)


        # Added dirs
        if dico_prj.has_key('dirs'):
            dico_vars = add_dirs_template(dico_prj['dirs'], dico_vars)

         # Added template_prj
        if dico_prj.has_key('template_prj'):
            add_template_prj(dico_prj['template_prj'], dico_vars)

        return dico_vars

    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)


        for i in self.prj.rec_deps:
            if i.get_lower('TYPE') in ['exec', 'bundle', 'shared']:
                self.create_prj(i)

        extra_dirs = ['bin','Python','PythonHome']

        for i in self.create_install_targets(extra_dirs):
            self.create_extra_dir(i)

        self.create_prj(self.prj)

        return result



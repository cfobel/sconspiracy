
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

def symblink(src, name):
    if os.name == "posix":
        try:
            os.symlink(src, name)
        except:
            pass
    else:
        try:
            from win32file import CreateSymbolicLink
            CreateSymbolicLink(name, src)
        except:
            racy.print_error("Unsuported",
                             'your platform is not yet supported')
            exit(0)
        

class CmakeProjectError(racy.RacyProjectError):
    pass

class CMakeProject(ConstructibleRacyProject):
    
    var_name = 'CMAKE_PRJ'

    def __init__(self, prj, config=None, **kwargs):
        if not isinstance(prj,ConstructibleRacyProject):
            msg = 'IDE take a ConstructibleRacyProject as first argument'

            raise CmakeProjectError(self, msg)

        opts = prj.opts_source

        self.master_project = prj
        self.deps_set = set()
        self.qt_used = False

        super(CMakeProject, self).__init__(
                                        build_options = opts,
                                        config = config,
                                        **prj.projects_db.prj_args
                                        )


    @property
    def name (self):
        name = super(CMakeProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(CMakeProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result

    def inject_deps(self, deps):
        new_key = deps.base_name
        self.master_deps[new_key] = deps


    def create_cmake_file(self, prj):
        #Create user_prj_name
        prj_format = self.master_project.get_lower('PRJ_USER_FORMAT')
        prj_format = prj_format.replace('(', '{')
        prj_format = prj_format.replace(')', '}')
        prj_format = prj_format.upper()

        rec_deps = set(p for p in prj.rec_deps if not prj.get_lower('TYPE')
                        == 'libext')
        
        dico = {
            'MASTER_PRJ_NAME' : self.master_project.base_name,
            'MASTER_PRJ'      : self.master_project,
            'PROJECT'         : prj,
            'PRJ_NAME'        : prj.base_name,
            'PRJ_TYPE'        : prj.get_lower('TYPE'),
            'PRJ_DEPS'        : prj.rec_deps,
            'SYMBLINK'        : symblink
            }

        dico.update(dico_g)

        dico_vars = dico

        dico_vars['PRJ_USER_FORMAT'] = apply_template(
                                        prj_format,dico_vars) 

        dico_prj = get_dico_prj(dico_prj_template['dico_cmake'], 'yes')

        # Added vars 
        if dico_prj.has_key('vars'):
                dico_vars_template = add_vars_template(dico_prj['vars'], dico_vars)

        # Added dirs
        if dico_prj.has_key('dirs'):
            dico_vars= add_dirs_template(dico_prj['dirs'], dico_vars)

         # Added template_prj


        if dico_prj.has_key('template_prj'):
            add_template_prj(dico_prj['template_prj'], dico_vars)



    def verify_qt_in_deps(self,prj):
        if not self.qt_used:
            for deps in prj.bin_deps:
                if 'qt' in deps.full_name:
                    self.qt_used = True
                    self.qt_prj = deps
                    break

    def qt_in_deps(self,):
        return self.qt_used


    def create_qt_conf(self):
        qt_path = os.path.split(self.qt_prj.bin_path)[0]
        template_dict= {'QT_PKG_PATH': qt_path }
        content = apply_file_template(
                os.path.dirname(__file__) + '/rc/cmake/qt.conf',
                template_dict)

        rutils.put_file_content(qt_path + '/bin/qt.conf', content)


    def install (self, opts = ['rc', 'deps'] ):
        result = self.result(deps_results = 'deps' in opts)


        for i in self.master_project.rec_deps:
            if i.type in ['exec', 'bundle', 'shared']:
                racy.print_msg("Create {0} CMakeList.txt".format(i.base_name))
                self.verify_qt_in_deps(i)
                self.create_cmake_file(i)

        self.create_cmake_file(self.master_project)

        if self.qt_in_deps():
            self.create_qt_conf()
        exit(0)
        return result

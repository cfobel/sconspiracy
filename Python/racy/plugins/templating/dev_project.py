
import os
import sys

import shutil
import string

from os.path import join as opjoin
import racy
import racy.rutils as rutils

from racy.renv     import constants
from racy.rproject import ConstructibleRacyProject, LibName
from racy.rutils   import cached_property, memoize, run_once
from templating  import *
from global_dico import *

class DevProjectError(racy.RacyProjectError):

    pass

class DevProject:
    type='' 
    var_name = 'DEV_PRJ'


    def __init__(self,  config=None, **kwargs):
        pass
    @property
    def name (self):
        name = super(DevProject, self).name
        return LibName.SEP.join( [self.var_name, name])

    @run_once
    def configure_env(self):
        super(DevProject, self).configure_env()

    @memoize
    def result(self, deps_results=True):
        result = []
        self.configure_env()
        return result

    def create_prj(self,prj_name, prj_type):
        dico_vars = dico_g
        print prj_name

        dico_vars['PRJ_PATH'] = os.path.join(os.getcwd(), prj_name)
        dico_vars['PRJ_TYPE'] = prj_type
        dico_vars['PRJ_NAME'] = prj_name

        dico_prj = get_dico_prj(dico_prj_template['dico_create_prj'], prj_type)

        # Added vars 
        if dico_prj.has_key('vars'):
                dico_vars_template = add_vars(dico_prj['vars'], dico_vars)
        
        racy.print_msg('Create {0} project'.format(
                                    prj_type))


        # Added dirs
        if dico_prj.has_key('dirs'):
            dico_vars= add_dirs_template(dico_prj['dirs'], dico_vars)

         # Added template_prj
        if dico_prj.has_key('template_prj'):
            add_template_prj(dico_prj['template_prj'], dico_vars)




        return [True]
 
    def create_srv(self,srv_path):
        dico_vars = dico_g

        dico_vars['SRV_PATH'] = os.path.split(srv_path)[0]

        dico_vars['SRV_NAME'] = os.path.split(srv_path)[1]
        dico_vars['PRJ_NAME'] = os.path.split(os.getcwd())[1]

        dico_prj = get_dico_prj(dico_prj_template['dico_create_srv'],'srv')

        # Added vars 
        if dico_prj.has_key('vars'):
                dico_vars_template = add_vars_template(dico_prj['vars'], dico_vars)
        
        racy.print_msg('Create {0} project'.format(
                                    srv_path))


        # Added dirs
        if dico_prj.has_key('dirs'):
            dico_vars= add_dirs_template(dico_prj['dirs'], dico_vars)

         # Added template_prj
        if dico_prj.has_key('template_prj'):
            add_template_prj(dico_prj['template_prj'], dico_vars)




        return [True]
        

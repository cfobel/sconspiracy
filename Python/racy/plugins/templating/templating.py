import os
import os.path
from mako.template import Template
from mako import exceptions
from mako.exceptions import RichTraceback

import racy.rutils as rutils
def apply_template( string, dico):
    temp = Template(string)
    res =''
    try:
        res = temp.render(**dico)
    except:
        print exceptions.text_error_template().render()

    return res
        
def apply_file_template( name, dico):
    temp = Template(filename = name)
    res = ''
    try:
        res = temp.render(**dico)
    except:
        print exceptions.text_error_template().render()

    return res

def add_vars_template( dico_vars_prj, dico_vars):
    for  key , value in dico_vars_prj:
        temp_key             = apply_template(key, dico_vars)
        dico_vars[temp_key]  = apply_template(value, dico_vars)
    return dico_vars

def add_dirs_template( dico_dir, dico_vars):
    for  key , value in dico_dir:
        temp_key             = apply_template(key, dico_vars)
        dico_vars[temp_key]  = apply_template(value, dico_vars)

        if not os.path.exists(dico_vars[temp_key]):
            try:
                os.makedirs(dico_vars[temp_key])
               
            except:
                pass   
    return dico_vars

def add_template_prj( dico_template, dico_vars):
    for key , value in dico_template:
        temp_key             = apply_template(key, dico_vars)
        dico_vars[temp_key]  = apply_template(value, dico_vars)
        file_content = apply_file_template(temp_key, dico_vars)
        rutils.put_file_content(dico_vars[temp_key] , file_content)


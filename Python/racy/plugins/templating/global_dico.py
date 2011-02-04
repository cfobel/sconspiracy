import racy
import racy.renv
import os
import os.path
from os.path import join as opjoin



# this dictionary contains all varibles for templates
dico_g = {
    'RACY_INSTALL_DIR': racy.renv.dirs.install,
    'RACY_SRC_DIR'    : racy.renv.dirs.code,
    'IDE_INSTALL_DIR' : opjoin(racy.renv.dirs.install, 'ide'), 
    'WIX_INSTALL_DIR' : opjoin(racy.renv.dirs.install, 'wix'), 
    'RACY_CMD'        : racy.get_racy_cmd(),
    'RACY_BIN_PATH'   : racy.renv.dirs.install_bin,
    'RACY_BUNDLE_PATH': racy.renv.dirs.install_bundle,
    'OS_NAME'         : racy.renv.system(), #windows, darwin, linux
    'SEP'             : os.sep,
    'PATHSEP'         : os.pathsep,
    'IDE_PLUGIN_PATH' : os.path.dirname(__file__),
    'WIX_PLUGIN_PATH' : os.path.dirname(__file__),
    'CALLING_PROJECT_TARGET' : '',
}


if os.name == 'nt':
    qt_default_dir = opjoin(os.environ['APPDATA'],'Nokia','qtcreator')
else:
    qt_default_dir = opjoin(os.path.expanduser("~"),'.config',
                                    'Nokia', 'qtcreator')

dico_prj_template = {
    'dico_ide':
    {
        'options':
        {
            'default_value': 'none',
            'allowed_value': ['none', 'eclipse', 'qtcreator', 'graphviz','vim','msvs'],
            'commandline_prj_opts': True,
            'descriptions_opts': 
    """Preferencies formated project name.
    You can used this variable like this:
    $( VARIABLE )
    PRJ_NAME           : project base name.
    RACY_CMD           : racy command.
    PRJ_TYPE           : project type.
    OS_NAME            : os name.
    SEP                : os depend separator (/ or \\).
    PATHSEP            : path separator ( : ).
    CALLING_PROJECT    : the main project.
    PROJECT_SPLIT_PATH : list of element in prj_path,
                         the first element is the last directory
                         in RACY_SRC_DIR path.
    """,
        },

        'qtcreator' :  
        {
            'dirs':
                [
                    ('QT_DIR'   ,'${IDE_INSTALL_DIR}/qtcreator/${PRJ_NAME}/'),
                    ('TEMP_DIR' ,'${IDE_PLUGIN_PATH}/rc/qtcreator/'     ),
                    ('OS_DIR'   , qt_default_dir                   ),
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
          },
         'vim' :
         {
            'dirs':
                [
                   ( 'VIM_DIR' , ('${IDE_INSTALL_DIR}/vim/'
                                     '${CALLING_PROJECT}/'
                   )),
                   ( 'TEMP_DIR'   , '${IDE_PLUGIN_PATH}/rc/vim/'),
                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/vim.tagslist'            ,
                     '${VIM_DIR}/.${PRJ_NAME}_tagslist'),
                    ('${TEMP_DIR}/vim.project'            ,
                     '${VIM_DIR}/.${PRJ_NAME}_vimprj'),
                    ('${TEMP_DIR}/tmp.tagslist'            ,
                     '${VIM_DIR}/tagslist'),
                    ('${TEMP_DIR}/tmp.vimprj'            ,
                     '${VIM_DIR}/vimprj'),


                ]
          },
          'msvs' :
          {
              'dirs':
                [
                   ( 'MSVS_DIR' , ('${IDE_INSTALL_DIR}/msvs/'
                                     '${CALLING_PROJECT}/${PRJ_NAME}'
                   )),
                   ( 'TEMP_DIR'   , '${IDE_PLUGIN_PATH}/rc/msvs/'),
                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/temp.vcproj'            ,
                     '${MSVS_DIR}/${PRJ_NAME}.vcproj'),
                    ('${TEMP_DIR}/user.template'            ,
                     '${MSVS_DIR}/${PRJ_NAME}.vcproj.user'),

                    ('${TEMP_DIR}/temp.sln'            ,
                     '${IDE_INSTALL_DIR}/msvs/'
                           '${CALLING_PROJECT}/${CALLING_PROJECT}.sln'),
                ]
          }
    }
    ,
    'dico_prj_user_format':
    {
        'options':
        {
            'default_value' : '$(PRJ_TYPE)_$(PRJ_NAME)',
            'commandline_prj_opts': True,
            'commandline_opts': True,
            'descriptions_opts':"Create new developer project",
        },

    }
    ,
    'dico_create_prj':
    {
        'options':
        {
            'commandline_prj_opts': True,
            'commandline_opts': False,
            'descriptions_opts':"Create new developer project",
        },
        'exec':
        {

            'dirs':
                [
                    ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/dev/'),
                    ('TEMP_DIR' , '${ROOT_TMP_DIR}/exec/'),
                    ('LICENSE_TMP_DIR', '${ROOT_TMP_DIR}/licenses/'),
                    ('SRC_DIR', '${PRJ_PATH}/src/${PRJ_NAME}'),
                    ('INCLUDE_DIR', '${PRJ_PATH}/include/${PRJ_NAME}'),
                    ('BIN_DIR', '${PRJ_PATH}/bin'),
                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/main.cpp', '${SRC_DIR}/main.cpp'),
                    ('${ROOT_TMP_DIR}/bin/build.options', '${BIN_DIR}/build.options'),
                    ('${LICENSE_TMP_DIR}/COPYING', '${PRJ_PATH}/COPYING'),
                    ('${LICENSE_TMP_DIR}/COPYING.LESSER', '${PRJ_PATH}/COPYING.LESSER'),
                ]
        },
        'bundle':
        {

            'dirs':
                [
                    ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/dev/'),
                    ('TEMP_DIR' , '${ROOT_TMP_DIR}/bundle/'),
                    ('LICENSE_TMP_DIR', '${ROOT_TMP_DIR}/licenses/'),
                    ('SRC_DIR', '${PRJ_PATH}/src/${PRJ_NAME}'),
                    ('RC_DIR', '${PRJ_PATH}/rc/'),
                    ('INCLUDE_DIR', '${PRJ_PATH}/include/${PRJ_NAME}'),
                    ('BIN_DIR', '${PRJ_PATH}/bin'),

                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/config.hpp', '${INCLUDE_DIR}/config.hpp'),
                    ('${TEMP_DIR}/plugin.hpp', '${INCLUDE_DIR}/Plugin.hpp'),
                    ('${TEMP_DIR}/plugin.cpp', '${SRC_DIR}/Plugin.cpp'),
                    ('${TEMP_DIR}/plugin.xml', '${RC_DIR}/plugin.xml'),
                    ('${TEMP_DIR}/namespace.hpp','${INCLUDE_DIR}/namespace.hpp'),
                    ('${ROOT_TMP_DIR}/bin/build.options', '${BIN_DIR}/build.options'),
                    ('${LICENSE_TMP_DIR}/COPYING', '${PRJ_PATH}/COPYING'),
                    ('${LICENSE_TMP_DIR}/COPYING.LESSER', '${PRJ_PATH}/COPYING.LESSER'),
                ]
        },
        'shared':
        {
            'dirs':
                [
                    ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/dev/'),
                    ('TEMP_DIR' , '${ROOT_TMP_DIR}/bundle/'),
                    ('LICENSE_TMP_DIR', '${ROOT_TMP_DIR}/licenses/'),
                    ('SRC_DIR', '${PRJ_PATH}/src/${PRJ_NAME}'),
                    ('INCLUDE_DIR', '${PRJ_PATH}/include/${PRJ_NAME}'),
                    ('BIN_DIR', '${PRJ_PATH}/bin'),

                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/config.hpp', '${INCLUDE_DIR}/config.hpp'),
                    ('${ROOT_TMP_DIR}/bin/build.options', '${BIN_DIR}/build.options'),
                    ('${LICENSE_TMP_DIR}/COPYING', '${PRJ_PATH}/COPYING'),
                    ('${LICENSE_TMP_DIR}/COPYING.LESSER', '${PRJ_PATH}/COPYING.LESSER'),
                ]


        },
    }
    ,
    'dico_create_srv':
    {
        'options':
        {
            
            'commandline_prj_opts': True,
            'commandline_opts': True,
            'descriptions_opts':"Create new service",
        },

        'srv':
        {
            'dirs':
                [
                    ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/dev/'),
                    ('TEMP_DIR' , '${ROOT_TMP_DIR}/srv/'),
                    ('SRC_DIR', 'src/${PRJ_NAME}/'),
                    ('INCLUDE_DIR', 'include/${PRJ_NAME}/${SRV_PATH}/'),
                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/srv.hpp', '${INCLUDE_DIR}${SRV_NAME}.hpp'),
                    ('${TEMP_DIR}/namespace.hpp', '${INCLUDE_DIR}/namespace.hpp'),
                    ('${TEMP_DIR}/srv.cpp', '${SRC_DIR}${SRV_NAME}.cpp'),
                ]

        }
    }
    ,
    'dico_create_wix':
    {
        'options':
        {

            'default_value' : 'no',
            'commandline_prj_opts': True,
            'commandline_opts': False,
            'allowed_values' : ['yes' , 'no'],
            'descriptions_opts':"Create new wix installer",
        },

        'yes':
        {
            'dirs':
                [
                    ('WIX_DIR'   ,'${WIX_INSTALL_DIR}/${CALLING_PROJECT}/'),
                    ('ROOT_TMP_DIR', '${IDE_PLUGIN_PATH}/rc/'),
                    ('TEMP_DIR' , '${ROOT_TMP_DIR}/wix/'),
                ],
            'template_prj':
                [
                    ('${TEMP_DIR}/call.wxs',
                        '${WIX_DIR}/${CALLING_PROJECT_FULL_NAME}.wxs'),
                    ('${TEMP_DIR}/proj.wxs', '${WIX_DIR}/${PRJ_NAME}.wxs'),
                    ('${TEMP_DIR}/generate_msi.py',
                         '${WIX_DIR}/gen_msi_${CALLING_PROJECT_FULL_NAME}.py'),
                    ('${TEMP_DIR}/generate_msi.bat',
                         '${WIX_DIR}/gen_msi_${CALLING_PROJECT_FULL_NAME}.bat'),

                ]

        }

    }
    ,
    'dico_wix_profile':
    {
        'options':
        {

            'default_value' : 'rc/profile.xml',
            'commandline_prj_opts': True,
            'commandline_opts': False,
            'allowed_values' : [],
            'descriptions_opts':"Path to profile relative to project dir",
        },
    }
    ,
    'dico_wix_icon':
    {
        'options':
        {

            'default_value' : '',
            'commandline_prj_opts': True,
            'commandline_opts': False,
            'allowed_values' : [],
            'descriptions_opts':"Path to icon relative to project dir",
        },
    }

}

def get_dico_prj(dico, type):
    return dico[type]

def get_dico_prj_options(dico):
    res = {}
    for prj, attr in dico.items():


        if attr.has_key('options'):
            prj = prj.replace('dico_', '')
            prj = prj.upper()
            res[prj] = attr['options']

    return res




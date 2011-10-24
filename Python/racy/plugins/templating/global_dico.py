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
    'CMAKE_INSTALL_DIR': opjoin(racy.renv.dirs.install, 'cmake'), 
    'RACY_CMD'        : racy.get_racy_cmd(),
    'RACY_BIN_PATH'   : racy.renv.dirs.install_bin,
    'RACY_BUNDLE_PATH': racy.renv.dirs.install_bundle,
    'OS_NAME'         : racy.renv.system(), #windows, darwin, linux
    'SEP'             : os.sep,
    'PATHSEP'         : os.pathsep,
    'TEMPLATING_PLUGIN_PATH' : os.path.dirname(__file__),
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
            'allowed_value': ['none', 'eclipse', 'qtcreator','qtcreator2-2', 
                              'qtcreator2-3','graphviz','vim','msvs',
                              'eclipse-indigo'],
            'commandline_prj_opts': True,
            'descriptions_opts':"Create new developer project",
         },

        'qtcreator' :
        {

            'dirs':
                [
                    ('QT_DIR'   ,'${IDE_INSTALL_DIR}/qtcreator/${PRJ_NAME}/'),
                    ('TPL_DIR' ,'${TEMPLATING_PLUGIN_PATH}/rc/qtcreator/'     ),
                    ('OS_DIR'   , qt_default_dir                   ),
                ]
            ,
            'template_prj':
                [

                    ('${TPL_DIR}/template.pro'     ,
                            '${QT_DIR}/${PRJ_NAME}.pro'     ),
                    ('${TPL_DIR}/template.pro.user',
                            '${QT_DIR}/${PRJ_NAME}.pro.user'),
                    ('${TPL_DIR}/template.qws'     ,
                            '${OS_DIR}/${PRJ_NAME}.qws'     ),
                ]

        },
        'qtcreator2-2' :
        {

            'dirs':
                [
                    ('QT_DIR'   ,'${IDE_INSTALL_DIR}/qtcreator2-2/${PRJ_NAME}/'),
                    ('TPL_DIR' ,'${TEMPLATING_PLUGIN_PATH}/rc/qtcreator/' ),
                    ('TPL_2_2_DIR' ,'${TEMPLATING_PLUGIN_PATH}/rc/qtcreator2-2/' ),
                    ('OS_DIR'   , qt_default_dir                   ),
                ]
            ,
            'template_prj':
                [

                    ('${TPL_DIR}/template.pro'     ,
                            '${QT_DIR}/${PRJ_NAME}.pro'     ),
                    ('${TPL_2_2_DIR}/template_pro_user.mako',
                            '${QT_DIR}/${PRJ_NAME}.pro.user'),
                    ('${TPL_2_2_DIR}/template.qws'     ,
                            '${OS_DIR}/${PRJ_NAME}.qws'     ),
                ]

        },
        
        'qtcreator2-3' :
        {

            'dirs':
                [
                    ('QT_DIR'   ,'${IDE_INSTALL_DIR}/qtcreator2-3/${PRJ_NAME}/'),
                    ('TPL_DIR' ,'${TEMPLATING_PLUGIN_PATH}/rc/qtcreator/' ),
                    ('TPL_2_3_DIR' ,'${TEMPLATING_PLUGIN_PATH}/rc/qtcreator2-3/' ),
                    ('OS_DIR'   , qt_default_dir                   ),
                ]
            ,
            'template_prj':
                [

                    ('${TPL_2_3_DIR}/template_config.mako'     ,
                            '${QT_DIR}/${PRJ_NAME}.config'     ),
                    ('${TPL_2_3_DIR}/template_creator.mako'     ,
                            '${QT_DIR}/${PRJ_NAME}.creator'     ),
                    ('${TPL_2_3_DIR}/template_files.mako'     ,
                            '${QT_DIR}/${PRJ_NAME}.files'     ),
                    ('${TPL_2_3_DIR}/template_includes.mako'     ,
                            '${QT_DIR}/${PRJ_NAME}.includes'     ),
                    ('${TPL_2_3_DIR}/template_qws.mako'     ,
                            '${OS_DIR}/${CALLING_PROJECT}.qws'     ),
                    ('${TPL_2_3_DIR}/template_creator_user.mako'     ,
                            '${QT_DIR}/${PRJ_NAME}.creator.user'     ),
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
                   ( 'TPL_DIR'   , '${TEMPLATING_PLUGIN_PATH}/rc/eclipse/'       ),
                ]

            ,
            'template_prj':
                [
                    ('${TPL_DIR}/template.project'       ,
                        '${EC_DIR}/.project'               ),
                    ('${TPL_DIR}/template.cproject'      ,
                       '${EC_DIR}/.cproject'               ),
                    ('${TPL_DIR}/template_exec.launch' ,
                       '${LAUNCH_DIR}/exec.launch'         ),
                ]
         },

        'eclipse-inplace' :
        {
            'dirs':
                [
                   ( 'EC_DIR'     , ('${PRJ_ROOT_DIR}/')
                   ),
                   ( 'LAUNCH_DIR' , ('${IDE_INSTALL_DIR}/eclipse/'
                                     '${CALLING_PROJECT}/.metadata/.plugins/'
                                      'org.eclipse.debug.core/.launches/')
                   ),
                   ( 'TPL_DIR'   , '${TEMPLATING_PLUGIN_PATH}/rc/eclipse/'       ),
                ]

            ,
            'template_prj':
                [
                    ('${TPL_DIR}/template.project'       ,
                        '${EC_DIR}/.project'               ),
                    ('${TPL_DIR}/template.cproject'      ,
                       '${EC_DIR}/.cproject'               ),
                    ('${TPL_DIR}/template_exec.launch' ,
                       '${LAUNCH_DIR}/exec.launch'         ),
                ]
         },

        'eclipse-indigo' :
        { 
            'dirs':
                [
                   ( 'TPL_DIR'      , '${TEMPLATING_PLUGIN_PATH}/rc/eclipse-ind/'     ),
                   ( 'META_DIR'     , '${IDE_INSTALL_DIR}/indigo/.metadata/'   ),
                   ( 'META_PRJ_DIR' , "${META_DIR}.plugins/org.eclipse.core.resources/.projects/${PRJ_NAME}"
                                                                               ),
                   ( 'META_WORK_DIR', 
                        '${META_DIR}/.plugins/org.eclipse.ui.workbench/'       )
                ]

            ,
            'template_prj':
                [
                    ('${TPL_DIR}/project.mako'       ,
                        '${PRJ_ROOT_DIR}/.project'               ),
                    ('${TPL_DIR}/cproject.mako'      ,
                       '${PRJ_ROOT_DIR}/.cproject'               ),
                ]
         },
         'graphviz' :
         {
            'dirs':
                [
                   ( 'GRAPHVIZ_DIR' , ('${IDE_INSTALL_DIR}/graphviz/'
                                     '${CALLING_PROJECT}/'
                   )),
                   ( 'TPL_DIR'   , '${TEMPLATING_PLUGIN_PATH}/rc/graphviz/'),
                ],
            'template_prj':
                [
                    ('${TPL_DIR}/template.dot'            ,
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
                   ( 'TPL_DIR'   , '${TEMPLATING_PLUGIN_PATH}/rc/vim/'),
                ],
            'template_prj':
                [
                    ('${TPL_DIR}/vim.tagslist'            ,
                     '${VIM_DIR}/.${PRJ_NAME}_tagslist'),
                    ('${TPL_DIR}/vim.project'            ,
                     '${VIM_DIR}/.${PRJ_NAME}_vimprj'),
                    ('${TPL_DIR}/tmp.tagslist'            ,
                     '${VIM_DIR}/tagslist'),
                    ('${TPL_DIR}/tmp.vimprj'            ,
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
                   ( 'TPL_DIR'   , '${TEMPLATING_PLUGIN_PATH}/rc/msvs/'),
                ],
            'template_prj':
                [
                    ('${TPL_DIR}/temp.vcproj'            ,
                     '${MSVS_DIR}/${PRJ_NAME}.vcproj'),
                    ('${TPL_DIR}/user.template'            ,
                     '${MSVS_DIR}/${PRJ_NAME}.vcproj.user'),

                    ('${TPL_DIR}/temp.sln'            ,
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
            'descriptions_opts':
    """Preferencies formated project name.
    You can use this variable like this:
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
                    ('ROOT_TMP_DIR', '${TEMPLATING_PLUGIN_PATH}/rc/dev/'),
                    ('TPL_DIR' , '${ROOT_TMP_DIR}/exec/'),
                    ('LICENSE_TMP_DIR', '${ROOT_TMP_DIR}/licenses/'),
                    ('SRC_DIR', '${PRJ_PATH}/src/${PRJ_NAME}'),
                    ('INCLUDE_DIR', '${PRJ_PATH}/include/${PRJ_NAME}'),
                    ('BIN_DIR', '${PRJ_PATH}/bin'),
                ],
            'template_prj':
                [
                    ('${TPL_DIR}/main.cpp', '${SRC_DIR}/main.cpp'),
                    ('${ROOT_TMP_DIR}/bin/build.options', '${BIN_DIR}/build.options'),
                    ('${LICENSE_TMP_DIR}/COPYING', '${PRJ_PATH}/COPYING'),
                    ('${LICENSE_TMP_DIR}/COPYING.LESSER', '${PRJ_PATH}/COPYING.LESSER'),
                ]
        },
        'bundle':
        {

            'dirs':
                [
                    ('ROOT_TMP_DIR', '${TEMPLATING_PLUGIN_PATH}/rc/dev/'),
                    ('TPL_DIR' , '${ROOT_TMP_DIR}/bundle/'),
                    ('LICENSE_TMP_DIR', '${ROOT_TMP_DIR}/licenses/'),
                    ('SRC_DIR', '${PRJ_PATH}/src/${PRJ_NAME}'),
                    ('RC_DIR', '${PRJ_PATH}/rc/'),
                    ('INCLUDE_DIR', '${PRJ_PATH}/include/${PRJ_NAME}'),
                    ('BIN_DIR', '${PRJ_PATH}/bin'),

                ],
            'template_prj':
                [
                    ('${TPL_DIR}/config.hpp', '${INCLUDE_DIR}/config.hpp'),
                    ('${TPL_DIR}/plugin.hpp', '${INCLUDE_DIR}/Plugin.hpp'),
                    ('${TPL_DIR}/plugin.cpp', '${SRC_DIR}/Plugin.cpp'),
                    ('${TPL_DIR}/plugin.xml', '${RC_DIR}/plugin.xml'),
                    ('${TPL_DIR}/namespace.hpp','${INCLUDE_DIR}/namespace.hpp'),
                    ('${ROOT_TMP_DIR}/bin/build.options', '${BIN_DIR}/build.options'),
                    ('${LICENSE_TMP_DIR}/COPYING', '${PRJ_PATH}/COPYING'),
                    ('${LICENSE_TMP_DIR}/COPYING.LESSER', '${PRJ_PATH}/COPYING.LESSER'),
                ]
        },
        'shared':
        {
            'dirs':
                [
                    ('ROOT_TMP_DIR', '${TEMPLATING_PLUGIN_PATH}/rc/dev/'),
                    ('TPL_DIR' , '${ROOT_TMP_DIR}/bundle/'),
                    ('LICENSE_TMP_DIR', '${ROOT_TMP_DIR}/licenses/'),
                    ('SRC_DIR', '${PRJ_PATH}/src/${PRJ_NAME}'),
                    ('INCLUDE_DIR', '${PRJ_PATH}/include/${PRJ_NAME}'),
                    ('BIN_DIR', '${PRJ_PATH}/bin'),

                ],
            'template_prj':
                [
                    ('${TPL_DIR}/config.hpp', '${INCLUDE_DIR}/config.hpp'),
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
                    ('ROOT_TMP_DIR', '${TEMPLATING_PLUGIN_PATH}/rc/dev/'),
                    ('TPL_DIR' , '${ROOT_TMP_DIR}/srv/'),
                    ('SRC_DIR', 'src/${PRJ_NAME}/${SRV_PATH}/'),
                    ('INCLUDE_DIR', 'include/${PRJ_NAME}/${SRV_PATH}/'),
                ],
            'template_prj':
                [
                    ('${TPL_DIR}/srv.hpp', '${INCLUDE_DIR}${SRV_NAME}.hpp'),
                    ('${TPL_DIR}/namespace.hpp', '${INCLUDE_DIR}/namespace.hpp'),
                    ('${TPL_DIR}/srv.cpp', '${SRC_DIR}${SRV_NAME}.cpp'),
                ]

        }
    }
    ,
    'dico_cmake':
    {
        'options':
        {
            
            'commandline_opts': False,
            'default_value' : 'no',
            'commandline_prj_opts': True,
            'allowed_values':['yes', 'no'],
            'descriptions_opts':"Create new cmakelist",
        },

        'yes':
        {
            'dirs':
                [
                   ( 'CMAKE_DIR' ,
                    '${CMAKE_INSTALL_DIR}/${MASTER_PRJ.base_name}/'
                    '${PRJ_NAME + "/" if not PRJ_NAME == MASTER_PRJ_NAME else ""}'
                   ),
                   ( 'TEMPLATE_DIR' , '${TEMPLATING_PLUGIN_PATH}/rc/cmake'),
                   ('CMAKE_BUILD_DIR',
                    '${CMAKE_INSTALL_DIR}/${MASTER_PRJ.base_name}/build/'),
                   ('CMAKE_INSTALL_OUTPUT',
                    '${CMAKE_INSTALL_DIR}/Install/'
                   ),
                   ('CMAKE_MACRO_DIR',
                       '${CMAKE_INSTALL_DIR}/${MASTER_PRJ.base_name}/.cmake_macro/')

                ],
            'template_prj':
                [
                    ('${TEMPLATE_DIR}/cmakelists.mako',
                     '${CMAKE_DIR}/CMakeLists.txt'),
                ],
            'copy_file':
                [
                    ('${TEMPLATE_DIR}/macro/macro.cmake',
                     '${CMAKE_MACRO_DIR}/macro.cmake')
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
                    ('WIX_BITMAP_DIR'   ,'${WIX_INSTALL_DIR}/${CALLING_PROJECT}/Bitmaps'),
                    ('ROOT_TMP_DIR', '${TEMPLATING_PLUGIN_PATH}/rc/'),
                    ('TPL_DIR' , '${ROOT_TMP_DIR}/wix/'),
                    ('DOC_DIR', '${PRJ_ROOT_DIR}/rc/documentations/')
                ],
            'template_prj':
                [
                    ('${TPL_DIR}/call.wxs',
                        '${WIX_DIR}/${CALLING_PROJECT_FULL_NAME}.wxs'),
                    ('${TPL_DIR}/proj.wxs', '${WIX_DIR}/${PRJ_NAME}.wxs'),
                    ('${TPL_DIR}/generate_msi.py',
                         '${WIX_DIR}/gen_msi_${CALLING_PROJECT_FULL_NAME}.py'),
                    ('${TPL_DIR}/generate_msi.bat',
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




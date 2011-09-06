<%
from string import Template
project=PROJECT

import os
import platform

def osname():
    if platform.platform().startswith('Linux'):
        return 'linux'
    elif platform.platform().startswith('Darwin'):
        return 'darwin'
    else:
        return 'nt'

def escape(varname):
    return ''.join(['${',varname,'}'])

def cmake_normalized(path):
    normalized_path = path

    if osname() == 'nt':
        normalized_path = path.replace('\\', '/')

    return normalized_path

if project.get_lower('DEBUG') == 'full':
    compile_mode = 'debug'
else:
    compile_mode = 'release'


def partial_matches_path(dirs, partial_filename, ext=''):
    
    list_file = []

    if not ext:
        ext = partial_filename

    for directory in dirs:
        for f in os.listdir(directory):
            if partial_filename in f and ext in f:
                list_file.append(os.path.join(directory,f))

    return list_file

def get_install_libs(libext_instance):
    list_libs = []
    list_dir = libext_instance.ABS_LIBPATH

    if osname() == 'nt':
        ext = '.dll'
    elif osname() == 'darwin':
        ext = '.dylib'
    else:
        ext = '.so'

    for libname in libext_instance.libs:
        list_libs.extend(partial_matches_path(list_dir, libname, ext))

    return list_libs

cmake_install_path = cmake_normalized(CMAKE_INSTALL_DIR)
output_dir = '/'.join([cmake_install_path, compile_mode, project.name])
libext_list = [i.get('LIBEXTINSTANCE') for i in PROJECT.bin_rec_deps]

if osname() == 'darwin':
    frameworks = []
    for i in libext_list:
        frameworks.extends(i.frameworks)


use_qt = False
qt_components = []
%>


#cmake version
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

#master project
PROJECT(${PRJ_USER_FORMAT})


#qt check
%for deps in project.bin_rec_deps:
    %if 'qt' in deps.full_name and not use_qt:
        <% use_qt = True; qt_prj = deps%>
    %endif
    %if 'qt' in deps.full_name:
        <% qt_components.append(deps.base_name) %>
        <% 
libext_instance = deps.get("LIBEXTINSTANCE")
qt_components = [ i.replace('qt', 'Qt') for i in libext_instance.depends_on if 'qt' in i]
%>
    %endif
%endfor

%if use_qt:
SET(QT_QMAKE_EXECUTABLE ${cmake_normalized(qt_prj.bin_path)}/qmake)
FIND_PACKAGE(Qt4 COMPONENTS ${' '.join(set(qt_components))} REQUIRED)
INCLUDE(${escape("QT_USE_FILE")})

QT4_WRAP_CPP(PRJ_HEADERS_MOC
    %for inc in project.get_includes(False):
            ${cmake_normalized(inc)}
    %endfor
            )
#ui management
QT4_WRAP_UI(PRJ_UI_FILES
%for other_file in project.get_others():
    %if other_file.endswith('.ui'):
        ${cmake_normalized(other_file)}
    %endif
%endfor
          )
INCLUDE_DIRECTORIES( ${escape("CMAKE_BINARY_DIR")} )
%endif


%if project.get_includes(false) or project.get_sources(false): #begin check if sources exist


%if project.get_lower('TYPE') == 'exec':
SET(EXECUTABLE_OUTPUT_PATH
    ${output_dir}
   )
%else:
SET(LIBRARY_OUTPUT_PATH
    ${output_dir}
   )
%endif

INCLUDE_DIRECTORIES(
%for path in project.env['CPPPATH']:
    %if isinstance(path, str) and '$' not in path:
    ${cmake_normalized(path)}
    %endif
%endfor
                   )
               
LINK_DIRECTORIES(
%for prj in project.rec_deps:
    %if not prj.get_lower("TYPE") == 'bin_libext':
    ${'/'.join([cmake_install_path, compile_mode, prj.base_name])}
    %endif
%endfor
%for lib_path in project.env['LIBPATH']:
    %if isinstance(lib_path, str) and '$' not in lib_path:
        ${cmake_normalized(lib_path)}
    %endif
%endfor
%for lib in libext_list:
    %if osname() == 'darwin':
    ${'\n   '.join(lib.ABS_FRAMEWORKPATH)}
    %endif
%endfor
    )

ADD_DEFINITIONS(
    %for var in project.env['CPPDEFINES']:
    %if isinstance(var, str):
    -D${var}
    %elif isinstance(var,list):
    <%list_str=[str(i) for i in var]%>
    -D${'='.join(list_str)}
    %else:
    <% temp = Template(var[1])%>
    -D${var[0]+'='+temp.substitute(prj.env)}
    %endif
%endfor
                )


FILE(
    GLOB_RECURSE
    ${project.base_name}
    %for include_path in project.include_path:
    ${cmake_normalized(include_path)}/*
    %endfor
    %for src_path in project.src_path:
    ${cmake_normalized(src_path)}/*
    %endfor
    )

#declaration of target
%if project.get_lower('TYPE') == 'bundle':
ADD_LIBRARY(${project.full_name}
            SHARED 
%elif project.get_lower('TYPE') == 'exec':
ADD_EXECUTABLE(${project.full_name} ${'WIN32' if project.get_lower('CONSOLE') else ''}
%else :
ADD_LIBRARY(${project.full_name}
            SHARED
%endif

%if use_qt:
        ${escape('PRJ_HEADERS_MOC')}
        ${escape('PRJ_UI_FILES')}
%endif
            ${escape(project.base_name)}
          )

#add linked libraries
TARGET_LINK_LIBRARIES(${project.full_name}
%for lib in project.env['LIBS']:
    %if 'QT4' not in lib:
    ${lib}
    %endif
%endfor
%if use_qt:
    ${escape("QT_LIBRARIES")} 
%endif
%if osname() == 'darwin':
    ${'\n   '.join(frameworks)}
%endif
    )

%endif #end check if sources exist


#add dependencies
%if PRJ_NAME == MASTER_PRJ_NAME:
    %for prj in PRJ_DEPS:
        %if prj.get_lower('TYPE') in ['exec', 'bundle','shared']:
    ADD_SUBDIRECTORY(${prj.base_name})
        %endif
    %endfor
%endif


#copying Files
%if project.get_lower('TYPE') == 'shared':
    %if osname() == "nt":
        <%output_dir= 'bin'%>
    %elif osname() == "darwin":
        <%output_dir= 'Librairies'%>
    %else:
        <%output_dir= 'lib'%>
    %endif
    <%output_prj_dir='/'.join(['share',project.versioned_name])%>
%elif project.get_lower('TYPE') == 'exec':
    <%output_dir= 'bin'%>
    <%output_prj_dir='/'.join(['share',project.versioned_name])%>
%else:
    <%output_dir= '/'.join(['Bundles',project.versioned_name])%>
    <%output_prj_dir = output_dir%>
%endif

%if project.get_includes(false) or project.get_sources(false): #begin check if sources exist

GET_TARGET_PROPERTY(target_path ${project.full_name} LOCATION)
INSTALL(PROGRAMS ${escape("target_path")}
        DESTINATION ${cmake_install_path}/Install/${output_dir})
INSTALL(FILES ${escape("target_path")}
        DESTINATION ${cmake_install_path}/Install/${output_prj_dir})



%endif #end check if sources exist

%for o_file in project.get_others():
    <% o_file = cmake_normalized(o_file)%> 
    %if '/rc/' in o_file:
<% 
path_rc = o_file.split('/rc/')[1]
if '/' in path_rc:
    path,name = path_rc.rsplit('/', 1)
else:
    name = path_rc
    path = ''
%>
INSTALL(FILES ${o_file} DESTINATION ${cmake_install_path}/Install/${output_prj_dir}/${path})
    %endif
%endfor


%if PRJ_NAME == MASTER_PRJ_NAME:
#install rules
<%  
libext_install = [i for i in libext_list if i.install]
%>
%for deps in libext_install:
<% src= deps.basepath %>
    %for directory in deps.install:
INSTALL(DIRECTORY ${src}/${directory[0]} 
        DESTINATION ${cmake_install_path}/Install/${directory[1]})
    %endfor
%endfor
%for bindeps in PROJECT.bin_rec_deps:
    %for lib in get_install_libs(bindeps.get('LIBEXTINSTANCE')):
INSTALL(FILES ${lib} DESTINATION ${cmake_install_path}/Install/${'bin' if osname()=='nt' else 'lib' } )

    %endfor
%endfor
%endif

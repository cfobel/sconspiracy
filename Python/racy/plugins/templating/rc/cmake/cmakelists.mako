<%
from string import Template
import os
def cmake_variable(varname):
    context.write(''.join(['${',varname,'}']))

if PROJECT.get_lower('DEBUG') == 'full':
    compile_mode = 'debug'
else:
    compile_mode = 'release'

OUTPUT_DIR = '/'.join([CMAKE_INSTALL_DIR, compile_mode, PROJECT.name])

USE_QT = False
%>


#cmake version
cmake_minimum_required(VERSION 2.6)

#master project
project(${PRJ_USER_FORMAT})


#qt check
%for deps in PROJECT.bin_deps:
    %if 'qt' in deps.full_name and not USE_QT:
        <% USE_QT = True
QT_PRJ = deps
        %>
    %endif
%endfor

%if USE_QT:
set(QT_QMAKE_EXECUTABLE ${QT_PRJ.bin_path}/qmake)
find_package(Qt4 REQUIRED)
include(<% cmake_variable("QT_USE_FILE")%>)
QT4_WRAP_CPP(PRJ_HEADERS_MOC 
    %for inc in PROJECT.get_includes(False):
            ${inc}
    %endfor
            )
%endif


%if PROJECT.get_includes(false) or PROJECT.get_sources(false): #begin check if sources exist

set(EXECUTABLE_OUTPUT_PATH
    ${OUTPUT_DIR}
   )

set(LIBRARY_OUTPUT_PATH
    ${OUTPUT_DIR}
   )

include_directories(
%for prj in PROJECT.rec_deps:
    %for include in set(prj.include_path):
    ${include}
    %endfor
%endfor
%for include_path in set(PROJECT.include_path):
    ${include_path}
%endfor
                   )
               
link_directories(
%for prj in PROJECT.rec_deps:
    %if not prj.get_lower("TYPE") == 'bin_libext':
    ${'/'.join([CMAKE_INSTALL_DIR, compile_mode, prj.base_name])}
    %endif
%endfor
%for lib_path in PROJECT.env['LIBPATH']:
    %if isinstance(lib_path, str) and '$' not in lib_path:
        ${lib_path}
    %endif
%endfor
                   )

add_definitions(
    %for var in PROJECT.env['CPPDEFINES']:
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


file(
    GLOB_RECURSE
    ${PROJECT.base_name}
    %for include_path in PROJECT.include_path:
    ${include_path}/*
    %endfor
    %for src_path in PROJECT.src_path:
    ${src_path}/*
    %endfor
    )

#declaration of target
%if PROJECT.get_lower('TYPE') == 'bundle':
add_library(${PROJECT.full_name}
            SHARED 
%if USE_QT:
            <%cmake_variable('PRJ_HEADERS_MOC') %>
%endif
            <%cmake_variable(PROJECT.base_name)%>)
%elif PROJECT.get_lower('TYPE') == 'exec':
add_executable(${PROJECT.full_name} 
            <%cmake_variable('PRJ_HEADERS_MOC') %>
            <%cmake_variable(PROJECT.base_name)%>)
%else :
add_library(${PROJECT.full_name}
            SHARED
            <%cmake_variable('PRJ_HEADERS_MOC') %>
            <%cmake_variable(PROJECT.base_name)%>)
%endif


#add linked libraries
target_link_libraries(${PROJECT.full_name}
%for deps in PROJECT.rec_deps:
    %if not deps.get_lower('TYPE') == 'bin_libext' and '$' not in deps.full_name:
    ${deps.full_name}
    %endif
%endfor
%for lib in PROJECT.env['LIBS']:
    %if 'QT4' not in lib:
    ${lib}
    %endif
%endfor
%if USE_QT:
    <%cmake_variable("QT_LIBRAIRIES")%> 
%endif
    )

%endif #end check if sources exist


#add dependencies
%if PRJ_NAME == MASTER_PRJ_NAME:
    %for prj in PRJ_DEPS:
        %if prj.get_lower('TYPE') in ['exec', 'bundle','shared']:
    add_subdirectory(${prj.base_name})
        %endif
    %endfor
%endif


#copying Files
%if PROJECT.get_lower('TYPE') == 'shared':
    <%output_dir= 'lib'%>
    <%output_prj_dir=os.path.join('share',PROJECT.versioned_name)%>
%elif PROJECT.get_lower('TYPE') == 'exec':
    <%output_dir= 'bin'%>
    <%output_prj_dir=os.path.join('share',PROJECT.versioned_name)%>
%else:
    <%output_dir= os.path.join('Bundles',PROJECT.versioned_name)%>
    <%output_prj_dir = output_dir%>
%endif

%if PROJECT.get_includes(false) or PROJECT.get_sources(false): #begin check if sources exist

get_target_property(target_path ${PROJECT.full_name} LOCATION)
file(MAKE_DIRECTORY ${CMAKE_INSTALL_DIR}/Install/${output_dir})
file(MAKE_DIRECTORY ${CMAKE_INSTALL_DIR}/Install/${output_prj_dir})

add_custom_command(TARGET ${PROJECT.full_name} POST_BUILD
        COMMAND <%cmake_variable("CMAKE_COMMAND")%> -E copy 
            <%cmake_variable("target_path")%> 
            ${CMAKE_INSTALL_DIR}/Install/${output_dir})

add_custom_command(TARGET ${PROJECT.full_name} POST_BUILD
        COMMAND <%cmake_variable("CMAKE_COMMAND")%> -E copy 
            <%cmake_variable("target_path")%> 
            ${CMAKE_INSTALL_DIR}/Install/${output_prj_dir})

%endif #end check if sources exist

%for o_file in PROJECT.get_others():
    %if '/rc/' in o_file:
<% 
path_rc = o_file.split('/rc/')[1]
path,name = os.path.split(path_rc)
%>
file(MAKE_DIRECTORY ${CMAKE_INSTALL_DIR}/Install/${output_prj_dir}/${path})
file(COPY ${o_file} DESTINATION ${CMAKE_INSTALL_DIR}/Install/${output_prj_dir}/${path})
    %endif
%endfor


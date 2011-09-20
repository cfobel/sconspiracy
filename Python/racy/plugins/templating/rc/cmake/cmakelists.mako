<%namespace file="definitions.mako" import="*"/>
<%
from string import Template
project=PROJECT
cmake_dir=CMAKE_DIR
use_qt=False

cmake_install_path = unix_path(CMAKE_INSTALL_DIR)
output_dir = '/'.join([CMAKE_BUILD_DIR, project.name])

libext_list = [i.get('LIBEXTINSTANCE') for i in PROJECT.bin_rec_deps]

frameworks = create_framework_var(libext_list)
for deps in project.bin_rec_deps:
    if 'qt' in deps.full_name:
        use_qt=True
        break

%>

#cmake version
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

#master project
PROJECT(${project.base_name})

SET(TARGET_NAME ${project.full_name})

%if "OpenCL" in frameworks:
FIND_LIBRARY(OPENCL_LIBS OpenCL)
FIND_PATH(OPENCL_INCLUDE OpenCL/cl.h)
%endif

%if use_qt:
<%
qt_components = get_qt_component(project)
qt_bin_dir = get_qt_bin_dir(project)
ui_files = [i for i in project.get_others() if i.endswith('.ui')]
%>
SET(QT_QMAKE_EXECUTABLE ${qt_bin_dir})
FIND_PACKAGE(Qt4 COMPONENTS ${' '.join(set(qt_components))} REQUIRED)
INCLUDE(${escape("QT_USE_FILE")})

QT4_WRAP_CPP(PRJ_HEADERS_MOC
            ${format_list_paths(project.get_includes(False))}
            )
%if ui_files:
QT4_WRAP_UI(PRJ_UI_FILES
        ${format_list_paths(ui_files)}
          )
%endif
INCLUDE_DIRECTORIES( ${escape("CMAKE_BINARY_DIR")} )
%endif


%if project.get_includes(false) or project.get_sources(false): #begin check if sources exist
<% 
include_dirs= [i for i in project.env['CPPPATH'] if isinstance(i, str) and not '$' in i] 
link_directories = [get_build_output_dir(i) for i in project.rec_deps if project.get_lower("TYPE") == 'bin_libext']
link_directories.extend([i for i in project.env['LIBPATH'] if isinstance(i, str) and not '$' in i])
src_dirs = [i + '/*' for i in project.src_path]
include_path= [i + '/*' for i in project.include_path]
libs = [ i for i in project.env['LIBS'] if not 'Qt' in i and 'QT' not in i]
%>


SET(${"EXECUTABLE_OUTPUT_PATH" if project.get_lower('TYPE') == 'exec' else "LIBRARY_OUTPUT_PATH"} 
    ${get_build_output_dir(project)}
    )




INCLUDE_DIRECTORIES(
    ${format_list_paths(include_dirs)}
%if "OpenCL" in frameworks:
    ${escape("OPENCL_INCLUDE")}
%endif
                    )
               
LINK_DIRECTORIES(
    ${format_list_paths(link_directories)}
%if osname() == 'darwin':
    %for lib in libext_list:
    ${'\n   '.join(lib.ABS_FRAMEWORKPATH)}
    %endfor
%endif
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
    -D${var[0]+'='+temp.substitute(project.env)}
    %endif
%endfor
    %if use_qt:
    ${escape("QT_DEFINITIONS")}
    %endif
                )


FILE(
    GLOB_RECURSE
    ${project.base_name}
    ${format_list_paths(include_path)}
    ${format_list_paths(src_dirs)}
    )

#declaration of target
%if project.get_lower('TYPE') == 'exec':
ADD_EXECUTABLE(${escape("TARGET_NAME")} ${'WIN32' if project.get_lower('CONSOLE') else ''}
%else :
ADD_LIBRARY(${escape("TARGET_NAME")}
            SHARED
%endif
        ${escape('PRJ_HEADERS_MOC')}
        ${escape('PRJ_UI_FILES')}
        ${escape(project.base_name)}
          )

#add linked libraries
TARGET_LINK_LIBRARIES(${escape("TARGET_NAME")}
${format_list_paths(libs)}
    ${escape("OPENCL_LIBS")}
    %if use_qt:
    ${escape("QT_LIBRARIES")} 
    %endif
    )

SET_TARGET_PROPERTIES(${escape("TARGET_NAME")}
                        PROPERTIES OUTPUT_NAME ${project.full_name})

GET_TARGET_PROPERTY(target_path ${escape("TARGET_NAME")} LOCATION)
ADD_CUSTOM_COMMAND(TARGET  ${escape("TARGET_NAME")}
                   POST_BUILD
                   COMMAND ${escape("CMAKE_COMMAND")} -E copy ${escape("target_path")}
                   ${get_output_dir(project)}
            )
INSTALL(PROGRAMS ${escape("target_path")}
        DESTINATION ${get_install_output_dir(project)})


INSTALL(FILES ${escape("target_path")}
        DESTINATION ${get_library_output_dir()})

%endif #end check if sources exist

%for o_file in project.get_others():
    %if '/rc/' in o_file:
<% 
o_file = unix_path(o_file)
output_dir = get_others_file_output_dir(project) +'/' + split_rc_path(o_file)
%> 
INSTALL(FILES ${o_file} DESTINATION
${get_install_output_dir(project) +'/' + split_rc_path(o_file)})

FILE(MAKE_DIRECTORY ${output_dir})
FILE(COPY ${o_file} 
    DESTINATION ${output_dir}           
            )


    %endif
%endfor

%if not  PRJ_NAME == MASTER_PRJ_NAME:
    <% return %>
%endif

%for prj in PRJ_DEPS:
    %if prj.get_lower('TYPE') in ['exec', 'bundle','shared']:
ADD_SUBDIRECTORY(${prj.base_name})
    %endif
%endfor
#install rules
<%  
libext_install = [i for i in libext_list if i.install]
%>
%for deps in libext_install:
<% src= deps.basepath %>
    %for directory in deps.install:
        %if not '*' in directory[0]: 
INSTALL(DIRECTORY ${src}/${directory[0]} 
        DESTINATION ${cmake_install_path}/Install/${directory[1]})
        %else:
<% dirs = get_wildcard_directory(src,directory[0]) %>
            %for dir_w in dirs:
INSTALL(DIRECTORY ${dir_w} 
        DESTINATION ${cmake_install_path}/Install/${directory[1]})
            %endfor
        %endif
    %endfor
%endfor
%for bindeps in PROJECT.bin_rec_deps:
    %for lib in get_install_libs(bindeps.get('LIBEXTINSTANCE')):
INSTALL(FILES ${lib} 
        DESTINATION ${get_library_output_dir()} 
       )
    %endfor
%endfor

%if osname() == 'darwin':
     %for i in project.bin_rec_deps:
<% framework = get_framework_path(i.get('LIBEXTINSTANCE'))%>
         %if framework:
INSTALL(DIRECTORY ${framework}
        DESTINATION ${cmake_install_path}/Install/Libraries
       )
         %endif
     %endfor
%endif

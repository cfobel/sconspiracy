<%namespace file="definitions.mako" import="*"/>
<% from string import Template
import os
project=PROJECT
cmake_dir=unix_path(CMAKE_DIR)
use_qt=False

cmake_install_path = unix_path(CMAKE_INSTALL_DIR)

libext_list = [i.get('LIBEXTINSTANCE') for i in PROJECT.bin_rec_deps]

frameworks = create_framework_var(libext_list)
for deps in project.bin_rec_deps:
    if 'qt' in deps.full_name:
        use_qt=True
        break

link_rc = os.path.join(CMAKE_DIR, "rc")
link_bin= os.path.join(CMAKE_DIR, "bin")%>


#cmake version
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

INCLUDE(${unix_path(CMAKE_MACRO_DIR)}/macro.cmake)
SYMLINK(${unix_path(project.rc_path)}  "rc"  ${cmake_dir})
SYMLINK(${unix_path(project.bin_path)} "bin" ${cmake_dir})

#master project
PROJECT(${project.base_name})
SET(CMAKE_INCLUDE_DIRECTORIES_BEFORE ON)

SET(TARGET_NAME ${project.full_name})

%if "OpenCL" in frameworks:
FIND_LIBRARY(OPENCL_LIBS OpenCL)
FIND_PATH(OPENCL_INCLUDE OpenCL/cl.h)
%endif

FILE(GLOB RESSOURCES
    FOLLOW_SYMLINKS
     ${unix_path(link_rc)}/*
     )

FILE(GLOB BIN 
    FOLLOW_SYMLINKS
     ${unix_path(link_bin)}/*
     )

%if project.get_includes(false) or project.get_sources(false): #begin check if sources exist

<% count = 0 %>
%for i in project.include_path:
%if os.path.exists(i):
SYMLINK(${unix_path(i)} "Include${count}" ${unix_path(os.path.join(cmake_dir, "includes"))})
%endif
<% count +=1 %>
%endfor
FILE(
    GLOB_RECURSE
    INCLUDES
    FOLLOW_SYMLINKS
    ${unix_path(os.path.join(cmake_dir, "includes"))}/*.[a-t]*
    )

    %if use_qt:
<% qt_components = get_qt_component(project)
qt_bin_dir = get_qt_bin_dir(project)
ui_files = [i for i in project.get_others() if i.endswith('.ui')] %>

SET(QT_QMAKE_EXECUTABLE ${qt_bin_dir})
FIND_PACKAGE(Qt4 COMPONENTS ${' '.join(set(qt_components))} REQUIRED)
INCLUDE(${escape("QT_USE_FILE")})

QT4_WRAP_CPP(PRJ_HEADERS_MOC
            ${escape('INCLUDES')}
            )
        %if ui_files:
QT4_WRAP_UI(PRJ_UI_FILES
        ${format_list_paths(ui_files)}
          )
        %endif
INCLUDE_DIRECTORIES( ${escape("CMAKE_BINARY_DIR")} )
    %endif




<% 
include_dirs= [i for i in project.env['CPPPATH'] if isinstance(i, str) and not '$' in i] 
link_directories = [escape("CMAKE_BINARY_DIR") +'/'+ get_build_output_dir(i) for i in project.rec_deps if project.get_lower("TYPE") == 'bin_libext']
link_directories.extend([i for i in project.env['LIBPATH'] if isinstance(i, str) and not '$' in i])
src_dirs = project.src_path
include_path= [i + '/*' for i in project.include_path]
libs = [ i for i in project.env['LIBS'] if not i.startswith('Qt') and 'QT' not in i]
link_src =  os.path.join(CMAKE_DIR, "src")

%>
<% count = 0%>
%for i in src_dirs:
SYMLINK(${unix_path(i)} "Src${count}" ${unix_path(link_src)})
<% count +=1 %>
%endfor

FILE(
    GLOB_RECURSE
    SOURCES
    FOLLOW_SYMLINKS
    ${unix_path(link_src)}/*
    )


SET(${"EXECUTABLE_OUTPUT_PATH" if project.get_lower('TYPE') == 'exec' else "LIBRARY_OUTPUT_PATH"} 
        ${escape("CMAKE_BINARY_DIR") +'/'+ get_build_output_dir(project)}
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


#declaration of target
%if project.get_lower('TYPE') == 'exec':
ADD_EXECUTABLE(${escape("TARGET_NAME")} ${'WIN32' if project.get_lower('CONSOLE') else ''}
%else :
ADD_LIBRARY(${escape("TARGET_NAME")}
            SHARED
%endif
        ${escape('PRJ_HEADERS_MOC')}
        ${escape('PRJ_UI_FILES')}
        ##${escape('RESSOURCES')}
        ${escape('BIN')}
        ${escape('SOURCES')}
        ${escape('INCLUDES')}
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

FILE(MAKE_DIRECTORY(${escape("CMAKE_BINARY_DIR") +'/'+get_output_dir(project)}/))

ADD_CUSTOM_COMMAND(TARGET  ${escape("TARGET_NAME")}
                   POST_BUILD
                   COMMAND ${escape("CMAKE_COMMAND")} -E copy ${escape("target_path")}
                   ${escape("CMAKE_BINARY_DIR") +'/' +get_output_dir(project)}/
            )
%else:
FILE(GLOB ARGS_LIST
    RELATIVE ${unix_path(project.rc_path)}
    ${unix_path(project.rc_path)}/*profile*.xml)

SET(PROJECT_NAME ${project.base_name})
SET(PROJECT_VERSION_NAME ${project.versioned_name})
SET(EXEC ${get_exec_path(project)})

FOREACH(ARG ${escape("ARGS_LIST")})

ADD_CUSTOM_TARGET(${escape('PROJECT_NAME')}_${escape('ARG')}
                ${escape('EXEC')}  Bundles/${escape('PROJECT_VERSION_NAME')}/${escape('ARG')}
                DEPENDS
%for i in project.rec_deps:
%if not i.get_lower('TYPE') == 'bin_libext':
                ${i.full_name}
%endif
%endfor
                WORKING_DIRECTORY
                ${escape("CMAKE_BINARY_DIR")}
                SOURCES
                ${escape('BIN')}
                ##${escape('RESSOURCES')}
                )
ENDFOREACH(ARG)


%endif #end check if sources exist


FILE(COPY
    ${escape("RESSOURCES")}
    DESTINATION
    ${escape("CMAKE_BINARY_DIR") +'/'+get_others_file_output_dir(project)}/
    )

IF(WIN32)
    SET(PROCESSOR_COUNT "$ENV{NUMBER_OF_PROCESSORS}")
    SET(CMAKE_CXX_FLAGS "${escape("CMAKE_CXX_FLAGS")} /MP${escape("CMAKE_CXX_MP_NUM_PROCESSORS")}")
    SET(CMAKE_C_FLAGS "${escape("CMAKE_C_FLAGS")} /MP${escape("CMAKE_CXX_MP_NUM_PROCESSORS")}")
%if not  PRJ_NAME == MASTER_PRJ_NAME:
ENDIF(WIN32)
    <% return %>
%endif


SET(LIST_LIBEXT
%for bindeps in PROJECT.bin_rec_deps:
    %for lib in get_install_libs(bindeps.get('LIBEXTINSTANCE')):
    ${unix_path(lib)}
    %endfor
%endfor
    )
LIST_COPY("${escape('LIST_LIBEXT')}" ${escape("CMAKE_BINARY_DIR") +'/'+get_build_output_dir(project)}/ )
ENDIF(WIN32)

SET(SUBDIRECTORIES 
%for prj in PRJ_DEPS:
    %if prj.get_lower('TYPE') in ['exec', 'bundle','shared']:
    ${prj.base_name}
    %endif
%endfor
    )
ADD_SUBDIRECTORIES("${escape("SUBDIRECTORIES")}")
#install rules
<%  
libext_install = [i for i in libext_list if i.install]
%>

%for deps in libext_install:
<% src= deps.basepath %>
    %for directory in deps.install:
        %if not '*' in directory[0]: 
<% link_name = os.path.split(directory[0])[1]%>
SYMLINK(${unix_path(src + '/' + directory[0])}
        ${link_name}
        ${escape("CMAKE_BINARY_DIR")+"/"+ directory[1]}
         )
        %else:
<% dirs = get_wildcard_directory(src,directory[0]) %>

            %for dir_w in dirs:
SYMLINK(${unix_path(dir_w)}
         ${os.path.split(dir_w)[1]}
         ${escape("CMAKE_BINARY_DIR") + "/"+ directory[1]}
         )

            %endfor
        %endif
    %endfor
%endfor


##%for bindeps in PROJECT.bin_rec_deps:
    ##%for lib in get_install_libs(bindeps.get('LIBEXTINSTANCE')):
##INSTALL(FILES ${unix_path(lib)} 
        ##DESTINATION ${get_library_output_dir()} 
       ##)
    ##%endfor

##%endfor

##%if osname() == 'darwin':
     ##%for i in project.bin_rec_deps:
##<% framework = get_framework_path(i.get('LIBEXTINSTANCE'))%>
         ##%if framework:
##INSTALL(DIRECTORY ${unix_path(framework)}
        ##DESTINATION ${cmake_install_path}/Install/Libraries
       ##)
         ##%endif
     ##%endfor
##%endif

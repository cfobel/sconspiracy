<%!
import platform
import os
import glob
%>
## Write the os name : linux, darwin or nt
<%def name="osname()">
    %if platform.platform().startswith('Linux'):
        <%return "linux"%>
    %elif platform.platform().startswith('Darwin'):
        <%return "darwin"%>
    %else:
        <%return "nt"%>
    %endif
</%def>

##convert all path in unix path style
<%def name="unix_path(path)"><% 
return path.replace('\\', '/').replace('//','/') %>
</%def>

##escape variables
<%def name="escape(varname)"><%return ''.join(['${',varname,'}'])%></%def>


<%def name="partial_matches_path(dirs, partial_filename, ext='')"> <%
    list_file = []
    if not ext:
        ext = partial_filename
    for directory in dirs:
        for f in os.listdir(directory):
            if partial_filename in f and ext in f:
                list_file.append(os.path.join(directory,f))
    return list_file %>
</%def>

<%def name="get_install_libs(libext_instance)"><%
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

    return list_libs%>
</%def>

<%def name="get_framework_path(libext_instance)">
<%
    frameworks_path = libext_instance.ABS_FRAMEWORKPATH
    result = ''
    for f in frameworks_path:
         for file in os.listdir(f):
              if libext_instance.name.lower() in file.lower() and '.framework' in file.lower():
                   result = os.path.join(f, file)
                   break
         if result:
             break
    return result
%>
</%def>


<%def name="get_wildcard_directory(src, directory)"><%
    directory = os.path.join(src,directory)
    return filter(os.path.isdir,glob.glob(directory)) %>
</%def>


<%def name="create_framework_var(libext_list)"><%
    frameworks = []%>
    %if osname() == 'darwin':
        %for i in libext_list:
            <% frameworks.extend(i.frameworks) %>
            <% frameworks = [f for f in frameworks if 'Qt' not in f] %>
        %endfor
    %endif
    <%return frameworks%>
</%def>


<%def name="get_build_output_dir(prj)">
    %if osname() == "nt" or prj.get_lower("TYPE") == "exec":
        <%return unix_path('/'.join([CMAKE_BUILD_DIR, 'bin']))%>
    %elif osname()  == "linux":
        <%return unix_path('/'.join([CMAKE_BUILD_DIR, 'lib']))%>
    %else:
        <%return unix_path('/'.join([CMAKE_BUILD_DIR, 'Libraries']))%>
    %endif
</%def>

<%def name="get_output_dir(prj)">
    %if  prj.get_lower("TYPE") == "exec":
        <%return unix_path('/'.join([CMAKE_BUILD_DIR, 'bin']))%>
    %elif prj.get_lower("TYPE") == "bundle":
        <%return unix_path('/'.join([CMAKE_BUILD_DIR,
                                    'Bundles',
                                    prj.versioned_name]))%>
    %else:
        <%return unix_path('/'.join([CMAKE_BUILD_DIR,
                                     "share",
                                     prj.versioned_name]))%>
    %endif
</%def>

<%def name="get_others_file_output_dir(prj)">
    %if prj.get_lower("TYPE") == 'bundle':
        <%return unix_path('/'.join([CMAKE_BUILD_DIR,'Bundles',
                                    prj.versioned_name]))%>
    %else:
        <%return unix_path('/'.join([CMAKE_BUILD_DIR,'share',
                   prj.versioned_name]))%>
    %endif
</%def>


<%def name="get_install_output_dir(prj)">
    %if prj.get_lower("TYPE") == 'exec':
        <%return unix_path('/'.join([CMAKE_INSTALL_OUTPUT, 'bin']))%>
    %elif prj.get_lower("TYPE") == 'bundle':
        <%return unix_path('/'.join([CMAKE_INSTALL_OUTPUT,'Bundles',
                                    prj.versioned_name]))%>
    %else:
        %if osname() == "nt":
            <%output_lib= 'bin'%>
        %elif osname() == "darwin":
            <%output_lib= 'Libraries'%>
        %else:
            <%output_lib= 'lib'%>
        %endif
        <%return unix_path('/'.join([CMAKE_INSTALL_OUTPUT,output_lib,
                   prj.versioned_name]))%>
    %endif
</%def>

<%def name="get_library_output_dir()" ><%
if osname() == "nt":
    output_lib= 'bin'
elif osname() == "darwin":
    output_lib= 'Libraries'
else:
    output_lib= 'lib'
return unix_path('/'.join([CMAKE_INSTALL_OUTPUT,output_lib]))%>
</%def>

<%def name="split_rc_path(path)"> <%
    tmp = path.split('/rc/')[1]
    path_rc = tmp.rsplit('/', 1)[0]
    if path_rc == tmp:
        return ""
    else:
        return path_rc %>
</%def>

<%def name="get_qt_bin_dir(prj)" >
    %for deps in prj.bin_rec_deps:
        %if 'qt' in deps.full_name:
            <% return '/'.join([unix_path(deps.bin_path), 'qmake']) %>
        %endif
    %endfor
    <%return ''%>
</%def>

<%def name="get_qt_component(prj)" >
<% 
supported_component = ["QtGui", "QtSvg", "QtCore", "QtXml", "QtXmlPatterns",
                       "QtSql", "QtScript", "QtNetwork","QtHelp", "QtOpenGL",
                       "QtCLucene", "QtDBus", "QtUiTools", "phonon"]
qt_components = []%>
%for deps in prj.bin_rec_deps:
    %if 'qt' in deps.full_name or 'phonon' in deps.full_name:
    <% 
        libext_instance = deps.get("LIBEXTINSTANCE")
        libs = libext_instance.libs + libext_instance.frameworks
        for lib in libs:
            qt_components.extend([i for i in supported_component if lib.startswith(i)]) 
    %>
    %endif
%endfor
<% return qt_components %>
</%def>


<%def name="format_list_paths(list_paths)"><%
return '\n'.join([unix_path(i) for i in list_paths])%>
</%def>



<%def name="get_args(project)">
<% return [os.path.split(i)[1] for i in project.get_others() if "profile" in i] %>
</%def>


<%def name="get_exec_path(project)"><%
if project.get_lower('TYPE') == 'bundle':
    launcher = ''
    for i in project.rec_deps:
        if "launcher" in i.base_name:
            launcher = unix_path(os.path.join('./bin', i.full_name))
            break
    return launcher
return  [(unix_path(os.path.join('./bin', project.full_name)),)]%> 
</%def>

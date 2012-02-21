<% from racy.rutils import symlink, mkdir_p, DeepGlob
import os
from racy import print_msg
%>

## Include files
%for i in project.include_dirs:
<% full_path = os.path.join(project.get_path() , i)
if os.path.exists(full_path):
    path, name = os.path.split(i)
    path = os.path.join(project.base_name,i)
    try:
        symlink(full_path, os.path.join(QT_DIR,i)) 
    except:
        print_msg("{0} ->{1} already exist".format(full_path, os.path.join(QT_DIR,i)))
        
%>
    %for j in DeepGlob(None, os.path.join(QT_DIR,i)):
${os.path.join(i,j[2:]).replace('\\','/')}
    %endfor
%endfor

## Src Files
%for i in project.src_dirs:
<% full_path = os.path.join(project.get_path() , i)
if os.path.exists(full_path):
    path, name = os.path.split(i)
    path = os.path.join(project.base_name,i)
    try:
        symlink(full_path, os.path.join(QT_DIR,i)) 
    except:
        print_msg("{0} ->{1} already exist".format(full_path, os.path.join(QT_DIR,i)))
%>
    %for j in DeepGlob(None, os.path.join(QT_DIR,i)):
${os.path.join(i,j[2:]).replace('\\','/')}
    %endfor
%endfor

## Bin Files
<% link_rc = os.path.join(QT_DIR, "rc")
try:
    symlink(project.rc_path,  link_rc)
except:
    print_msg("{0} ->{1} already exist".format(full_path, os.path.join(QT_DIR,i)))
    %>
%for j in DeepGlob(None, link_rc):
${os.path.join("rc",j[2:]).replace('\\','/')}
%endfor

## Bin Files
<% link_bin = os.path.join(QT_DIR, "bin") 
try:
    symlink(project.bin_path,  link_bin)
except:
    print_msg("{0} ->{1} already exist".format(full_path, os.path.join(QT_DIR,i)))
    %>
%for j in DeepGlob(None, link_bin):
${os.path.join("bin",j[2:]).replace('\\','/')}
%endfor

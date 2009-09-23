@REM Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008 The SCons Foundation
@REM src/script/scons.bat 3842 2008/12/20 22:59:52 scons
@echo off
set SCONS_ERRORLEVEL=
if "%OS%" == "Windows_NT" goto WinNT

@REM for 9x/Me you better not have more than 9 args
python -c "from os.path import join; import sys; sys.path = [ join(sys.prefix, 'Lib', 'site-packages', 'scons-1.2.0'), join(sys.prefix, 'Lib', 'site-packages', 'scons'), join(sys.prefix, 'scons-1.2.0'), join(sys.prefix, 'scons')] + sys.path; import SCons.Script; yams_bin = r'"%~f0"'; yams_bin_dir = os.path.split(yams_bin)[0]; yams_root_dir = os.path.split(yams_bin_dir)[0]; yams_config_dir = os.path.join(yams_root_dir,'Config'); yams_python_dir = os.path.join(yams_root_dir,'Python'); sys.path.append(yams_python_dir); config_dir = os.environ.get('YAMS_CONFIG_DIR','~/.Yams'); os.environ['YAMS_CONFIG_DIR'] = (config_dir if os.path.isdir(config_dir) else yams_config_dir); import yams; yams_module_path = os.path.dirname(yams.__file__); sconstruct_file = os.path.join(yams_module_path, 'rc','SConstruct'); sys.argv.insert(1,sconstruct_file); sys.argv.insert(1,'-f');; SCons.Script.main()" %1 %2 %3 %4 %5 %6 %7 %8 %9
@REM no way to set exit status of this script for 9x/Me
goto endscons

@REM Credit where credit is due:  we return the exit code despite our
@REM use of setlocal+endlocal using a technique from Bear's Journal:
@REM http://code-bear.com/bearlog/2007/06/01/getting-the-exit-code-from-a-batch-file-that-is-run-from-a-python-program/

:WinNT
setlocal
@REM ensure the script will be executed with the Python it was installed for
set path=%~dp0;%~dp0..;%path%
python -c "import os; from os.path import join; import sys; sys.path = [ join(sys.prefix, 'Lib', 'site-packages', 'scons-1.2.0'), join(sys.prefix, 'Lib', 'site-packages', 'scons'), join(sys.prefix, 'scons-1.2.0'), join(sys.prefix, 'scons')] + sys.path; import SCons.Script; yams_bin = r'"%~f0"';print yams_bin; yams_bin_dir = os.path.split(yams_bin)[0]; yams_root_dir = os.path.split(yams_bin_dir)[0]; yams_config_dir = os.path.join(yams_root_dir,'Config'); yams_python_dir = os.path.join(yams_root_dir,'Python'); sys.path.append(yams_python_dir); config_dir = os.environ.get('YAMS_CONFIG_DIR','~/.Yams'); os.environ['YAMS_CONFIG_DIR'] = (config_dir if os.path.isdir(config_dir) else yams_config_dir); import yams; yams_module_path = os.path.dirname(yams.__file__); sconstruct_file = os.path.join(yams_module_path, 'rc','SConstruct'); sys.argv.insert(1,sconstruct_file); sys.argv.insert(1,'-f'); SCons.Script.main()" %*
endlocal & set SCONS_ERRORLEVEL=%ERRORLEVEL%

if NOT "%COMSPEC%" == "%SystemRoot%\system32\cmd.exe" goto returncode
if errorlevel 9009 echo you do not have python in your PATH
goto endscons

:returncode
exit /B %SCONS_ERRORLEVEL%

:endscons
call :returncode %SCONS_ERRORLEVEL%

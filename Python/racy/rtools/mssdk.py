# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import re
import os
import racy

import SCons.Tool.MSCommon.common as MSCommon

from racy.renv   import constants
from racy.renv.options import get_option
from racy.rtools import common, get_tool

import SCons

#------------------------------------------------------------------------------

class MssdkFlags(common.Flags):
    CXXFLAGS         = ['/GR']
    CXXFLAGS_RELEASE = ['/W3','/EHs','/Zm600','/MD','/Oi','/Ot','/Ob2','/TP']
    CXXFLAGS_DEBUG   = ['/W3','/EHsc','/MDd','/Od']
    CFLAGS           = []
    CFLAGS_RELEASE   = ['/MD']
    CFLAGS_DEBUG     = ['/MDd']
    CPPDEFINES       = [
                        'WIN32',
                        '_MBCS',
                        'NOMINMAX',
                       ]
    CPPDEFINES_RELEASE = []
    CPPDEFINES_DEBUG   = []
    LINKFLAGS      = [
                      #'/verbose'
                      ]

    WARNINGSASERRORS_FLAGS = ['/WX']
    OPTIMIZATION_FLAGS     = ['/O${OPTIMIZATIONLEVEL}']

    LINKFLAGS_NOCONSOLE  = ['/subsystem:windows']
    CPPDEFINES_NOCONSOLE = ['_WINDOWS']

    LINKFLAGS_CONSOLE  = ['/subsystem:console']
    CPPDEFINES_CONSOLE = []

    CXXFLAGS_BUNDLE   = ['/EHsc']
    CPPDEFINES_BUNDLE = ['_USRDLL']

    CXXFLAGS_SHARED   = ['/EHsc']
    CPPDEFINES_SHARED = ['_USRDLL']

    CXXFLAGS_EXEC = ['/GA']

    CPPDEFINES_RACY_VISIBILITY = [
                                ('_API_EXPORT'      , r'__declspec(dllexport)'),
                                ('_API_IMPORT'      , r'__declspec(dllimport)'),
                                ('_CLASS_API_EXPORT', r''),
                                ('_CLASS_API_IMPORT', r''),
                                ('_TEMPL_API_EXPORT', r''),
                                ('_TEMPL_API_IMPORT', r'export/**/"C++"'),
                                ]
    
#------------------------------------------------------------------------------

class MssdkFlagsDefault(MssdkFlags):
    CXXFLAGS_RELEASE = ['/Z7']
    CXXFLAGS_DEBUG =   ['/Z7']


#------------------------------------------------------------------------------

def generate(env):
    """Add Builders and construction variables for mssdk to an Environment."""
    
    env.__class__.ManageOption = manage_options
    env.__class__.InstallFileFilter = install_file_filter
        
    sdk_version = env.get('MSSDK_VERSION')
    env['WINDOWS_INSERT_MANIFEST'] = True
    
    if re.match('^6', sdk_version):
        # Run manifest tool as part of the link step
        # The number at the end of the line indicates the file type (1: EXE; 2:DLL).
        MTCOM = 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;'
        env['LINKCOM']   = [env['LINKCOM']  , MTCOM + '1']
        env['SHLINKCOM'] = [env['SHLINKCOM'], MTCOM + '2']
        
    FlagsGenerator =  MssdkFlagsDefault
    flags = env.__class__.Flags = FlagsGenerator()
    common.merge_flags(env, flags)
    
    mssdk_setup_env(env)

    # Windows SDK Archive:
    # http://msdn.microsoft.com/en-us/windowsserver/ff851942    
    sdk_to_msvc = {
                  '6.1':'9.0',  #MS SDK for VisualStudio2008 SP1 (2/5/2008)
                  '7.0':'10.0', #MS SDK for VisualStudio2010 (7/24/2009)
                  '7.1':'10.0', #MS SDK for VisualStudio2010 (5/19/2010)
                  }
    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = 'cl'
    env['TOOLINFO']['VERSION'] = sdk_to_msvc[sdk_version]

#------------------------------------------------------------------------------

def get_sdk_versions():
    import _winreg as reg
    HKLM = reg.HKEY_LOCAL_MACHINE
    
    try:
        k = reg.OpenKey(HKLM, "SOFTWARE\Microsoft\Microsoft SDKs\Windows")
        N = reg.QueryInfoKey(k)[0]
    except WindowsError, e:
        N = 0

    keys = [reg.EnumKey(k, i)[1:] for i in range(N)]
    return keys
    

#------------------------------------------------------------------------------

def mssdk_setup_env(env):
    HKEY_FMT = r'Software\Microsoft\Microsoft SDKs\Windows\v{sdk_version}\InstallationFolder'
    available_versions = get_sdk_versions()
    sdk_version = env.get('MSSDK_VERSION')
    if sdk_version not in available_versions:
        msg = ('mssdk <{v}> version is not available. '
               'Available versions are : {vs}')
        msg = msg.format(v = sdk_version, vs = available_versions)
        raise racy.ToolError('mssdk', msg )
    
    HKEY_FMT = HKEY_FMT.format(sdk_version = sdk_version)
    try:
        sdk_dir = MSCommon.read_reg(HKEY_FMT)
    except WindowsError, e:
        msg = 'Missing SDK registry key {key}'
        msg = msg.format(key = HKEY_FMT)
        raise racy.ToolError('mssdk', msg )

    target_arch = {
              '32':'/x86',
              '64':'/x64',
              }
    target_build = {
              'release':'/Release',
              'full':'/Debug',
              }
    args = '{build_arg} {arch_arg}'
    args = args.format(arch_arg = target_arch[get_option('ARCH')], build_arg = target_build[get_option('DEBUG')])
    import platform
    env['ENV']["PROCESSOR_ARCHITECTURE"] = platform.machine()
    env_clone = env.Clone()
    for k in ['OS']:
        env_clone['ENV'][k] = os.environ[k]
    stdout = get_output(sdk_dir + 'bin\\SetEnv.Cmd', args, env_clone)
    # Stupid batch files do not set return code: we take a look at the
    # beginning of the output for an error message instead
    olines = stdout.splitlines()
    if olines[0].startswith("The specified configuration type is missing"):
        raise racy.ToolError('mssdk', "\n".join(olines[:2]) )
    d = MSCommon.parse_output(stdout, ("INCLUDE", "LIB", "LIBPATH", "PATH"))
    for k, v in d.items():
        env.PrependENVPath(k, v, delete_existing=True)

#------------------------------------------------------------------------------

def get_output(vcbat, args , env ):
    """Parse the output of given bat file, with given args."""
    import subprocess
    system32_folder = os.environ['SystemRoot'] +'\System32'
    popen = SCons.Action._subproc(env,
                                  '"%s" %s & set' % (vcbat, args),
                                  stdin = 'devnull',
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  cwd=system32_folder )#needed by bat script file (to find reg and cmd program)

    # Use the .stdout and .stderr attributes directly because the
    # .communicate() method uses the threading module on Windows
    # and won't work under Pythons not built with threading.
    stdout = popen.stdout.read()
    stderr = popen.stderr.read()
    if stderr:
        raise racy.ToolError('mssdk', stderr )
    if popen.wait() != 0:
        raise IOError(stderr.decode("mbcs"))

    output = stdout.decode("mbcs")
    return output

#------------------------------------------------------------------------------

def manage_options(env, prj, options):
    common.manage_options(env, prj, options)

    if env.get('DEBUG') != 'release' :
        env['PDB'] = os.path.join(prj.build_dir, prj.full_name + '.pdb')

    if int(options.get('OPTIMIZATIONLEVEL')) > 2:
        msg = 'CL does not support an optimization level > 2'
        raise racy.ToolError('mssdk', msg)

    nolib = options.get('NOLIB',[])
    if nolib:
        nolib = ['/nodefaultlib:"{0}"'.format(lib) for lib in nolib]
        env.AppendUnique(LINKFLAGS = nolib)

    rc_file = os.path.join(prj.vc_dir, prj.name + '.rc' )
    if os.path.exists( rc_file ):
        res_file = env.RES(rc_file)
        prj.special_source.append(res_file)
        
    def_files = [os.path.join(p, prj.name + '.def') for p in prj.src_path]
    if any(map(os.path.exists, def_files)):
        env['WIN32_INSERT_DEF']        = 1
        constants.CXX_SOURCE_EXT      += [env['WIN32DEFSUFFIX'][1:]]

#------------------------------------------------------------------------------

def install_file_filter(env, f):
    to_install = [ '.exe', '.dll', '.pdb']
    res = hasattr(f,'get_path')
    if res:
        res = any(f.get_path().endswith(ext) for ext in to_install)
    return res
            
#------------------------------------------------------------------------------

def exists(version=None):
    #simple check with OS version
    #TODO check if win SDK is installed?
    if racy.renv.is_windows():
        return True
    else:
        return False


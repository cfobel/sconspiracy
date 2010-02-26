# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import re

import os

from racy.renv   import constants
from racy.renv.options import get_option
from racy.rtools import get_tool
from racy.rutils import merge_lists_of_dict, is_true

import SCons
msvc = get_tool('SCons.Tool.msvc')
msvs = get_tool('SCons.Tool.msvs')

exists = msvc.exists

def generate(env):
    """Add Builders and construction variables for msvc to an Environment."""

    msvc.generate(env)
    env.__class__.ManageOption = manage_options
    env.__class__.InstallFileFilter = install_file_filter

    # Run manifest tool as part of the link step
    # The number at the end of the line indicates the file type (1: EXE; 2:DLL).
#    if '8' in env['MSVS']['VERSION'] :
#        MTCOM = 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;'
#        env['LINKCOM']   = [env['LINKCOM']  , MTCOM + '1']
#        env['SHLINKCOM'] = [env['SHLINKCOM'], MTCOM + '2']
    env['WINDOWS_INSERT_MANIFEST'] = True

    #env['WIN32_INSERT_DEF']        = 1
    #constants.CXX_SOURCE_EXT      += [env['WIN32DEFSUFFIX'][1:]]

    CXXFLAGS = [
            '/GR', 
            ]

    CPPDEFINES = [
            'WIN32',
            '_MBCS',
            'NOMINMAX',
            ]

    LINKFLAGS  = []


    if env.get('DEBUG') == 'release' :
        if env['MSVS']['VERSION'] < 8:
            CXXFLAGS += ['/Og','/Gi']
        elif re.match('^9', env['MSVS']['VERSION']):
            CXXFLAGS += ['/Z7']

        merge_lists_of_dict(locals(), constants.COMMON_RELEASE)

        CXXFLAGS += ['/W3','/EHs','/Zm600','/MD','/Oi','/Ot','/Ob2','/TP']
        #CXXFLAGS += [ '/O{0}'.format(env['OPTIMIZATIONLEVEL']) , ]
    else :
        merge_lists_of_dict(locals(), constants.COMMON_DEBUG)

        CXXFLAGS += ['/W3','/EHsc','/MDd','/Od']

        if re.match('^[78]', env['MSVS']['VERSION']):
            CXXFLAGS += ['/Z7','/Wp64']
        elif re.match('^9', env['MSVS']['VERSION']):
            CXXFLAGS += ['/Z7']
        else :
            CXXFLAGS += ['/Zi']

    CPPDEFINES += [ ('__ARCH__' , r'\"{0}\"'.format(get_option('ARCH'))) ]
    
    names = ['CPPDEFINES','LINKFLAGS','CXXFLAGS']
    attrs = [locals()[n] for n in names]
    env.MergeFlags(dict(zip(names,attrs)), unique=True)

    env['TOOLINFO'] = {}
    env['TOOLINFO']['NAME']    = "cl"
    env['TOOLINFO']['VERSION'] = env['MSVS']['VERSION']



def manage_options(env, prj, options):
    CXXFLAGS   = []
    LINKFLAGS  = []
    CPPDEFINES = []
    if env.get('DEBUG') != 'release' :
        env['PDB'] = os.path.join(prj.build_dir, prj.full_name + ".pdb")

    if str(options.get('OPTIMIZATIONLEVEL')) in ['1','2']:
        CXXFLAGS += ['/O{0}'.format(options['OPTIMIZATIONLEVEL'])]

    if is_true( options.get('CONSOLE') ):
        LINKFLAGS += ['/subsystem:console']
    else:
        LINKFLAGS  += ['/subsystem:windows','/incremental:yes']
        CPPDEFINES += ['_WINDOWS']

    nolib = options.get('NOLIB',[])
    nolib = ['/nodefaultlib:"{0}"'.format(lib) for lib in nolib]
    LINKFLAGS += nolib

    if prj.is_shared or prj.is_bundle :
        if re.match('^[789]', env['MSVS']['VERSION']) :
            CXXFLAGS += ['/EHsc']
        else :
            CXXFLAGS += ['/GD','/GX']
        CPPDEFINES += ['_USRDLL']
    else :
        CXXFLAGS += ["/GA"]


    if options.get('USEVISIBILITY') == "racy":
        CPPDEFINES += [
            ('_API_EXPORT'      , r'__declspec(dllexport)'),
            ('_API_IMPORT'      , r'__declspec(dllimport)'),
            ('_CLASS_API_EXPORT', r''),
            ('_CLASS_API_IMPORT', r''),
            ('_TEMPL_API_EXPORT', r''),
            ('_TEMPL_API_IMPORT', r'export/**/"C++"'),
                ]

    env.Append( 
                CXXFLAGS   = CXXFLAGS  ,
                LINKFLAGS  = LINKFLAGS ,
                CPPDEFINES = CPPDEFINES
                )

    rc_file = os.path.join(prj.vc_dir, prj.name + '.rc' )
    if os.path.exists( rc_file ):
        res_file = env.RES(rc_file)
        prj.special_source.append(res_file)


def install_file_filter(env, f):
    to_install = [ '.exe', '.dll', '.pdb']
    res = hasattr(f,"get_path")
    if res:
        res = any(res.get_path().endswith(exit) for ext in to_install)
    return res
            




###############################################################################
### msvc patch
import string
def _get_msvc8_default_paths(env, version, suite, use_mfc_dirs):
    """Return a 3-tuple of (INCLUDE, LIB, PATH) as the values of those
    three environment variables that should be set in order to execute
    the MSVC 8 tools properly, if the information wasn't available
    from the registry."""

    MVSdir = None
    paths = {}
    exe_paths = []
    lib_paths = []
    include_paths = []
    try:
        paths = msvs.get_msvs_install_dirs(version, suite)
        MVSdir = paths['VSINSTALLDIR']
    except (KeyError, SCons.Util.RegError, SCons.Errors.InternalError):
        if os.environ.has_key('VSCOMNTOOLS'):
            MVSdir = os.path.normpath(os.path.join(os.environ['VSCOMNTOOLS'],'..','..'))
        else:
            # last resort -- default install location
            MVSdir = os.getenv('ProgramFiles') + r'\Microsoft Visual Studio 8'

    if MVSdir:
        if SCons.Util.can_read_reg and paths.has_key('VCINSTALLDIR'):
            MVSVCdir = paths['VCINSTALLDIR']
        else:
            MVSVCdir = os.path.join(MVSdir,'VC')

        MVSCommondir = os.path.join(MVSdir, 'Common7')
        include_paths.append( os.path.join(MVSVCdir, 'include') )
        lib_paths.append( os.path.join(MVSVCdir, 'lib') )
        for base, subdir in [(MVSCommondir,'IDE'), (MVSVCdir,'bin'),
                             (MVSCommondir,'Tools'), (MVSCommondir,r'Tools\bin')]:
            exe_paths.append( os.path.join( base, subdir) )

        if paths.has_key('PLATFORMSDKDIR'):
            PlatformSdkDir = paths['PLATFORMSDKDIR']
        else:
            PlatformSdkDir = os.path.join(MVSVCdir,'PlatformSDK')
        platform_include_path = os.path.join( PlatformSdkDir, 'Include' )
        include_paths.append( platform_include_path )
        lib_paths.append( os.path.join( PlatformSdkDir, 'Lib' ) )
        exe_paths.append( os.path.join( PlatformSdkDir, 'Bin' ) )
        if use_mfc_dirs:
            if paths.has_key('PLATFORMSDKDIR'):
                include_paths.append( os.path.join( platform_include_path, 'mfc' ) )
                include_paths.append( os.path.join( platform_include_path, 'atl' ) )
            else:
                atlmfc_path = os.path.join( MVSVCdir, 'atlmfc' )
                include_paths.append( os.path.join( atlmfc_path, 'include' ) )
                lib_paths.append( os.path.join( atlmfc_path, 'lib' ) )

        if SCons.Util.can_read_reg and paths.has_key('FRAMEWORKSDKDIR'):
            fwdir = paths['FRAMEWORKSDKDIR']
            include_paths.append( os.path.join( fwdir, 'include' ) )
            lib_paths.append( os.path.join( fwdir, 'lib' ) )
            exe_paths.append( os.path.join( fwdir, 'bin' ) )

        if SCons.Util.can_read_reg and paths.has_key('FRAMEWORKDIR') and paths.has_key('FRAMEWORKVERSION'):
            exe_paths.append( os.path.join( paths['FRAMEWORKDIR'], paths['FRAMEWORKVERSION'] ) )
    
    include_path = string.join( include_paths, os.pathsep )
    lib_path = string.join(lib_paths, os.pathsep )
    exe_path = string.join(exe_paths, os.pathsep )
    return (include_path, lib_path, exe_path)

def get_visualstudio8_suites(version="8.0"):
    """
    Returns a sorted list of all installed Visual Studio 2005 suites found
    in the registry. The highest version should be the first entry in the list.
    """

    suites = []

    # Detect Standard, Professional and Team edition
    try:
        idk = SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE,
            r'Software\Microsoft\VisualStudio\\' + version)
        SCons.Util.RegQueryValueEx(idk, 'InstallDir')
        editions = { 'PRO': r'Setup\VS\Pro' }       # ToDo: add standard and team editions
        edition_name = 'STD'
        for name, key_suffix in editions.items():
            try:
                idk = SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE,
                    r'Software\Microsoft\VisualStudio\\'+version + '\\' + key_suffix )
                edition_name = name
            except SCons.Util.RegError:
                pass
            suites.append(edition_name)
    except SCons.Util.RegError:
        pass

    # Detect Express edition
    try:
        idk = SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE,
            r'Software\Microsoft\VCExpress\\' + version)
        SCons.Util.RegQueryValueEx(idk, 'InstallDir')
        suites.append('EXPRESS')
    except SCons.Util.RegError:
        pass

    return suites

def get_default_visualstudio8_suite(env):
    """
    Returns the Visual Studio 2005 suite identifier set in the env, or the
    highest suite installed.
    """
    if not env.has_key('MSVS') or not SCons.Util.is_Dict(env['MSVS']):
        env['MSVS'] = {}

    if env.has_key('MSVS_SUITE'):
        # TODO(1.5)
        #suite = env['MSVS_SUITE'].upper()
        suite = string.upper(env['MSVS_SUITE'])
        suites = [suite]
    else:
        suite = 'EXPRESS'
        suites = [suite]
        if SCons.Util.can_read_reg:
            suites = get_visualstudio8_suites(env.get('MSVS_VERSION','8.0'))
            if suites:
                suite = suites[0] #use best suite by default

    env['MSVS_SUITE'] = suite
    env['MSVS']['SUITES'] = suites
    env['MSVS']['SUITE'] = suite

    return suite


def get_msvs_install_dirs(version = None, vs8suite = None):
    """
    Get installed locations for various msvc-related products, like the .NET SDK
    and the Platform SDK.
    """

    if not SCons.Util.can_read_reg:
        return {}

    if not version:
        versions = get_visualstudio_versions()
        if versions:
            version = versions[0] #use highest version by default
        else:
            return {}

    version_num, suite = msvs.msvs_parse_version(version)

    K = 'Software\\Microsoft\\VisualStudio\\' + str(version_num)
    if (version_num >= 8.0):
        if vs8suite == None:
            # We've been given no guidance about which Visual Studio 8
            # suite to use, so attempt to autodetect.
            suites = get_visualstudio8_suites(str(version_num))
            if suites:
                vs8suite = suites[0]

        if vs8suite == 'EXPRESS':
            K = 'Software\\Microsoft\\VCExpress\\' + str(version_num)

    # vc++ install dir
    rv = {}
    if (version_num < 7.0):
        key = K + r'\Setup\Microsoft Visual C++\ProductDir'
    else:
        key = K + r'\Setup\VC\ProductDir'
    try:
        (rv['VCINSTALLDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE, key)
    except SCons.Util.RegError:
        pass

    # visual studio install dir
    if (version_num < 7.0):
        try:
            (rv['VSINSTALLDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
                                                             K + r'\Setup\Microsoft Visual Studio\ProductDir')
        except SCons.Util.RegError:
            pass

        if not rv.has_key('VSINSTALLDIR') or not rv['VSINSTALLDIR']:
            if rv.has_key('VCINSTALLDIR') and rv['VCINSTALLDIR']:
                rv['VSINSTALLDIR'] = os.path.dirname(rv['VCINSTALLDIR'])
            else:
                rv['VSINSTALLDIR'] = os.path.join(SCons.Platform.win32.get_program_files_dir(),'Microsoft Visual Studio')
    else:
        try:
            (rv['VSINSTALLDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
                                                             K + r'\Setup\VS\ProductDir')
        except SCons.Util.RegError:
            pass

    # .NET framework install dir
    try:
        (rv['FRAMEWORKDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
            r'Software\Microsoft\.NETFramework\InstallRoot')
    except SCons.Util.RegError:
        pass

    if rv.has_key('FRAMEWORKDIR'):
        # try and enumerate the installed versions of the .NET framework.
        contents = os.listdir(rv['FRAMEWORKDIR'])
        l = re.compile('v[0-9]+.*')
        installed_framework_versions = filter(lambda e, l=l: l.match(e), contents)

        def versrt(a,b):
            # since version numbers aren't really floats...
            aa = a[1:]
            bb = b[1:]
            aal = string.split(aa, '.')
            bbl = string.split(bb, '.')
            # sequence comparison in python is lexicographical
            # which is exactly what we want.
            # Note we sort backwards so the highest version is first.
            return cmp(bbl,aal)

        installed_framework_versions.sort(versrt)

        rv['FRAMEWORKVERSIONS'] = installed_framework_versions

        # TODO: allow a specific framework version to be set

        # Choose a default framework version based on the Visual
        # Studio version.
        DefaultFrameworkVersionMap = {
            '7.0'   : 'v1.0',
            '7.1'   : 'v1.1',
            '8.0'   : 'v2.0',
            # TODO: Does .NET 3.0 need to be worked into here somewhere?
        }
        try:
            default_framework_version = DefaultFrameworkVersionMap[version[:3]]
        except (KeyError, TypeError):
            pass
        else:
            # Look for the first installed directory in FRAMEWORKDIR that
            # begins with the framework version string that's appropriate
            # for the Visual Studio version we're using.
            for v in installed_framework_versions:
                if v[:4] == default_framework_version:
                    rv['FRAMEWORKVERSION'] = v
                    break

        # If the framework version couldn't be worked out by the previous
        # code then fall back to using the latest version of the .NET
        # framework
        if not rv.has_key('FRAMEWORKVERSION'):
            rv['FRAMEWORKVERSION'] = installed_framework_versions[0]

    # .NET framework SDK install dir
    if rv.has_key('FRAMEWORKVERSION'):
        # The .NET SDK version used must match the .NET version used,
        # so we deliberately don't fall back to other .NET framework SDK
        # versions that might be present.
        ver = rv['FRAMEWORKVERSION'][:4]
        key = r'Software\Microsoft\.NETFramework\sdkInstallRoot' + ver
        try:
            (rv['FRAMEWORKSDKDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
                key)
        except SCons.Util.RegError:
            pass

    # MS Platform SDK dir
    try:
        (rv['PLATFORMSDKDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
            r'Software\Microsoft\MicrosoftSDK\Directories\Install Dir')
    except SCons.Util.RegError:
        pass
    try:
        (rv['PLATFORMSDKDIR'], t) = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
            r'Software\Microsoft\Microsoft SDKs\Windows\CurrentInstallFolder')
    except SCons.Util.RegError:
        pass

    if rv.has_key('PLATFORMSDKDIR'):
        # if we have a platform SDK, try and get some info on it.
        vers = {}
        try:
            loc = r'Software\Microsoft\MicrosoftSDK\InstalledSDKs'
            k = SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE,loc)
            i = 0
            while 1:
                try:
                    key = SCons.Util.RegEnumKey(k,i)
                    sdk = SCons.Util.RegOpenKeyEx(k,key)
                    j = 0
                    name = ''
                    date = ''
                    version = ''
                    while 1:
                        try:
                            (vk,vv,t) = SCons.Util.RegEnumValue(sdk,j)
                            # TODO(1.5):
                            #if vk.lower() == 'keyword':
                            #    name = vv
                            #if vk.lower() == 'propagation_date':
                            #    date = vv
                            #if vk.lower() == 'version':
                            #    version = vv
                            if string.lower(vk) == 'keyword':
                                name = vv
                            if string.lower(vk) == 'propagation_date':
                                date = vv
                            if string.lower(vk) == 'version':
                                version = vv
                            j = j + 1
                        except SCons.Util.RegError:
                            break
                    if name:
                        vers[name] = (date, version)
                    i = i + 1
                except SCons.Util.RegError:
                    break
            rv['PLATFORMSDK_MODULES'] = vers
        except SCons.Util.RegError:
            pass

    return rv

msvs.get_msvs_install_dirs = get_msvs_install_dirs
msvs.get_visualstudio8_suites = get_visualstudio8_suites
msvs.get_default_visualstudio8_suite = get_default_visualstudio8_suite
msvc._get_msvc8_default_paths = _get_msvc8_default_paths

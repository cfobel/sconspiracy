# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******



LOGLEVEL= {
    'disable' : 0,
    'fatal'   : 1,
    'error'   : 2,
    'warning' : 3,
    'info'    : 4,
    'debug'   : 5,
    'trace'   : 6,
}

VCS_DIRS = ['CVS', '.svn', '.hg']

LIBNAME_SEP = "_"

BIN_PATH     = 'bin'
LIB_PATH     = 'lib'
RC_PATH      = 'rc'
TEST_PATH    = 'test'

CXX_SOURCE_EXT = ['cpp','cxx','c','C']
CXX_HEADER_EXT = ['hpp','hxx','h','H']

PRJ_OPT_DIR = 'bin'
OPTS_FILE   = 'build.options'

SYSTEM_DEFAULT_TOOL = {
        "linux"   : "g++" ,
        "darwin"  : "g++" ,
        "windows" : "msvc",
        }

WINDOWS = 'win'
LINUX   = 'nux'
MACOSX  = 'osx'

SYSTEMS_RACY_NAMES = { 
        'linux'   : LINUX,
        'darwin'  : MACOSX,
        'windows' : WINDOWS,
        }

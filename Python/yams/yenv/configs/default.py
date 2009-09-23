# -*- coding: UTF8 -*-
# vim:filetype=python
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import yams.yenv as yenv


# --- Global variables ---
DEBUG             = 'full'

ARCH              = yenv.architecture()
PLATFORM          = yenv.platform()

DISTRIB           = 'no'

TOOL              = 'auto'
CONFIG            = 'default'

JOBS              = 'auto'

YAMS_DEBUG        = 'no'

BINPKG_VERSIONS   = {}

# --- individual projects variables ---
TYPE              = 'no type defined'
NAME              = '' # Internal use only

LOGLEVEL          = 'warning'


BUILD             = "yes"
BUILDDEPS         = "yes"
BUILDPKG          = "no"


CXX               = ''
MSVS_VERSION      = ''

USEVISIBILITY     = 'yes'
CONSOLE           = 'no'
OPTIMIZATIONLEVEL = 0

PREFIX            = []
POSTFIX           = []

VERSION           = '0-0'

LIB               = []
BUNDLES           = []
USE               = []


DEF               = []
INC               = []

STDLIBPATH        = []
STDLIB            = []
NOLIB             = []

CXXFLAGS          = []
LINKFLAGS         = []



import os
YAMS_CONFIG_DIR    = ''
YAMS_BUILD_DIR     = ''
YAMS_INSTALL_DIR   = ''
YAMS_LIBEXT_DIR    = ''
YAMS_BINPKGS_DIR   = ''
YAMS_CODE_DIRS     = []

ALLOW_USER_OPTIONS        = True
OVERRIDE_PROJECT_VALUE = {}

DEPRECATED = {
    'PATHLIB'     : 'Use "STDLIBPATH" instead.',
    'STDPATHLIB'  : 'Use "STDLIBPATH" instead.',
    'CPPFLAGS'    : 'Use "CXXFLAGS" instead.'  ,
    'TEST'        : 'Use "CPPUNIT" instead, managed by cppunit plugin' ,
    'TESTFIXTURE' : 'Use "CPPUNIT" instead, managed by cppunit plugin' ,
    'TESTRUNNER'  : 'Use "CPPUNIT" instead, managed by cppunit plugin' ,
    'TESTLIB'     : 'Use "CPPUNIT" instead, managed by cppunit plugin' ,
    }

# DISTCC/CCACHE/SCONSCACHE
# #PACK??
# #RESRC?
# DSP
# USEGCH
# USESTDAFX

import re
# Variable names :
# * can contain any upcase Alphanumerical char or an underscore 
# * must begin with any of [A-Z] or '_'
# * length must be at least 2
# Every other variable names will be ignored (but are accessible from python
# scripts)
opt_name_regex = re.compile("^[A-Z_]+[A-Z0-9_]+$")
del re

def check_deprecated(conf, source):
    """Returns a dict of deprecated options present in conf, based on the 
    'DEPRECATED' dict.
    conf may be any iterable (dict, list, ...)
    """
    res = {}
    for opt in conf:
        if opt_name_regex.match(opt):
            if DEPRECATED.has_key(opt):
                res[opt] = DEPRECATED[opt]

        if DEPRECATED.has_key(opt):
            import warnings
            msg = ('"{0}" option is deprecated. {2}').format(opt, source, DEPRECATED[opt])
            warnings.warn_explicit(
                msg,
                DeprecationWarning,
                '[{0}]'.format(source), 
                0
                )

    return res


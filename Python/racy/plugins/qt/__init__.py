# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from racy.renv import constants
from racy      import renv
from racy      import rutils


import re
q_object_search = re.compile(r'[^A-Za-z0-9]Q_OBJECT[^A-Za-z0-9]')
def header_has_qobject(file):
    res = False
    f = open(file)
    try:
        res = q_object_search.search(f.read())
    finally:
        f.close()
    return res


def qressources(prj):
    """Returns ui source files of the project"""
    qrc = rutils.DeepGlob(
            ['qrc'],
            prj.src_path,
            prj.build_dir,
            )
    return qrc


def includes(prj):
    """Returns ui source files of the project"""
    includes = rutils.DeepGlob(
            constants.CXX_HEADER_EXT,
            prj.include_path,
            inc_build_dir(prj),
            filter = header_has_qobject,
            )
    return includes


def inc_build_dir(prj):
    return os.path.join(renv.dirs.build, prj.full_name, constants.INCLUDE_PATH)

def ui_sources(prj):
    """Returns ui source files of the project"""
    return rutils.DeepGlob(
            ['ui'],
            prj.include_path,
            inc_build_dir(prj)
            )



class Plugin(racy.rplugins.Plugin):
    name = "qt"

    def has_additive(self, prj):
        return [use for use in prj.uses if 'qt' in use.lower()]

    def get_additive(self, prj):
        prj.variant_dir( inc_build_dir(prj), prj.include_path )
        env = prj.env

        localtoolpath = os.path.join(__path__[0], 'sconstools')
        env.Tool('qt4', toolpath=[localtoolpath])

        # add -name management
        env['QT4_RCCCOM']   = '$QT4_RCC $QT4_QRCFLAGS $SOURCE -o $TARGET -name ${SOURCE.filebase}'
        env['QT4_AUTOSCAN'] = 0

        uic = [ env.Uic4(ui)  for  ui in ui_sources(prj) ]
        moc = [ env.Moc4(inc) for inc in includes(prj)   ]
        qrc = [ env.Qrc(rc)   for rc in qressources(prj) ]

        sources = rutils.DeepGlob(
                constants.CXX_SOURCE_EXT, 
                prj.src_path, 
                prj.build_dir
                )

        #prj.special_source += uic
        prj.special_source += moc + qrc

        env.Depends(sources, uic)
        env.Append(CPPPATH = inc_build_dir(prj))
        #prj.sources
        return []

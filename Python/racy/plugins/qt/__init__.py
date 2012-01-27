# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from racy.renv     import constants
from racy.rproject import RacyProjectsDB
from racy          import renv
from racy          import rutils
from racy          import rlibext


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
    """Returns resource files of the project"""
    qrc = rutils.DeepGlob(
            ['qrc'],
            prj.src_path,
            src_build_dir(prj),
            )
    return qrc


def includes(prj):
    """Returns source files of the project"""
    includes = rutils.DeepGlob(
            constants.CXX_HEADER_EXT,
            prj.include_path,
            inc_build_dir(prj),
            filter = header_has_qobject,
            )
    return includes


def src_build_dir(prj):
    return map(prj.get_build_dir_for, prj.src_path)

def inc_build_dir(prj):
    return map(prj.get_build_dir_for, prj.include_path)

def ui_sources(prj):
    """Returns ui source files of the project"""
    return rutils.DeepGlob(
            ['ui'],
            prj.include_path,
            inc_build_dir(prj)
            )



class Plugin(racy.rplugins.Plugin):
    name = "qt"

    additive  = True
    env_addon = True

    def has_env_addon(self, env):
        return True

    def get_env_addon(self, env):
        localtoolpath = os.path.join(__path__[0], 'sconstools')
        try:
            env.Tool('qt4', toolpath=[localtoolpath])
        except Exception, e:
            self.enabled = False
            racy.print_warning(
                    "Qt plugin",
                    'Could not detect Qt 4 : Is Qt4 binary package missing ?'
                    )
        else:
            self.enabled = True
            def configure(e):

                db = RacyProjectsDB.current_db
                class FakePrj(object):
                    compiler = db.prj_args['cxx']
                    opts_source = 'Qt plugin'
                    projects_db = db
                    def __str__(self):
                        return ''

                zlib = rlibext.register.get_lib_for_prj('z', FakePrj())
                lib_path = zlib.ABS_LIBPATH
                racy.renv.QT_TOOLS_ENV = ( racy.renv.LD_VAR, lib_path )
            env._callbacks.append(configure)
        return []


    def has_additive(self, prj):
        return self.enabled and any(
                use for use in prj.uses if use.startswith('qt')
                )

    def get_additive(self, prj):
        for builddir, incpath in zip( inc_build_dir(prj), prj.include_path ):
            prj.variant_dir( builddir, incpath )
        env = prj.env

        env.PrependENVPath( *racy.renv.QT_TOOLS_ENV )

        uic = [ env.Uic4(ui)  for ui  in ui_sources(prj) ]
        moc = [ env.Moc4(inc) for inc in includes(prj)   ]
        qrc = [ env.Qrc(rc)   for rc  in qressources(prj) ]

        sources = rutils.DeepGlob(
                constants.CXX_SOURCE_EXT, 
                prj.src_path, 
                prj.build_dir
                )

        prj.special_source += moc + qrc

        env.Depends(sources, uic)
        env.Append(CPPPATH = inc_build_dir(prj))

        return []

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os

import racy

from racy import renv

from generategraph import generate_graph


class GraphLibExtError(racy.RacyPluginError):
    pass


KEYWORD = 'GRAPHLIBEXT'

GRAPHLIBEXT_INSTALL_PATH = os.path.join(racy.renv.dirs.install,"graphlibext")

class Plugin(racy.rplugins.Plugin):
    name = "graphlibext"

    options              = { KEYWORD : None }
    #allowed_values       = { KEYWORD : ['no', 'yes'] }
    commandline_opts     = [ KEYWORD ]
    #commandline_prj_opts = [ KEYWORD ]
    descriptions_opts    = {
            KEYWORD : 'Generate libext graph for "all" or '
                      'specified libext.'
                      }


    def init(self):
        libext = renv.options.get_option( KEYWORD )

        if libext:
            if libext == "all":
                libext = []
                dot_filename = "all_libext"
            else:
                libext = libext.split(',')
                dot_filename = "_".join(libext)
            
            graph = generate_graph(libext)

            if graph:
                file = os.path.join(
                    GRAPHLIBEXT_INSTALL_PATH,
                    "{0}.dot".format(dot_filename)
                    )
                fp=None
                try:
                    os.mkdir(GRAPHLIBEXT_INSTALL_PATH)
                    fp = open(file, 'w')
                    fp.write(graph)
                    fp.flush()
                except Exception,e:
                    racy.print_error( 'GraphLibExt error', GraphLibExtError(e) )
                finally:
                    if fp:
                        fp.close()

        return True




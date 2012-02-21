# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os
import platform
import sys

import racy
from racy.renv.options import get_option

import base
from stdoutproxy import ColorConsoleProxy

class Plugin(racy.rplugins.Plugin):
    name = "coloracy"

    options = {
            base.ENABLE_COLORACY_KEYWORD : 'auto',
            }

    allowed_values = {
            base.ENABLE_COLORACY_KEYWORD : ['no', 'yes', 'auto']
            }

    commandline_opts = [ base.ENABLE_COLORACY_KEYWORD ]

    descriptions_opts = {
            base.ENABLE_COLORACY_KEYWORD : 'Enable/disable coloracy plugin. '
                                           '"yes" forces color.',
            }

    stdout = sys.stdout
    stderr = sys.stderr


    def __init__(self):
        user_pattern = self.get_patterns()
        sys.stdout = self.get_proxy_stream(self.stdout, user_pattern)
        sys.stderr = self.get_proxy_stream(self.stderr, user_pattern, 'stderr')

    def get_patterns(self, user_pattern=None):
        patterns = []
        if user_pattern:
            patterns += user_pattern
        else:
            patterns += base.scons_patterns
            if platform.system() == "Windows":
                patterns += base.msvs_patterns
            else:
                patterns += base.gcc_patterns
            patterns += base.default_patterns
        return patterns

    def get_proxy_stream(
            self, stream,
            user_pattern=None,
            type='stdout',
            force=False,
            ):
        if force or stream.isatty():
            return ColorConsoleProxy(self.stdout, patterns=user_pattern,
                                    type=type)
        return stream



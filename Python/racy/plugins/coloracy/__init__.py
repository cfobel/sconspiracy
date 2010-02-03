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
from stdoutproxy import ColorStdOutProxy

class Plugin(racy.rplugins.Plugin):
    name = "coloracy"

    options = {
            base.ENABLE_COLORACY_KEYWORD : 'yes',
            base.COLORACY_KEYWORD        : None,
            }

    allowed_values = {
            base.ENABLE_COLORACY_KEYWORD : ['no', 'yes']
            }

    commandline_opts = [ base.ENABLE_COLORACY_KEYWORD ]

    descriptions_opts = {
            base.ENABLE_COLORACY_KEYWORD : 'Enable/disable coloracy plugin',
            base.COLORACY_KEYWORD        : base.COLORACY_PATTERN_HELP,
            }

    stdout = sys.stdout

    def __init__(self):
        self.set_stdout()

    def set_stdout(self, user_pattern=None):
        if sys.stdout.isatty():
            if user_pattern:
                patterns = user_pattern
            else:
                patterns = base.scons_patterns
                if platform.system() == "Windows":
                    patterns += base.msvs_patterns
                else:
                    patterns += base.gcc_patterns
                patterns += base.default_patterns
            sys.stdout = ColorStdOutProxy(self.stdout, patterns=patterns)


    def has_additive(self, prj):
        enable = prj.get(base.ENABLE_COLORACY_KEYWORD) == 'yes'

        if enable:
            user_pattern = prj.get(base.COLORACY_KEYWORD)
            self.set_stdout(user_pattern)
        else:
            sys.stdout = self.stdout

        return False


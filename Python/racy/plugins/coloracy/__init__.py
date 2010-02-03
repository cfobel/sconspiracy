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
            base.COLORACY_KEYWORD        : None,
            }

    allowed_values = {
            base.ENABLE_COLORACY_KEYWORD : ['no', 'yes', 'auto']
            }

    commandline_opts = [ base.ENABLE_COLORACY_KEYWORD ]

    descriptions_opts = {
            base.ENABLE_COLORACY_KEYWORD : 'Enable/disable coloracy plugin. '
                                           '"yes" forces color.',
            base.COLORACY_KEYWORD        : base.COLORACY_PATTERN_HELP,
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


    def has_additive(self, prj):
        user_option = prj.get(base.ENABLE_COLORACY_KEYWORD)
        enable = user_option == 'auto'
        force  = user_option == 'yes'

        if enable or force:
            user_ptrn = prj.get(base.COLORACY_KEYWORD)
            user_ptrn = self.get_patterns(user_ptrn)
            sys.stdout = self.get_proxy_stream(
                    self.stdout, user_ptrn, force=force)
            sys.stderr = self.get_proxy_stream(
                    self.stderr, user_ptrn, type='stderr', force=force)
        else:
            sys.stdout = self.stdout
            sys.stderr = self.stderr

        sys.__stdout__ = sys.stdout
        sys.__stderr__ = sys.stderr

        return False


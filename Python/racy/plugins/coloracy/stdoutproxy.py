# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

import re
from colorconsole import ColorText
from colorizer import Colorizer


class Proxy(object):

    def __init__( self, subject ):
        self.__subject = subject

    def __getattr__( self, name ):
        return getattr( self.__subject, name )


class ColorStdOutProxy(Proxy):
    """ StdOut proxy """

    def __init__(self, subject, *args, **kwargs):
        super(ColorStdOutProxy, self).__init__(subject)
        self.colorizer = Colorizer(*args, **kwargs)

    def write(self, s):
        self.colorizer(txt=s, out=self._Proxy__subject)


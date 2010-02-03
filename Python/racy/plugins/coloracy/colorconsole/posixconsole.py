# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from base import BaseColorText

__all__ = ["Console", "ColorText"]

class Console(object):
    FOREGROUND_BLACK     = '30'
    FOREGROUND_RED       = '31'
    FOREGROUND_GREEN     = '32'
    FOREGROUND_YELLOW    = '33'
    FOREGROUND_BLUE      = '34'
    FOREGROUND_MAGENTA   = '35'
    FOREGROUND_CYAN      = '36'
    FOREGROUND_WHITE     = '37'

    BACKGROUND_BLACK     = '40'
    BACKGROUND_RED       = '41'
    BACKGROUND_GREEN     = '42'
    BACKGROUND_YELLOW    = '43'
    BACKGROUND_BLUE      = '44'
    BACKGROUND_MAGENTA   = '45'
    BACKGROUND_CYAN      = '46'
    BACKGROUND_WHITE     = '47'

    FOREGROUND_INTENSITY = 1
    BACKGROUND_INTENSITY = 1

    RESET = '\033[0m'
    COLOR_FORMAT = '\033[{attributes}m'

    def __init__(self, *args):
        self.default_colors = self.RESET
        self.default_fg = self.RESET
        self.default_bg = self.RESET

    def get_text_attr(self):
        return self.color_attr

    def set_text_attr(self,color):
        self.color_attr = color


class ColorText(BaseColorText):
    cons = Console()

    def __init__(self, fg = None, bg = None, txt = '', **kwargs):
        super(ColorText, self).__init__(**kwargs)

        colors = ['0'] # Reset
        if fg:
            colors.append(self.get_fgcolor(fg))
        if bg:
            colors.append(self.get_bgcolor(bg))

        attrs = ';'.join(colors)

        self.color = self.cons.COLOR_FORMAT.format(attributes=attrs)
        self.txt   = txt

        self.write()

    def write(self):
        self.out.write(self.color)
        self.out.write(self.txt)
        self.out.write(self.cons.RESET)



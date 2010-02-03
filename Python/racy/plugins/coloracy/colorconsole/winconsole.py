# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


"""
Colors text in console mode application (win32).
Uses ctypes and Win32 methods SetConsoleTextAttribute and
GetConsoleScreenBufferInfo.

Code inspired from MIT-licensed code from André Burgaud
http://www.burgaud.com/bring-colors-to-the-windows-console-with-python/
"""

__all__ = ["WinConsole", "ColorText"]

from ctypes import windll, Structure, c_short, c_ushort, byref

from base import BaseColorText

SHORT = c_short
WORD = c_ushort

class COORD(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]

class SMALL_RECT(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("Left",   SHORT),
        ("Top",    SHORT),
        ("Right",  SHORT),
        ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)]


class WinConsole(object):

    # winbase.h
    STD_INPUT_HANDLE  = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE  = -12

    # wincon.h
    FOREGROUND_BLACK     = 0x0000
    FOREGROUND_BLUE      = 0x0001
    FOREGROUND_GREEN     = 0x0002
    FOREGROUND_CYAN      = 0x0003
    FOREGROUND_RED       = 0x0004
    FOREGROUND_MAGENTA   = 0x0005
    FOREGROUND_YELLOW    = 0x0006
    FOREGROUND_WHITE     = 0x0007

    BACKGROUND_BLACK     = 0x0000
    BACKGROUND_BLUE      = 0x0010
    BACKGROUND_GREEN     = 0x0020
    BACKGROUND_CYAN      = 0x0030
    BACKGROUND_RED       = 0x0040
    BACKGROUND_MAGENTA   = 0x0050
    BACKGROUND_YELLOW    = 0x0060
    BACKGROUND_WHITE     = 0x0070

    FOREGROUND_INTENSITY = 0x0008
    BACKGROUND_INTENSITY = 0x0080

    def __init__(self, console = "stdout"):
        consoles = {
                'stdin'  : self.STD_INPUT_HANDLE,
                'stderr' : self.STD_ERROR_HANDLE,
                'stdout' : self.STD_OUTPUT_HANDLE,
                }
        handle = consoles[console]
        self.stdout_handle = windll.kernel32.GetStdHandle(handle)
        self.SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
        self.GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

        self.default_colors = self.get_text_attr()
        self.default_fg = self.default_colors & 0x0007
        self.default_bg = self.default_colors & 0x0070

    def get_text_attr(self):
        """Returns the character attributes (colors) of the console screen
        buffer."""
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        self.GetConsoleScreenBufferInfo(self.stdout_handle, byref(csbi))
        return csbi.wAttributes

    def set_text_attr(self,color):
        """Sets the character attributes (colors) of the console screen
        buffer. Color is a combination of foreground and background color,
        foreground and background intensity."""
        self.SetConsoleTextAttribute(self.stdout_handle, color)


class ColorText(BaseColorText):
    stdout = WinConsole()
    stderr = WinConsole('stderr')

    def __init__(self, fg = None, bg = None, txt = '', console='stdout', **kwargs):
        super(ColorText, self).__init__(**kwargs)

        cons = getattr(self, console, self.stdout)
        if fg:
            fgcolor = self.get_fgcolor(fg)
        else:
            fgcolor = cons.default_fg
        if bg:
            bgcolor = self.get_bgcolor(bg)
        else:
            bgcolor = cons.default_bg

        self.color = bgcolor | fgcolor
        self.txt   = txt

        self.write(cons)

    def write(self, cons):
        cons.set_text_attr(self.color)
        self.out.write(self.txt)
        cons.set_text_attr(cons.default_colors)



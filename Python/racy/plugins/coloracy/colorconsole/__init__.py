# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******



__all__ = ["ColorText"]

import platform

if platform.system() == 'Windows':
    from winconsole import ColorText
else:
    from posixconsole import ColorText


def test():
  """Simple test for color_console."""
  import os
  import sys
  ctext = ColorText

  ctext('blue', txt='==========================================='+os.linesep)
  ctext('blue', 'white', txt='And Now for Something ')
  ctext('red', 'white', txt='Completely Different!'+os.linesep)
  ctext('red', txt='==========================================='+os.linesep)
  ctext(txt = 'is_tty : ')
  ctext(txt = str(sys.stdout.isatty()) + os.linesep)

if __name__ == "__main__":
  test()

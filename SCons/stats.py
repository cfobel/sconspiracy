# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

#!/usr/bin/env python
# -*- coding: UTF8 -*-


import pstats
import sys

p = pstats.Stats(sys.argv[1])
#p.sort_stats('time')
p.sort_stats('cumulative')

p.print_stats()

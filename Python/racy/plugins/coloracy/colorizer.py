# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

__all__ = ['Colorizer']

import re

from sys import stdout
from os import linesep
from collections import deque

from colorconsole import ColorText


def get_regex(patterns):
    expressions = []
    expr_fmt = "(?P<n{cnt:04}_{0}>{1})"
    counter  = 0
    for c,m in patterns:
        expr = ""
        for pair in zip(c,m):
            counter += 1
            expr += expr_fmt.format(*pair, cnt=counter)
        expressions.append(expr)
    return "|".join(expressions)



class Colorizer(object):
    """Use colorconsole and regex defined above to write to output a colorized
    text.
    """
    
    def __init__(self, patterns= ([''] , ['^.*$']), type='stdout' ):
        self.queue = deque()
        self.writing = False
        self.regex = re.compile( get_regex(patterns) )
        self.type = type

    def __call__(self, txt, out):
        if self.writing:
            self.queue.append(txt)
        else:
            self.writing = True
            self.write(txt, out)
            while self.queue:
                self.write(self.queue.popleft(), out)
            self.writing = False


    def write(self, txt, out):
        for l in txt.splitlines():
            m = self.regex.match(l)
            if m:
                d = m.groupdict()
                for color in sorted(d.keys()):
                    e = color[6:] # cut the order clue 'nXXXX_'
                    val = d[color]
                    if val:
                        if e:
                            ColorText(fg=e, txt=val, out=out, console=self.type)
                        else:
                            out.write(val)
            else:
                out.write(l)
            out.write(linesep)

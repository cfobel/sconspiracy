# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


ENABLE_COLORACY_KEYWORD = 'COLORACY'
COLORACY_KEYWORD        = 'COLORACY_PATTERNS'

COLORACY_PATTERN_HELP = """Defines colors and patterns that are used to
    colorize output.

    Pattern format:
    [ item1, item2, ... ]

    where itemN is : 
    ([color1, color2, ...], [pattern1, pattern2, ...])
"""

black   = "black"
red     = "red"
green   = "green"
yellow  = "yellow"
blue    = "blue"
magenta = "magenta"
cyan    = "cyan"
white   = "white"
cnone   = ""

cfile     = white
clinenum  = cyan
cerror    = red
cwarning  = yellow
cscons    = cyan

scons_patterns = [
        ([cscons, magenta]       , ['^Target :','.*$']),
        ([cerror]                , ['^scons:.*[eE]rrors?.*$']),
        ([cerror, cfile, cerror] , ['^.*?', '[^:\] ]+', '[:\]].*(interrupted|failed).*$']),
        ([cerror]                , ['^Build failed$']),
        ([cscons, cfile]         , ['^Removed', ' .*']),
        ([cscons, cfile, cscons, cfile, cscons] , ['^Install .+?[\'"]', '.*?', '[\'"].*?[\'"]', '.*?', '[\'"].*$']),

        # exception header : +-[Error]: PRJError =========
        ([yellow, red, yellow, magenta, yellow], ['^\+-\[', '[^\]]+', '\]: ', '\w+', '.*$']),
        # exception body
        ([yellow, blue], ['^\|', '.*$' ]),
        # exception footer
        ([yellow], ['^\+-+$']),

        ([cscons], ['^scons:.*$']),
        ([cscons], ['^"+$']),
        ]

msvs_patterns = [
        ([magenta, blue, magenta]   , ['^[^\W]*(cl|link)[0-9\-\.]* .*?', '(\W[^ ]+\.(cpp|cc|cxx|c|lib|dll))' ,'.*$']),

        ([cfile,cnone,clinenum,cnone, cerror, cyan]   , ['^[^(]+', '\(', '\d+', '\) :\W*',  'error'  , '.*$']),
        ([cfile,cnone,clinenum,cnone, cwarning, cyan] , ['^[^(]+', '\(', '\d+', '\) :\W*',  'warning', '.*$']),
        ]

gcc_patterns = [
        #gcc command
        #([magenta, blue, magenta]   , ['^[^\W]*(gcc|g\+\+)[0-9\-\.]* .*?', '(\W[^ ]+\.(cpp|cc|cxx|c|so|dylib))' ,'.*$']),
        ([magenta, blue, magenta]   , ['^[^\W]*(gcc|g\+\+)[0-9\-\.]* .*?', '-o (\W[^ ]+)' ,'.*$']),

        #gcc errors, warnings, In *
        ([cfile,cnone,clinenum,cnone, cerror, cyan]   , ['^[^:]+', ':', '\d+', ':\W*', 'error:', '.*$']),
        ([cnone, cerror, cyan]   , ['^.*', 'error', '.*$']),
        ([cfile,cnone,clinenum,cnone, cwarning, cyan] , ['^[^:]+', ':', '\d+', ':\W*', 'warning:', '.*$']),
        ([cfile,cnone, cyan]                          , ['^[^:]+', ':\W*', 'In.*$']),

        ([cfile,cnone,clinenum,cnone] , ['^/.*', ':', '\d+', ':.*$']), # /a/file:num: *
        ]

default_patterns = [ ([cnone] , ['^.*$']) ]

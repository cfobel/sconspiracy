# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******



class InfoLogger(object):
    def __init__(self):
        self.info = {}
        self.reset()

    def _get(self, key):
        return ", ".join(self.info[key])

    def log(self, info, value, append=True):
        value = str(value)
        if append:
            log = self.info.get(info, [])
            log.append(value)
        else:
            log = [value]
        self.info[info] = log
        self.max_len_info   = max(self.max_len_info, len(info))
        self.max_len_value  = max(self.max_len_value, len(self._get(info)))

    def reset(self):
        self.info.clear()
        self.max_len_info  = 0
        self.max_len_value = 0

    def __str__(self):
        import os
        max_info = self.max_len_info
        max_len  = max_info + self.max_len_value + 3
        info     = [" : ".join([i.rjust(max_info), self._get(i)]) 
                        for i in sorted(self.info.keys())]
        sep      = ['"'*max_len]
        return os.linesep.join(sep + info + sep)

info = InfoLogger()

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from racy.rutils import cached_property

class Target(object):
    """Grab and store the name, the list of args and the dictionnary of options
    given in 'target'.  Target's format : 

        Name/foo/OPT1:val1/OPT2:[val2a,val2b,...]/+bar
    
    This example will grab :
        name = 'Name'
        args = ['foo','+bar']
        opts = {'OPT1':'val1', 'OPT2':['val2a','val2b',...]}
    """

    SEP = '/'
    AFFECT_OP = ':'

    __splitted = None
    target_str = None

    def __init__(self, target):
        self.__splitted = target.split(self.SEP)
        self.target_str = target

    @property
    def name(self):
        return self.__splitted[0]

    @name.setter
    def name(self, value):
        self.__splitted[0] = value

    @cached_property
    def args(self):
        op = self.AFFECT_OP
        return [el for el in self.__splitted[1:] if op not in el]

    @cached_property
    def opts(self):
        import racy.rutils as rutils
        op = self.AFFECT_OP
        opts = [el.split(op) for el in self.__splitted[1:] if op in el]
        return dict( (k,rutils.ListFromStr.get_list(v)) for k,v in opts )

class TargetDB(dict):
    def get(self, key):
        return super(TargetDB, self).get(Target(key).name, Target(''))


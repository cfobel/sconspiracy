# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

from libexterror import LibextError


class NodeHolder(object):

    def __init__(self):
        self._node = None

    @property
    def node(self):
        node = self._node
        if node is None:
            raise LibextError, "Node uninitialized"
        return node

    @node.setter
    def node(self, n):
        self._node = n

    @staticmethod
    def unwrap(iterable):
        def unwrap_filter(a):
            if isinstance(a, NodeHolder):
                return a.node
            return a

        def unwrap_dict_item(item):
            k,v = item
            return k, unwrap_filter(v)

        if isinstance(iterable, dict):
            res = dict(map(unwrap_dict_item, iterable.items()))
        else:
            res = map(unwrap_filter, iterable)

        return res

# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******

from racy import rutils
from nodeholder     import NodeHolder

class BuilderWrapper(object):
    _called_builders = {}

    def __init__(self, prj, name, builder = None, reg_name = None):
        self.prj                   = prj
        self.builder_name          = name
        self.builder_reg_name      = reg_name if reg_name else name
        self.builder               = builder
        self._called_builders[prj] = []

    @property
    def called_builders(self):
        return self._called_builders[self.prj]

    def __call__(self, *args, **kwargs):
        nodewrap = NodeHolder()
        call = (self.builder_name, self.builder, args, kwargs, nodewrap)
        self.called_builders.append(call)
        return nodewrap

    def subscribe_to(self, dict):
        dict[self.builder_reg_name] = self

    @staticmethod
    def apply_calls(prj, *args, **kwargs):
        env = prj.env
        called_builders = BuilderWrapper._called_builders[prj]
        results = []
        for (name, builder, call_args, call_kwargs, ndwrap) in called_builders:
            if builder is None:
                builder = getattr(env, name)
            if builder is None:
                raise LibextError, "Builder " + name + "Not found"
            builder_args = []
            builder_args.extend(NodeHolder.unwrap(call_args))
            builder_args.extend(args)
            builder_kwargs = {}
            builder_kwargs.update(NodeHolder.unwrap(call_kwargs))
            builder_kwargs.update(kwargs)
            node = ndwrap.node = builder(*builder_args, **builder_kwargs)
            if node:
                if name == 'Download':
                    if rutils.is_false(prj.get('CLEAN_DOWNLOADS')):
                        prj.env.NoClean(node)
                results.append(node)
        return results


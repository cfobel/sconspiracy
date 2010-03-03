# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


import os 

import racy

from collections  import defaultdict
from itertools    import cycle
from racy.rlibext import register as libext_reg




def get_base(cls):
    """Return cls's base class (the last in hierarchy that is not 'object').
    Works only with new style classes.
    """
    if cls.__base__ is object:
        return cls.__name__
    else:
        return get_base(cls.__base__)



def generate_graph(filter = []):
    colors = cycle([ '"/pastel28/{0}"'.format(n) for n in range(1,9) ])

    clslist  = []
    clsdict  = {}
    clusters = defaultdict(list)

    def load_module_callback (cls, **kwargs):
        if cls.debug:
            clslist.append(cls)

    def load_binpkgs_callback(reg, **k):
        reg.load_module(callback=load_module_callback, **k)

    libext_reg.load_binpkgs(
            racy.renv.dirs.binpkg,
            callback=load_binpkgs_callback
            )

    for c in clslist:
        if c.register_names:
            c.name = c.register_names[0]
            base   = get_base(c)
            if not filter or c.name in filter or base in filter:
                clsdict[c.name] = c
                cluster_name    = base
                clusters[cluster_name].append(c)


    gv_edges = []
    gv_nodes = []

    for name,node in clsdict.items():
        for dependency_name in getattr(node, 'depends_on', []):
            gv_edges.append( '"{0}"->"{1}";'.format(name, dependency_name) )

        node.libs = getattr(node,'libs',[])
        property = '"{n.name}" [label="{{{n.name}|{n.libs}}}"];'
        gv_nodes.append( property.format(n=node()) )

    def get_clusters(clusters):
        gv_clusters= []
        for cl_name, nodes in clusters.items():
            gv_clusters.append("subgraph cluster_"+cl_name)
            gv_clusters.append("{")
            gv_clusters.append("style=filled;color={0};".format(colors.next()))
            for node in nodes:
                gv_clusters.append('"{0}";'.format(node.name))
            gv_clusters.append("}")
        return os.linesep.join(gv_clusters)

    def get_gv_graph(edges, nodes, clusters):
        gv_graph = []
        gv_graph.append('digraph G')
        gv_graph.append('{')
        gv_graph.append('rankdir=BT;')
        gv_graph.append('node [shape=record, style=rounded]')
        gv_graph.append( os.linesep.join(nodes) )
        gv_graph.append( os.linesep.join(edges) )
        gv_graph.append( get_clusters(clusters) )
        gv_graph.append('}')

        return os.linesep.join(gv_graph)
    
    return get_gv_graph(gv_edges, gv_nodes, clusters)

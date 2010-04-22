# -*- coding: UTF8 -*-

import string
import UserDict

import SCons.Errors
import SCons.Node
import SCons.Util

import urllib2


class URLNameSpace(UserDict.UserDict):
    def URL(self, name, **kw):
        if isinstance(name, URL):
            return name
        try:
            a = self[name]
        except KeyError:
            a = apply(URL, (name,), kw)
            self[name] = a
        return a

    def lookup(self, name, **kw):
        try:
            return self[name]
        except KeyError:
            return None

class URLNodeInfo(SCons.Node.NodeInfoBase):
    current_version_id = 1
    field_list = ['csig']
    def str_to_node(self, s):
        return default_uns.URL(s)

class URLBuildInfo(SCons.Node.BuildInfoBase):
    current_version_id = 1

class URL(SCons.Node.Node):

    NodeInfo = URLNodeInfo
    BuildInfo = URLBuildInfo

    def __init__(self, url):
        SCons.Node.Node.__init__(self)
        self.name = url

    def str_for_display(self):
        return '"' + self.__str__() + '"'

    def __str__(self):
        return self.name

    def make_ready(self):
        self.get_csig()

    really_build = SCons.Node.Node.build
    is_up_to_date = SCons.Node.Node.children_are_up_to_date

    def is_under(self, dir):
        # Make URL nodes get built regardless of
        # what directory scons was run from. URL nodes
        # are outside the filesystem:
        return 1

    def get_contents(self):
        """The contents of an alias is the concatenation
        of the content signatures of all its sources."""
        childsigs = map(lambda n: n.get_csig(), self.children())
        return string.join(childsigs, '')

    def sconsign(self):
        """An URL is not recorded in .sconsign files"""
        pass

    #
    #
    #

    def changed_since_last_build(self, target, prev_ni):
        cur_csig = self.get_csig()
        try:
            return cur_csig != prev_ni.csig
        except AttributeError:
            return 1

    def build(self):
        """A "builder" for aliases."""
        pass

    def convert(self):
        try: del self.builder
        except AttributeError: pass
        self.reset_executor()
        self.build = self.really_build

    def get_csig(self):
        """
        Generate a node's content signature, the digested signature
        of its content.

        node - the node
        cache - alternate node to use for the signature cache
        returns - the content signature
        """
        try:
            return self.ninfo.csig
        except AttributeError:
            pass

        contents = self.get_contents()
        csig = SCons.Util.MD5signature(contents)
        self.get_ninfo().csig = csig
        return csig

    def exists(self):
        try:
            self.url = urllib2.urlopen(self.name)
            res = True
        except urllib2.HTTPError, e:
            res = False
            print "URL Error:",e.reason , self.name
        except urllib2.URLError, e:
            res = False
            print "URL Error:",e.reason , self.name
        return res

    def write_to_file(self, io, filename, file_mode=''):
        print 'downloading ' + self.name + '...'

        with open(filename, "w" + file_mode) as local_file:
            local_file.write(io.read())

        print 'done'



    @staticmethod
    def Download(target, source, env):
        assert (len(target) == len(source))
        for s,t in zip(source, target):
            s.write_to_file(s.url, t.get_path(), file_mode='')
        return None




default_uns = URLNameSpace()

SCons.Node.arg2nodes_lookups.append(default_uns.lookup)

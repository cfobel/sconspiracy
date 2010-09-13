# -*- coding: UTF8 -*-

import os
import string
import UserDict

import SCons.Node
import SCons.Util

import urllib2
from urlparse import urlparse

import racy

class UrlNameSpace(UserDict.UserDict):
    def Url(self, name, **kw):
        if isinstance(name, Url):
            return name
        try:
            a = self[name]
        except KeyError:
            a = apply(Url, (name,), kw)
            self[name] = a
        return a

    def lookup(self, name, **kw):
        try:
            return self[name]
        except KeyError:
            return None

class UrlNodeInfo(SCons.Node.NodeInfoBase):
    current_version_id = 1
    field_list = ['csig']
    def str_to_node(self, s):
        return default_uns.Url(s)

class UrlBuildInfo(SCons.Node.BuildInfoBase):
    current_version_id = 1

class Url(SCons.Node.Node):

    NodeInfo = UrlNodeInfo
    BuildInfo = UrlBuildInfo

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
        # Make Url nodes get built regardless of
        # what directory scons was run from. Url nodes
        # are outside the filesystem:
        return 1

    def get_contents(self):
        """The contents of an url is the concatenation
        of the content signatures of all its sources."""
        childsigs = map(lambda n: n.get_csig(), self.children())
        return string.join(childsigs, '')

    def sconsign(self):
        """An Url is not recorded in .sconsign files"""
        pass


    def changed_since_last_build(self, target, prev_ni):
        cur_csig = self.get_csig()
        try:
            return cur_csig != prev_ni.csig
        except AttributeError:
            return 1

    def build(self):
        """A "builder" for Url."""
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
        res = False
        pieces = urlparse(self.name)
        if not all([pieces.scheme, pieces.netloc]):
            raise Exception, 'Malformed Url: {0}'.format(self.name)
        return True

    def write_to_file(self, io, filename, file_mode=''):
        size = 0
        with open(filename, "wb" + file_mode) as local_file:
            racy.rutils.buffered_copy(io, local_file)
            size = local_file.tell()

        racy.print_msg( 'Downloaded', self.name, size, 'bytes' )



def Download(target, source, env):
    if not len(target) == len(source):
        raise Exception, ("Number of target ({0}) must be equal to the number "
                          "of sources ({1})".format(len(target), len(sources)))
    for s,t in zip(source, target):
        stream = urllib2.urlopen(s.name, timeout=10)
        s.write_to_file(stream, t.get_path(), file_mode='')
        stream.close()
    return None


def DownloadString(target, source, env):
    s = ' Downloading %s' % source[0]
    return env.subst('[${CURRENT_PROJECT}]: ') + s


def generate(env):
    env.Url = Url
    SCons.Node.FS.get_default_fs().Url = Url
    action = SCons.Action.Action(Download, DownloadString)
    builder = env.Builder(
            action=action ,
            source_factory = Url,
            )

    env.Append(BUILDERS = {'Download' : builder})


default_uns = UrlNameSpace()

SCons.Node.arg2nodes_lookups.append(default_uns.lookup)


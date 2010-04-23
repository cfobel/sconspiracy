# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


from __future__ import print_function

import os


#------------------------------------------------------------------------------
class Undefined:
    def __nonzero__(self):
        return False

Undefined = Undefined()

NotUsed = Undefined

MSG_WIDTH = 79


#------------------------------------------------------------------------------
class RacyException(Exception):
    def __init__(self, *args, **kwargs):
        import traceback
        self.traceback = traceback.extract_stack()
        super(RacyException, self).__init__(*args, **kwargs)
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

#------------------------------------------------------------------------------
class OptionError(RacyException):
    pass


#------------------------------------------------------------------------------
class EnvError(RacyException):
    pass


#------------------------------------------------------------------------------
class LibExtException(RacyException):
    pass


#------------------------------------------------------------------------------
class LibError(RacyException):
    msg_template = ''

    def init(self, bad_libs, prj):
        self.msg = messages = []
        db = prj.projects_db

        for lib in bad_libs:
            msg = self.msg_template
            self.msg.append( msg.format(lib=lib, prj=prj, cur_lib=db[lib]) )

    def __str__(self):
        return os.linesep.join(self.msg)


class LibMissingVersion(LibError):
    msg_template = ('Missing <{lib.name}> vesion in <{prj.name}> options '
                    '[{prj.opts_source}]. Current is <{lib.versioned_name}>.')



class LibBadVersion(LibError):
    msg_template = ('<{lib}> in <{prj.name}> options [{prj.opts_source}] '
                    'should be updated to <{cur_lib.versioned_name}>.')



#------------------------------------------------------------------------------
class ConfigError(RacyException):
    pass

class ConfigVariantError(ConfigError):
    pass


#------------------------------------------------------------------------------
class RacyProjectError(RacyException):
    def init(self, prj, message):
        self.prj = prj
        self.msg = message
    def __str__(self):
        prj = self.prj
        return '[{0.full_name}] : {1}'.format( prj, self.msg.format( prj = prj ) )


#------------------------------------------------------------------------------
class RacyCommandLineError(RacyException):
    pass


#------------------------------------------------------------------------------
class RacyPluginError(RacyException):
    pass



#------------------------------------------------------------------------------
class RacyAttributeException(RacyException):
    def init(self, obj, attr, msg):
        self.obj  = obj
        self.attr = attr
        self.msg = msg
    def __str__(self):
        desc = None
        #using hasattr because getattr(obj, attr, default) will raise an 
        # exception if obj has <no_undef_attr_read>
        if hasattr(self.obj, 'desc'):
            desc = getattr(self.obj, 'desc', None)
        msg = ("In file {file[0]}:{file[1]}, {obj.__class__} has no attribute "
               "<{attr}>, can't {msg}.{desc}")
        
        descmsg = ""
        if desc:
            descmsg = ' Instance description: {1}]]'.format(os.linesep,desc)
        msg = msg.format(
                obj  = self.obj,
                desc = descmsg,
                attr = self.attr,
                msg  = self.msg,
                file = self.traceback[-3]
                )
        return msg


#------------------------------------------------------------------------------
def no_undef_attr_read(cls):
    def __getattr__(self, attr):
        if attr.startswith('__racy_internal'):
            raise AttributeError
        else:
            raise RacyAttributeException(self, attr, 'read')
    cls.__getattr__ = __getattr__
    return cls

def no_undef_attr_write(cls):
    def __setattr__(self, attr, value):
        if not hasattr(self, attr) and not attr.startswith('__racy_internal'):
            msg = 'write "{0}"'.format(str(value))
            raise RacyAttributeException(self, attr, msg)
        else:
            object.__setattr__(self,attr,value)
    cls.__setattr__ = __setattr__
    return cls


#------------------------------------------------------------------------------
def load_plugins():
    import racy
    import racy.rplugins
    plugins_path = os.path.join(os.path.dirname(racy.__file__), 'plugins')
    racy.rplugins.register.load_dir( plugins_path )


#------------------------------------------------------------------------------
def racy_msg (level, title, msg, wrap, width=MSG_WIDTH):
    import textwrap
    if wrap:
        wrap_args = {
                'initial_indent'    : '|  ',
                'subsequent_indent' : '|  ',
                'replace_whitespace': False,
                'drop_whitespace'   : False,
                'break_long_words'  : False,
                }
        msg = textwrap.fill(str(msg), width, **wrap_args)
    msg = [
        '+-[{0}]: {1} '.format(level.upper(), title).ljust(width,'='),
        msg,
        '+' + '-'*(width-1),
        ]
    return msg

def print_msg( *msg ):
    print (' '.join((str(m) for m in msg)))

errors = []
def print_error(title, error, wrap=True):
    errors.append((title, errors))
    print (os.linesep.join(racy_msg('Error', title, error, wrap)))

def print_warning(title, warning, wrap=True):
    print (os.linesep.join(racy_msg('Warning', title, warning, wrap)))

def get_last_exception_traceback():
    import traceback
    import sys
    err, detail, tb = sys.exc_info()
    tb = os.linesep*2 + ''.join(traceback.format_tb(tb))
    return tb

def manage_exception(e, default_print = print_error):
    from renv.options import get_option
    if get_option('RACY_DEBUG') == 'yes':
        print_msg(get_last_exception_traceback())
    print_error(e.__class__.__name__, e)


#------------------------------------------------------------------------------
def path(dir=None):
    root = os.path.dirname(__file__)
    if dir:
        root = os.path.join(root, dir)
    return root


#------------------------------------------------------------------------------
def ressources(file):
    rc = path("rc")
    if file:
        rc = os.path.join(rc, file)
    return rc

#------------------------------------------------------------------------------


try:
    import renv
except RacyException, e:
    manage_exception(e)


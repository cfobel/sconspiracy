# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
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
class YamsException(Exception):
    def __init__(self, *args, **kwargs):
        import traceback
        self.traceback = traceback.extract_stack()
        super(YamsException, self).__init__(*args, **kwargs)
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

#------------------------------------------------------------------------------
class OptionError(YamsException):
    pass


#------------------------------------------------------------------------------
class EnvError(YamsException):
    pass


#------------------------------------------------------------------------------
class LibExtException(YamsException):
    pass


#------------------------------------------------------------------------------
class LibError(YamsException):
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
                    '[{prj.opts_path}]. Current is <{lib.versioned_name}>.')



class LibBadVersion(LibError):
    msg_template = ('<{lib}> in <{prj.name}> options [{prj.opts_path}] '
                    'should be updated to <{cur_lib.versioned_name}>.')



#------------------------------------------------------------------------------
class ConfigError(YamsException):
    pass

class ConfigVariantError(ConfigError):
    pass


#------------------------------------------------------------------------------
class YamsProjectError(YamsException):
    def init(self, prj, message):
        self.prj = prj
        self.msg = message
    def __str__(self):
        prj = self.prj
        return '[{0.full_name}] : {1}'.format( prj, self.msg.format( prj = prj ) )


#------------------------------------------------------------------------------
class YamsCommandLineError(YamsException):
    pass


#------------------------------------------------------------------------------
class YamsPluginError(YamsException):
    pass



#------------------------------------------------------------------------------
class YamsAttributeException(YamsException):
    def init(self, obj, attr, msg):
        self.obj  = obj
        self.attr = attr
        self.msg = msg
    def __str__(self):
        msg = ("In file {file[0]}:{file[1]}, {obj.__class__} has no attribute <{attr}>, can't "
               "{msg}")
        
        msg = msg.format(obj=self.obj, attr=self.attr, msg=self.msg, 
                file = self.traceback[-3] )
        return msg


#------------------------------------------------------------------------------
def no_undef_attr_read(cls):
    def __getattr__(self, attr):
        if attr.startswith('__yams_internal'):
            raise AttributeError
        else:
            raise YamsAttributeException(self, attr, 'read')
        
    cls.__getattr__ = __getattr__
    return cls

def no_undef_attr_write(cls):
    def __setattr__(self, attr, value):
        if not hasattr(self, attr) and not attr.startswith('__yams_internal'):
            msg = 'write "{0}"'.format(str(value))
            raise YamsAttributeException(self, attr, msg)
        else:
            object.__setattr__(self,attr,value)
    cls.__setattr__ = __setattr__
    return cls
    

#------------------------------------------------------------------------------
def load_plugins():
    import yams
    import yams.yplugins
    plugins_path = os.path.join(os.path.dirname(yams.__file__), 'plugins')
    yams.yplugins.register.load_dir( plugins_path )

    
#------------------------------------------------------------------------------
def yams_msg (level, title, msg, wrap, width=MSG_WIDTH):
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

def print_msg( msg ):
    print (msg)

errors = []
def print_error(title, error, wrap=True):
    errors.append((title, errors))
    print (os.linesep.join(yams_msg('Error', title, error, wrap)))

def print_warning(title, warning, wrap=True):
    print (os.linesep.join(yams_msg('Warning', title, warning, wrap)))

def manage_exception(e):
    from yenv.options import get_option
    if get_option('YAMS_DEBUG') == 'yes':
        import traceback
        print_msg (os.linesep.join(traceback.format_list(e.traceback[:-1])))
    print_error(e.__class__.__name__, e)


try:
    import yenv
except YamsException, e:
    manage_exception(e)

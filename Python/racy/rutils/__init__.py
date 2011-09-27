# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******



import exceptions
import os
import re

from os.path import join, isfile, normpath


#------------------------------------------------------------------------------

def buffer_generator(file_src, size):
    """Return a generator returning buffers of 'size' size from file_src
    stream.
    """
    while True:
        buf = file_src.read(size)
        if not buf:
            break
        yield buf


#------------------------------------------------------------------------------

def buffered_copy(file_src, file_dst, buffer_size = 4*1024*1024):
    for chunk in buffer_generator(file_src, buffer_size):
        file_dst.write(chunk)


#------------------------------------------------------------------------------

def decorator(_decorator):
    """This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied."""

    def copy_attributes(src, dst):
        if not isinstance(dst, property):
            dst.__name__ = src.__name__
            dst.__doc__  = src.__doc__
            dst.__dict__.update(src.__dict__)

    def new_decorator(f):
        g = _decorator(f)
        copy_attributes(f,g)
        return g

    copy_attributes(_decorator ,new_decorator)
    return new_decorator



#------------------------------------------------------------------------------
def get_re_from_extensions(extensions):
    """ Return a compiled regex from a list of extensions or a regex
        
    Example : for ['cpp','hxx','c'] the returned regex is '.*\\.(cpp|hxx|c)$'
    and matches strings that ends with '.cpp', '.hxx' or '.c'
    """
    if not extensions:
        reg = '.*'
    elif isinstance(extensions, list):
        reg = '.*\.({0})$'.format('|'.join(extensions))
    else: 
        reg = extensions
    return re.compile(reg)

#------------------------------------------------------------------------------
def remove_vcs_dirs(dirs):
    """ Remove vcs dirs from a list """
    import racy.renv.constants as constants
    for dir in constants.VCS_DIRS:
        if dir in dirs:
            dirs.remove(dir)


#------------------------------------------------------------------------------
def _match_any(v, values):
    """Returns True if v is a value in values. If values contains strings,
    then the strings has to be in lowercase.
    """
    if isinstance(v, basestring): v = v.lower()
    return v in values


#------------------------------------------------------------------------------
def is_false(v):
    """Returns True if v is a value in ['no', 'false', 'off', 0, False, None]"""
    return _match_any(v, ['no', 'false', 'off', 0, False, None])


#------------------------------------------------------------------------------
def is_true(v):
    """Returns True if v is a value in ['yes', 'true', 'on', 1, True]"""
    return _match_any(v, ['yes', 'true', 'on', 1, True])




#------------------------------------------------------------------------------
def DeepGlob(extensions, src_dir= '.', replace_dir = '', return_orig = False, 
        invert_matches = False, filter = lambda x:True):
    """ Do a deep Glob, lookin up for file matching extensions, in 
    src_dir (default '.'), replacing srd_dir by replace_dir if given.

    if invert_matches is True, DeepGlob will return files that doesn't 
    match with extensions

    Accept regex as extensions (don't use '^')
    if extensions is None, match all files
    """
    if is_iterable(src_dir):
        kwargs = {
        'extensions'     : extensions,
        'src_dir'        : None,
        'replace_dir'    : None,
        'return_orig'    : return_orig,
        'invert_matches' : invert_matches,
        'filter'         : filter
        }
        result = []
        if not is_iterable(replace_dir):
            replace_dir = [replace_dir] * len(src_dir)

        for dir, replace in zip(src_dir, replace_dir):
            kwargs['src_dir']     = dir
            kwargs['replace_dir'] = replace
            result += DeepGlob(**kwargs)
        if return_orig:
            cat = lambda a,b: (a[0]+b[0], a[1]+b[1])
            if len(result)>1:
                result = reduce(cat, result)

    else:
        replace_dir = normpath(replace_dir)
        src_dir     = normpath(src_dir)
        regex       = get_re_from_extensions(extensions)
        file_match  = regex.match # cache the function
        result      = []

        if invert_matches:
            file_match = lambda x: not regex.match(x)

        for root, dirs, files in os.walk(src_dir, topdown=True):
            #don't walk in vcs dirs
            remove_vcs_dirs(dirs)
            result += [ join(root, name) for name in files if file_match(name) ]
            result = [res for res in result if filter(res)]

        if replace_dir:
            result_orig = result
            norm = lambda f:normpath(f).replace(src_dir, replace_dir, 1)
            result = map(norm, result)

        if return_orig and replace_dir:
            result = result_orig, result

    return result


#------------------------------------------------------------------------------
def mkdir_p(path):
    """Create the directory and intermediate directories as required by path.
    raise an exceptions only if path exists and is not a dir.
    """
    try:
        os.makedirs(path)
    except exceptions.OSError, exc:
        import errno
        if not (exc.errno == errno.EEXIST and os.path.isdir(path)):
            raise

#------------------------------------------------------------------------------
def copy (src, dst, preserve_links=True, preserve_relative_links_only = True):
    import shutil
    action = lambda s, d : None
    action_kwargs = {}

    #never true if symlinks not supported
    if preserve_links and os.path.islink(src):
        linktarget = os.readlink( src )

        if preserve_relative_links_only and os.path.isabs(linktarget):
            action = shutil.copy
        else:
            src = linktarget
            action = os.symlink


        if os.path.exists(dst): 
            os.unlink(dst)

    elif os.path.isdir(src):
        #mkdir_p(dst)
        action = shutil.copytree
        action_kwargs['symlinks'] = preserve_links
    else:
        action = shutil.copy

    #hack to manage some symlinks errors
    try:
        if not os.path.exists(os.path.split(dst)[0]):
            mkdir_p(os.path.split(dst)[0])
        action(src, dst, **action_kwargs)
    except exceptions.OSError, e:
        import errno
        if not e.errno == errno.EEXIST:
            raise e
        
#------------------------------------------------------------------------------
def symlink(src, dest):
    if os.name == 'posix':
        import posix as platform
    else:
        import win as platform

    platform.symlink(src,dest)


#------------------------------------------------------------------------------
def get_first_existing_file(files):
    """Returns first existing file from files. If an item of files is a list,
    the list items are first joined."""
    for file in files:
        if hasattr(file,'__iter__'):
            file = join(*file)
        if isfile(file):
            return file


#------------------------------------------------------------------------------
def tupleize(iterable):
    """Recursively <tupleize> an iterable to obtain a hashable object"""
    if hasattr(iterable, "__iter__"):
        if isinstance(iterable, dict):
            iterable = iterable.items()
        return tuple( tupleize(el) for el in iterable )
    return iterable


#------------------------------------------------------------------------------
@decorator
def memoize(f, cache={}):
    """Memoization decorator. Store the computed values in 'cache'. If cache is
    not specified, every results will be store in the same dict (the one in the
    decorator's defautls value)
    *WARNING* : If tuple is used instead of tupleize, a parameter in args or
    kwargs or is unhashable, the decorated function will raise a TypeError
    """
    def g(*args, **kwargs):
        key = ( f, tupleize(args), tupleize(kwargs.items()) )
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return g


@decorator
def cached_property(f):
    """Returns a cached property that is computed by function f. Be carefull
    with setter and deleter uses (they shouldn't be used with a
    cached_property).
    """
    def func(self):
        prefix = '__racy_internal__cached_property'
        fullname = "_".join([prefix, f.__name__])
        if hasattr(self, fullname):
            return getattr(self, fullname)
        res = f(self)
        setattr(self, fullname, res)
        return res


    func.__name__ = f.__name__
    #p = property(memoize(f)) 
    # not memoized anymore for property -> optimized
    p = property(func)
    return p


@decorator
def run_once(f):
    """This decorator ensure that an instance method is executed once
    and return ever the same result, without any regards on arguments
    """
    def func(self, *a, **k):
        prefix = '__racy_internal__used'
        fullname = "_".join([prefix, f.__name__])
        used = getattr(self, fullname, 0)
        res = None
        if used < 1:
            res = f(self, *a, **k)
        setattr(self, fullname, used+1)
        return res
    return func

#------------------------------------------------------------------------------
@decorator
def time_it(func):
    """Internal use, class method timing decorator"""
    import time
    func.__tot  = 0.
    func.__call = 0
    def _inner(*args, **kw):
        func.__call += 1
        start = time.time()
        res = func(*args, **kw)
        timed = time.time() - start
        func.__tot += timed

        msg = '{0:20}: {1:15}  avg: {2:15}  tot: {3:15}  calls: {4:6}'
        msg = msg.format(func.__name__, timed,
                func.__tot/func.__call, func.__tot, func.__call)
        print msg
        return res
    return _inner


def merge_lists_of_dict(dict_dest, dict_src):
    """Merge two dict of list in dict_dest"""
    for el, val in dict_src.items():
        dict_dest[el] += val


#------------------------------------------------------------------------------
def is_iterable(obj):
    return hasattr(obj, "__iter__")
def iterize(obj):
    return obj if is_iterable(obj) else [obj]


#------------------------------------------------------------------------------
def put_file_content(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

#------------------------------------------------------------------------------
def get_file_content(filename):
    read_data = None
    with open(filename, 'r') as f:
        read_data = f.read()
    return read_data

#------------------------------------------------------------------------------
class ListFromStr(list):
    """Build a list from a string if it contain a list. Examples : 
       '[foo,bar,6]' gives ['foo','bar','6']
       'foo,bar,6' gives []
    """
    def __init__(self, s):
        super(ListFromStr, self).__init__()
        if s.startswith('[') and s.endswith(']'):
            self[:] = s[1:-1].split(',')

    @staticmethod
    def get_list(s):
       """Return a list from a string. the string must contain [ and ] to
       define a list, else the string will be returned as is.
       """
       lst = ListFromStr(s)
       if not lst:
           lst = s
       return lst


#------------------------------------------------------------------------------
def uniq(iterable):
    """Return a list from iterable without duplicates, keep the order of
    appearance of the iterable elements"""
    seen = set()
    add  = seen.add
    return [x for x in iterable if not (x in seen or add(x))]

#------------------------------------------------------------------------------


class Version(str):
    """This class provide a way to compare/normalize versions strings.
    Version format is [name]v1<sep>v2<sep>...<sep>vn where :
      - v1 ... vn are components of version (ex: 5 and 4 for 5.4)
      - <sep> is a separating char from [-_.]
      - [name] is an optionnal name composed with [a-zA-Z-_.]

    [name] is ignore for comparison.

    examples of True assertions: 
     - Version('gcc4.3') < Version('gcc4.4')
     - Version('0.9') < Version('1')
     - Version('1.9') < Version('1.10')
    """

    separator = re.compile('[-_.]')


    @property
    def dotted (self):
        return self.separator.sub('.', self)

    @property
    def dashed (self):
        return self.separator.sub('-', self)

    @property
    def underscored (self):
        return self.separator.sub('_', self)

    @property
    def normalized (self):
        return self.dashed

    @property
    def to_tuple(self):
        filtered = re.sub('^[a-zA-Z-_.]+','',self)
        splited = self.separator.split(filtered)
        return tuple( int(el) for el in splited )

    def __str__(self):
        return self.normalized

    def __repr__(self):
        return self.normalized.join(["'", "'"])


    def __lt__(self, other):
        if isinstance(other, Version):
            return self.to_tuple < other.to_tuple
        str.__lt__(self, other)

    def __le__(self, other):
        if isinstance(other, Version):
            return self.to_tuple <= other.to_tuple
        str.__le__(self, other)

    def __eq__(self, other):
        if isinstance(other, Version):
            return self.to_tuple == other.to_tuple
        str.__eq__(self, other)

    def __ne__(self, other):
        if isinstance(other, Version):
            return self.to_tuple != other.to_tuple
        str.__ne__(self, other)

    def __gt__(self, other):
        if isinstance(other, Version):
            return self.to_tuple > other.to_tuple
        str.__gt__(self, other)

    def __ge__(self, other):
        if isinstance(other, Version):
            return self.to_tuple >= other.to_tuple
        str.__ge__(self, other)


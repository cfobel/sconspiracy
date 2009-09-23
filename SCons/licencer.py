# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******
import os
import textwrap

licence = {}
comments = {}

comments['.cpp'] = {
        'beginblock' : '/* ' ,
        'endblock'   : ' */' ,
        'indent'     : ' * ' ,
        }

comments['.py'] = {
        'beginblock' : '# ' ,
        'endblock'   : ''   ,
        'indent'     : '# ' ,
        }

comments['.hpp'] = comments['.cpp']
comments['.c'] = comments['.cpp']
comments['.h'] = comments['.cpp']
comments['.cxx'] = comments['.cpp']
comments['.hxx'] = comments['.cpp']
comments['.py'] = comments['.py']

ignore_lines = ['vim:', 'utf8', 'UTF8']
licence['begin'] = '***** BEGIN LICENSE BLOCK *****'
licence['end']   = '****** END LICENSE BLOCK ******'
licence['newbegin'] = '***** BEGIN LICENSE BLOCK *****'
licence['newend']   = '****** END LICENSE BLOCK ******'

licence['LGPL'] = """FW4SPL - Copyright (C) IRCAD, 2009.
Distributed under the terms of the GNU Lesser General Public License (LGPL) as
published by the Free Software Foundation.  """

licence['BSD'] = """Sconspiracy - Copyright (C) IRCAD, 2004-2009.
Distributed under the terms of the BSD Licence as
published by the Open Source Initiative.  """

sep = '\n'

def get_licence_block(filetype, licence_content):
    if filetype not in comments:
        raise KeyError, \
                "Don't know how to write in '{0}' files".format(filetype)

    com = comments[filetype]

    #content = textwrap.wrap(
            #licence_content,
            #initial_indent    = com['indent'],
            #subsequent_indent = com['indent'],
            #width = 80,
            #)

    content = [com['indent'] + el for el in licence_content.split(sep)]

    header  = ''.join([ com['beginblock'], licence['newbegin'] ])
    content = sep.join(content)
    footer  = ''.join([ com['indent'], licence['newend'], com['endblock'] ])

    licenceblock = [ header, sep, content, sep, footer, sep]
    return licenceblock


def find_first_matching( needles, haystack, offset = 0):
    for i, v in enumerate(haystack[offset:]):
        if any(needle in v for needle in needles):
            return i + offset

def find_first_not_matching( needles, haystack, offset = 0):
    for i, v in enumerate(haystack[offset:]):
        if not any(needle in v for needle in needles):
            return i + offset


def licencify_list(lines, block):
    fcontent = ''.join(lines)
    replace_old_licence = licence['begin'] in fcontent

    extra = []

    if replace_old_licence:
        id_begin = find_first_matching( [licence['begin']], lines )
        id_end   = find_first_matching( [licence['end']  ], lines , id_begin )
        id_end  += 1
        print "updating block"
    else:
        id_begin = find_first_not_matching ( ignore_lines, lines )
        id_end = id_begin
        extra = [sep]
        print "adding block"
    
    lines[id_begin:id_end] = block + extra
    return lines


def licencify_file(file, content):
    basename, ext = os.path.splitext(file)
    print 'reading', file, '...'
    f = open(file)
    lines = f.readlines()
    f.close()

    block = get_licence_block(ext, content)
    licencify_list(lines, block)

    print 'writing', file, '...'
    f = open(file, "w")
    f.writelines(lines)
    f.close()


def licencify_dirs(dirs, content):
    for dir in dirs:
        if not os.path.isdir(dir):
            print "warning : ", dir, "is not a dir"
            continue
        for root, dirs, files in os.walk(dir):
            for file in files:
                basename, ext = os.path.splitext(file)
                if ext in comments:
                    licencify_file(os.path.join(root,file), content)



def main():
    import sys
    licencify_dirs(sys.argv[1:], licence['LGPL'])

if __name__ == "__main__":
    main()


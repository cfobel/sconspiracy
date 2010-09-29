# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2010.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


ALLOWED_COMMANDLINE_OPTIONS = [
        'ARCH'             ,
        'DEBUG'            ,
        'LOGLEVEL'         ,
        'CONFIG'           ,
        'BUILD'            ,
        'BUILDDEPS'        ,
        'BUILDPKG'         ,
        'RACY_DEBUG'       ,
        'USEVISIBILITY'    ,
        'CXX'              ,

        'RACY_DBFILE'      ,
        'RACY_BUILD_DIR'   ,
        'RACY_INSTALL_DIR' ,
        'RACY_BINPKGS_DIR' ,
        'RACY_CODE_DIRS'   ,
        'OPTIMIZATIONLEVEL',
        'WARNINGSASERRORS' ,

        ]

ALLOWED_COMMANDLINE_PRJ_OPTIONS = [
        'JOBS_LIMIT'      ,
        'LOGLEVEL'        ,
        'BUILD'           ,
        'BUILDDEPS'       ,
        'BUILDPKG'        ,
        'USEVISIBILITY'   ,
        'WARNINGSASERRORS',
        ]

COMMANDLINE_OPTIONS_DESC = {
        'ARCH'              : 'Architecture destination'                            ,
        'DEBUG'             : 'Debug mode'                                          ,
        'RACY_DEBUG'        : 'Switch SConspiracy to debug mode'                    ,
        'JOBS_LIMIT'        : ('For the specified project, limit the number of'
                               'simultaneously compiled files'),
        'LOGLEVEL'          : 'Log level'                                           ,
        'OPTIMIZATIONLEVEL' : 'Optimization level'                                  ,
        'WARNINGSASERRORS'  : 'Treat compilation warning as errors '                ,
        'CONFIG'            : 'Select the config to use'                            ,

        'BUILD'             : ('If "no", nothing will be compiled. Usefull for '
                               'Doxygen generation without having to build project '
                               'for ex.')                                           ,

        'BUILDDEPS'         : 'if yes build target\'s dependencies'                 ,
        'BUILDPKG'          : 'if yes generate target\'s binary packages'           ,
        'CXX'               : 'Select c++ compiler executable'                      ,

        'USEVISIBILITY'     : 'Switch visibility mode'                       ,

        'RACY_DBFILE'       : 'Scons\'s signatures file'                     ,
        'RACY_BUILD_DIR'    : 'Build dir path'                               ,
        'RACY_INSTALL_DIR'  : 'Install dir path'                             ,
        'RACY_BINPKGS_DIR'  : 'Binaries packages path'                       ,
        'RACY_CODE_DIRS'    : 'List of path containing SConspiracy projects' ,

        }



def check_opts(opts):
    forbiden = [ opt for opt in opts 
            if opt not in ALLOWED_COMMANDLINE_OPTIONS]

    if forbiden:
        import racy
        msg = '{opts} option(s) not allowed in commandline arguments'
        raise racy.RacyCommandLineError, msg.format(opts = forbiden)


def check_prj_opts(opts):
    forbiden = [ opt for opt in opts 
            if opt not in ALLOWED_COMMANDLINE_PRJ_OPTIONS]

    if forbiden:
        import racy
        msg = "{opts} option(s) not allowed in commandline project's arguments"
        raise racy.RacyCommandLineError, msg.format(opts = forbiden)



class Undef(object): pass
Undef = Undef()

def get_opt_help(opt, desc, def_val, allowed_val=Undef, current_val=Undef):
    help = """{opt}: {desc}
        default : {default}"""
    if current_val is not Undef:
        help += """
        current : {allowed} """.format(allowed = str(current_val))
    if allowed_val is not Undef:
        help += """
        allowed values : {allowed} """.format(allowed = str(allowed_val))

    help = help.format(opt=opt, desc=desc, default=str(def_val))
    return help

def get_opts_help():
    import default
    import allowedvalues
    import racy.renv.options as opts
    help = []
    def get_help_for(L, for_prj_opts=False):
        for opt in sorted(L):
            desc = COMMANDLINE_OPTIONS_DESC[opt]
            opt_def = getattr(default, opt, Undef)
            if opt_def is Undef:
                import racy
                msg = '"{0}" has no default value'
                raise racy.OptionError, msg.format(opt)
            allowed = getattr(allowedvalues, opt, Undef)
            current = opts.get_option(opt)
            help.append(get_opt_help(opt, desc, opt_def, allowed, current))

    help.append('= Global options '      + '='*67 )
    get_help_for(ALLOWED_COMMANDLINE_OPTIONS)
    help.append('= By projects options ' + '='*57 )
    get_help_for(ALLOWED_COMMANDLINE_PRJ_OPTIONS, for_prj_opts = True)
    help.append('='*79)
    
    return help




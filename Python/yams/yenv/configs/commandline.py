# -*- coding: UTF8 -*-
# ***** BEGIN LICENSE BLOCK *****
# Sconspiracy - Copyright (C) IRCAD, 2004-2009.
# Distributed under the terms of the BSD Licence as
# published by the Open Source Initiative.  
# ****** END LICENSE BLOCK ******


ALLOWED_COMMANDLINE_OPTIONS = [
        'ARCH'            ,
        'DEBUG'           ,
        'LOGLEVEL'        ,
        'CONFIG'          ,
        'BUILD'           ,
        'BUILDDEPS'       ,
        'BUILDPKG'        ,
        'YAMS_DEBUG'      ,
        'USEVISIBILITY'   ,
        'CXX'             ,

        'YAMS_BUILD_DIR'  ,
        'YAMS_INSTALL_DIR',
        'YAMS_LIBEXT_DIR' ,
        'YAMS_CODE_DIRS'  ,

        ]

ALLOWED_COMMANDLINE_PRJ_OPTIONS = [
        'LOGLEVEL'     ,
        'BUILD'        ,
        'BUILDDEPS'    ,
        'BUILDPKG'     ,
        'USEVISIBILITY',
        ]

COMMANDLINE_OPTIONS_DESC = {
        'ARCH'      : 'Architecture destination'                            ,
        'DEBUG'     : 'Debug mode'                                          ,
        'YAMS_DEBUG': 'Switch yams to debug mode'                           ,
        'LOGLEVEL'  : 'Log level'                                           ,
        'CONFIG'    : 'Select the config to use'                            ,
        'BUILD'     : ('If "no", nothing will be compiled. Usefull for '
                       'Doxygen generation without having to build project '
                       'for ex.')                                           ,
        'BUILDDEPS' : 'if yes build target\'s dependencies'                 ,
        'BUILDPKG'  : 'if yes generate target\'s binary packages'           ,
        'CXX'       : 'Select c++ compiler executable'                      ,

        'USEVISIBILITY'    : 'Switch visibility mode'                       ,

        'YAMS_BUILD_DIR'   : 'Build dir path'                               ,
        'YAMS_INSTALL_DIR' : 'Install dir path'                             ,
        'YAMS_LIBEXT_DIR'  : 'External libraries path'                      ,
        'YAMS_CODE_DIRS'   : 'List of path containing yams projects'        ,

        }



def check_opts(opts):
    forbiden = [ opt for opt in opts 
            if opt not in ALLOWED_COMMANDLINE_OPTIONS]

    if forbiden:
        import yams
        msg = "{opts} option(s) not allowed in commandline arguments"
        raise yams.YamsCommandLineError, msg.format(opts = forbiden)


def check_prj_opts(opts):
    forbiden = [ opt for opt in opts 
            if opt not in ALLOWED_COMMANDLINE_PRJ_OPTIONS]

    if forbiden:
        import yams
        msg = "{opts} option(s) not allowed in commandline project's arguments"
        raise yams.YamsCommandLineError, msg.format(opts = forbiden)



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
    import yams.yenv.options as opts
    help = []
    def get_help_for(L, for_prj_opts=False):
        for opt in sorted(L):
            desc = COMMANDLINE_OPTIONS_DESC[opt]
            opt_def = getattr(default, opt, Undef)
            if opt_def is Undef:
                import yams
                raise yams.OptionError, '"{0}" has no default value'
            allowed = getattr(allowedvalues, opt, Undef)
            current = opts.get_option(opt)
            help.append(get_opt_help(opt, desc, opt_def, allowed, current))

    help.append("= Global options ==============================================================")
    get_help_for(ALLOWED_COMMANDLINE_OPTIONS)
    help.append("= By projects options =========================================================")
    get_help_for(ALLOWED_COMMANDLINE_PRJ_OPTIONS, True)
    help.append("===============================================================================")
    
    return help


#def ...()
#
#    opt_def = getattr(default, opt)

    




# DISTCC/CCACHE/SCONSCACHE



#def FormatVariableHelpText(self, env, key, help, default, actual, aliases=[]):
#    # Don't display the key name itself as an alias.
#    format = '\n%s: %s\n'
#    aliases = filter(lambda a, k=key: a != k, aliases)
#    if len(aliases)==0:
#        return self.format % (key, help, default, actual)
#    else:
#        return self.format_ % (key, help, default, actual, aliases)





#AddOption ( "DEBUG", help = "Debug mode", allowed_values=('full', 'release') )


#--------------------------------------------------

#USEVISIBILITY
#DISTRIB -> config
#CONSOLE

#DEF           
#INC           
#STDLIBPATH    
#STDLIB        
#LIBPATH       
#NOLIB         
#USE           


#ALLOW_USER_OPTIONS
#OVERRIDE_PROJECT_VALUE


#CXX           = ''

# CXX
# #CPPFLAGS
# #LINKFLAGS
# #PACK??
# #RESRC?
# DSP
# USEGCH
# USESTDAFX
# OPTIMIZATIONLEVEL


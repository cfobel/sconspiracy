
import os
import os.path
import sys



def main():

    # racy tricks
    racy_bin = sys.argv[0]
    racy_bin_dir = os.path.split(racy_bin)[0]
    racy_root_dir = os.path.split(racy_bin_dir)[0]
    racy_config_dir = os.path.join(racy_root_dir,'Config')
    racy_python_dir = os.path.join(racy_root_dir,'Python')

    #racy scons dir
    racy_scons_dir = os.path.join(racy_python_dir, 'SCons')
    
    #insert racy dir in python path
    sys.path.insert(0, racy_python_dir)
    import racy
    
    #Check scons installation
    if os.path.isdir(racy_scons_dir):
        try:
            import SCons.Script
        except:
            racy.print_msg("Bad install of scons in {0}"
                        .format(racy_scons_dir))
            exit()
    else:
        racy.print_msg("Please install scons in {0}"
                           .format(racy_python_dir))



    #Possibility of define some variables in ~/.Racy
    config_dir = os.environ.get('RACY_CONFIG_DIR',
                                os.path.expanduser('~/.Racy'))
    os.environ['RACY_CONFIG_DIR'] = (config_dir 
            if os.path.isdir(config_dir) else racy_config_dir)


    racy_module_path = os.path.dirname(racy.__file__)
    racy_rc_path     = os.path.join(racy_module_path, 'rc')
    sconstruct_file  = os.path.join(racy_rc_path,'SConstruct')
    sys.argv.insert(1,sconstruct_file)
    sys.argv.insert(1,'-f')
    sys.argv[:] = racy.clean_args(sys.argv)
    # this does all the work, and calls sys.exit
    # with the proper exit status when done.
    SCons.Script.main()




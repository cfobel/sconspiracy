MACRO(SYMLINK src dest working_dir)

FILE(MAKE_DIRECTORY ${working_dir})
IF(WIN32)
    FIND_PROGRAM(link_present linkd.exe)
    EXECUTE_PROCESS(COMMAND linkd.exe /D  ${dest} ${src}
                        WORKING_DIRECTORY ${working_dir}
                        OUTPUT_QUIET
                        ERROR_QUIET
                       )

    IF(link_present)
        
    ELSE(link_present)
        MESSAGE(ERROR "No tools to create symlink in the path")
    ENDIF(link_present)

ELSE(WIN32)
    FIND_PROGRAM(link_present ln)
    IF(link_present)
        EXECUTE_PROCESS(COMMAND ln -sn ${src} ${dest}
                        WORKING_DIRECTORY ${working_dir}
                        OUTPUT_QUIET
                        ERROR_QUIET
                       )
    ELSE(link_present)
        MESSAGE(ERROR "ld not present")
    ENDIF(link_present)
ENDIF(WIN32)



ENDMACRO(SYMLINK)


MACRO(LIST_COPY list_files destination)
    FOREACH(elem ${list_files})
        FILE(COPY ${elem}
             DESTINATION ${destination}
           )
    ENDFOREACH(elem)
ENDMACRO(LIST_COPY)

MACRO(ADD_SUBDIRECTORIES list_directories)
    FOREACH(elem ${list_directories} )
        ADD_SUBDIRECTORY(${elem})
    ENDFOREACH(elem)
ENDMACRO(ADD_SUBDIRECTORIES)

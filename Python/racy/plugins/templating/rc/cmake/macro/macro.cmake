MACRO(SYMLINK src dest working_dir)

FILE(MAKE_DIRECTORY ${working_dir})
IF(WIN32)
    FIND_PROGRAM(link_present linkd.exe)
    IF(link_present)
     EXECUTE_PROCESS(COMMAND linkd.exe  ${dest} ${src}
                        WORKING_DIRECTORY ${working_dir}
                        OUTPUT_QUIET
                        ERROR_QUIET
                       )       
    ELSE(link_present)
        MESSAGE(WARNING "No link tool found.")
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
		MESSAGE(WARNING "No link tool found.")
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


MACRO(EXTRACT_QT_HEADERS list_headers)
    MESSAGE(STATUS "Moc headers extractions")
    SET (qt_moc_headers "" PARENT_SCOPE)

    FOREACH(header ${list_headers})
        FILE(READ ${header} header_content)
        STRING(REGEX MATCH "Q_OBJECT" matched "${header_content}")

        IF(NOT ${matched} STREQUAL "")
            LIST(APPEND qt_moc_headers ${header})
        ENDIF(NOT ${matched} STREQUAL "")

    ENDFOREACH(header)
ENDMACRO(EXTRACT_QT_HEADERS)

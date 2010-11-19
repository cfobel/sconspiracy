/* ***** BEGIN LICENSE BLOCK *****
* FW4SPL - Copyright (C) IRCAD, 2009-2010.
* Distributed under the terms of the GNU Lesser General Public License (LGPL) as
* published by the Free Software Foundation.
* ****** END LICENSE BLOCK ****** */
<% NAME = PRJ_NAME.upper() %> 

#ifndef _${NAME}_CONFIG_HPP_
#define _${NAME}_CONFIG_HPP_

    #ifdef _WIN32

        #ifdef ${NAME}_EXPORTS
            #define ${NAME}_API __declspec(dllexport)
        #else
            #define ${NAME}_API __declspec(dllimport)
        #endif

        #define ${NAME}_CLASS_API

        #pragma warning(disable: 4290)

    #elif defined(__GNUC__) && (__GNUC__>=4) && defined(__USE_DYLIB_VISIBILITY__)

        #ifdef ${NAME}_EXPORTS
            #define ${NAME}_API __attribute__ ((visibility("default")))
            #define ${NAME}_CLASS_API __attribute__ ((visibility("default")))
        #else
            #define ${NAME}_API __attribute__ ((visibility("hidden")))
            #define ${NAME}_CLASS_API __attribute__ ((visibility("hidden")))
        #endif

    #else

        #define ${NAME}_API
        #define ${NAME}_CLASS_API

    #endif

#endif //${NAME}_API


/* ***** BEGIN LICENSE BLOCK *****
 * FW4SPL - Copyright (C) IRCAD, 2009-2010.
 * Distributed under the terms of the GNU Lesser General Public License (LGPL) as
 * published by the Free Software Foundation.
 * ****** END LICENSE BLOCK ****** */

<% NAME = PRJ_NAME.upper() %> 
#ifndef _${NAME}_PLUGIN_HPP_
#define _${NAME}_PLUGIN_HPP_


#include <fwRuntime/Plugin.hpp>


namespace ${PRJ_NAME}
{
/**
* @brief   This class is started when the bundles is loaded.
* @class   Plugin.
* @author  IRCAD (Research and Development Team).
* @date    2010.
*/

struct Plugin : public ::fwRuntime::Plugin
{

    /**
     * @brief   destructor
     */
    ~Plugin() throw();

    // Overrides
    void start() throw(::fwRuntime::RuntimeException);

    // Overrides
    void stop() throw();

};


} // namespace ${PRJ_NAME}


#endif //_${NAME}_PLUGIN_HPP_

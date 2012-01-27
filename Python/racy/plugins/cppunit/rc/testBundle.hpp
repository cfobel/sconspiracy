/* ***** BEGIN LICENSE BLOCK *****
 * Sconspiracy - Copyright (C) IRCAD, 2004-2010.
 * Distributed under the terms of the BSD Licence as
 * published by the Open Source Initiative.  
 * ****** END LICENSE BLOCK ****** */

#ifndef __CPPUNIT_RC_TESTBUNDLE_HPP__
#define __CPPUNIT_RC_TESTBUNDLE_HPP__


#include <boost/filesystem/operations.hpp>
#include <boost/filesystem/path.hpp>

#include <fwRuntime/operations.hpp>
#include <fwRuntime/profile/Profile.hpp>
#include <fwRuntime/io/ProfileReader.hpp>


class MiniLauncher
{
public:
    MiniLauncher( ::boost::filesystem::path profilePath );
    ~MiniLauncher();

private:
    ::fwRuntime::profile::Profile::sptr m_profile;

};


#define CPPUNIT_INIT_BUNDLES_TESTS MiniLauncher miniLaucher( "share/"  PRJ_NAME "_" CPPUNIT_TEST_VERSION "/profile.xml" )

#endif /* end of include guard: __CPPUNIT_RC_TESTBUNDLE_HPP__ */

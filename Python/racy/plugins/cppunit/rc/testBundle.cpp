/* ***** BEGIN LICENSE BLOCK *****
 * Sconspiracy - Copyright (C) IRCAD, 2004-2010.
 * Distributed under the terms of the BSD Licence as
 * published by the Open Source Initiative.  
 * ****** END LICENSE BLOCK ****** */

MiniLauncher::MiniLauncher( ::boost::filesystem::path profilePath )
{
    ::boost::filesystem::path cwd = ::boost::filesystem::current_path();
    ::boost::filesystem::path bundlePath = cwd / "Bundles";

    ::fwRuntime::addBundles(bundlePath);

    if (!::boost::filesystem::exists( profilePath ))
    {
        profilePath = cwd / profilePath;
    }

    if (!::boost::filesystem::exists( profilePath ))
    {
        throw (std::invalid_argument("<" + profilePath.string() + "> not found." ));
    }


    m_profile = ::fwRuntime::io::ProfileReader::createProfile(profilePath);
    ::fwRuntime::profile::setCurrentProfile(m_profile);

    m_profile->setParams(0, NULL);
    m_profile->start();
    // m_profile->run();

}

MiniLauncher::~MiniLauncher()
{
    m_profile->stop();
    m_profile.reset();
    ::fwRuntime::profile::setCurrentProfile(m_profile);
}


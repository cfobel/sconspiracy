.. raw:: latex

   \newcommand{\beamerENV}[2] { \begin{#1} #2 \end{#1} }

   \newcommand{\docutilsroledefinition}{\beamerENV{definition}}
   \newcommand{\docutilsroleexample}{\beamerENV{example}}
   \newcommand{\docutilsroleproof}{\beamerENV{proof}}
   \newcommand{\docutilsroletheorem}{\beamerENV{theorem}}

   \newcommand{\docutilsrolequotation}{\beamerENV{quotation}}
   \newcommand{\docutilsrolequote}{\beamerENV{quote}}
   \newcommand{\docutilsrolesemiverbatim}{\beamerENV{semiverbatim}}
   \newcommand{\docutilsroleverse}{\beamerENV{verse}}

   \newcommand{\docutilsrolecommand}[1]{ \begin{exampleblock}{Command} \$> #1 \end{exampleblock} }

.. role:: definition
.. role:: example
.. role:: proof
.. role:: theorem

.. role:: quotation
.. role:: quote
.. role:: semiverbatim
.. role:: verse

.. role:: command


.. role:: path(strong)




=========
Yams (++)
=========







What's new
----------

What makes yams better
~~~~~~~~~~~~~~~~~~~~~~

Backend
=======

- Python 2.6 and SCons 1.2
- More 'pythonic' and 'SCons-friendly' architecture
- yams is now a python module


Features
========

- Automatic projects and dependencies lookup
- Option checking system ( bad values, bad required project version, deprecated options)
- New libext management system
- Bundles can be free of code
- Configuration system (yams-level, user-level, project-level)
- Plugin system
- Cppunit and doxygen plugins
- Better compilators management
- C++ exports yams-managed


Frontend
========

- Flexible commandline
- New 'yams' command


Installation
------------

Yams Installation
~~~~~~~~~~~~~~~~~

Getting Yams
============

:command:`svn co http://dev-srv:8080/svn/Config/branches/yams_0.2 <somewhere>`



Installation
============

- Add :path:`<somewhere>/Python/` to PYTHONPATH
- Add :path:`<somewhere>/bin/` to PATH
- Copy :path:`<somewhere>/Config/user.options-dist` to user.options in your yams 
  config dir (it can be in :path:`<somewhere>/Config`)
- Fill your user.options file
- Set YAMS_CONFIG_DIR environment variable to the path of your yams 
  configuration dir. Default config dir is :path:`~/.Yams`








Usage
-----

Yams Usage
~~~~~~~~~~

Building a project
==================

:command:`yams fwData`

- Lookup for fwData
- Lookup for fwData dependencies (fwTools, fwCore)
- build and install fwData and each dependencies


Building a project
==================

:command:`yams fwData/LOGLEVEL:trace`

- set 'LOGLEVEL' option to 'trace' for fwData
- leave 'LOGLEVEL' to default for each other dependencies 
- build and install fwData and each dependencies


Building a project
==================

:command:`yams fwData/LOGLEVEL:trace fwCore/LOGLEVEL:debug`

- Multiple targets
- set 'LOGLEVEL' option to 'trace' for fwData
- set 'LOGLEVEL' option to 'debug' for fwCore
- leave 'LOGLEVEL' to default for each other dependencies 
- build and install fwData, fwCore and each dependencies


Building a project
==================

:command:`yams fwData LOGLEVEL=fatal`

- Set 'LOGLEVEL' option to 'fatal' for fwData and each dependencies
- Build and install fwData


Building a project
==================

:command:`yams fwData/LOGLEVEL:trace LOGLEVEL=warning`

- Will set 'LOGLEVEL' option to 'trace' for project fwData, and to 'warning'
  for each other dependencies and build and install project
- LOGLEVEL:trace is a 'by project' option
- LOGLEVEL=warning is a 'global' option


Special commands
================

- Passing several options to a project : :command:`yams fwData/LOGLEVEL:warning/CPPUNIT:yes`

- Clean fwData and dependencies : :command:`yams fwData -c`

- Display yams help about global and by project commandline options : :command:`yams -h`








Options
-------

Yams options
~~~~~~~~~~~~

Options
=======
- Yams use several level of options to build projects
- Yams options priority (lowest to highest) :

  - Yams default options
  - User options
  - Project options
  - User by project options
  - Commandline options
  - Commandline by project options



Yams options files
~~~~~~~~~~~~~~~~~~


Option file
===========

|begintblock| user.options |endtitletblock|

- Set user's global options

  - DEBUG, LOGLEVEL, CONFIG, USEVISIBILITY, YAMS_*_DIR[S], ...

- Is a python script : any python module is usable
- An example is available in :path:`<somewhere>/Config`

|endtblock|


Option file
===========

|begintblock| build.options |endtitletblock|

- This file is in :path:`prj_path/bin` dir
- Set project options, is compatible with the previous yams version
- Is a python script : any python module is usable
- An example is available in :path:`<somewhere>/Config`

|endtblock|

Option file
===========

|begintblock| user.prj.options |endtitletblock|

- Set user's by project options

  - DEBUG, LOGLEVEL, CONFIG, DOX, CPPUNIT, ...

- Is a python script : any python module is usable
- An example is available in :path:`<somewhere>/Config`

|endtblock|







Variants
--------


Yams configuration variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurations
==============

- A configuration is particular a set of options
- A configuration is a python script
- There are several kind of 'configs' :

  - Yams internal defined configs
  - User configs
  - By project configs



Yams internal defined configs
=============================

- Override yams default options
- Should not be modified

User configs
============

- Overrides user options
- Have the same properties than user.options file
- Are available in :path:`<somewhere>/Config/configs`
- Are selected with CONFIG global option

By project configs
==================

- Overrides project's build.options file
- Have the same properties than build.options file
- Are available in :path:`prj_path/bin/configs`
- Are selected with "@config" special attribute global option or automatically
  choosed in project's configurations following global's CONFIG option if the
  requested config is available
- Example : :command:`yams fwData/@crypto`




.. |begindefinition| raw:: latex

   \begin{definition}

.. |enddefinition| raw:: latex

   \end{definition}



.. |beginexample| raw:: latex

   \begin{example}

.. |endexample| raw:: latex

   \end{example}



.. |beginproof| raw:: latex

   \begin{proof}

.. |endproof| raw:: latex

   \end{proof}



.. |begintheorem| raw:: latex

   \begin{theorem}

.. |endtheorem| raw:: latex

   \end{theorem}



.. |beginquotation| raw:: latex

   \begin{quotation}

.. |endquotation| raw:: latex

   \end{quotation}



.. |beginquote| raw:: latex

   \begin{quote}

.. |endquote| raw:: latex

   \end{quote}



.. |beginsemiverbatim| raw:: latex

   \begin{semiverbatim}

.. |endsemiverbatim| raw:: latex

   \end{semiverbatim}



.. |beginverse| raw:: latex

   \begin{verse}

.. |endverse| raw:: latex

   \end{verse}



.. |beginblock| raw:: latex

   \begin{block}{}

.. |endblock| raw:: latex

   \end{block}


.. |begintblock| raw:: latex

   \begin{block}{

.. |endtitletblock| raw:: latex

   }

.. |endtblock| raw:: latex

   \end{block}



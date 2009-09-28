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




===========
SConspiracy
===========







What's new
----------

What makes SConspiracy better
~~~~~~~~~~~~~~~~~~~~~~

Backend
=======

- Python 2.6 and SCons 1.2
- More 'pythonic' and 'SCons-friendly' architecture
- SConspiracy is now a python module


Features
========

- Automatic projects and dependencies lookup
- Option checking system ( bad values, bad required project version, deprecated options)
- New libext management system
- Bundles can be free of code
- Configuration system (SConspiracy-level, user-level, project-level)
- Plugin system
- Cppunit and doxygen plugins
- Better compilators management
- C++ exports SConspiracy-managed


Frontend
========

- Flexible commandline
- New 'racy' command


Installation
------------

SConspiracy Installation
~~~~~~~~~~~~~~~~~~~~~~~~

Getting SConspiracy
===================

:command:`hg clone https://sconspiracy.googlecode.com/hg/ <somewhere>`


Installation
============

- Add :path:`<somewhere>/bin/` to PATH
- Copy :path:`<somewhere>/Config/user.options-dist` to :path:`<somewhere>/Config/user.options`
- Fill your user.options file








Usage
-----

SConspiracy Usage
~~~~~~~~~~~~~~~~~

Building a project
==================

:command:`racy fwData`

- Lookup for fwData
- Lookup for fwData dependencies (fwTools, fwCore)
- build and install fwData and each dependencies


Building a project
==================

:command:`racy fwData/LOGLEVEL:trace`

- set 'LOGLEVEL' option to 'trace' for fwData
- leave 'LOGLEVEL' to default for each other dependencies 
- build and install fwData and each dependencies


Building a project
==================

:command:`racy fwData/LOGLEVEL:trace fwCore/LOGLEVEL:debug`

- Multiple targets
- set 'LOGLEVEL' option to 'trace' for fwData
- set 'LOGLEVEL' option to 'debug' for fwCore
- leave 'LOGLEVEL' to default for each other dependencies 
- build and install fwData, fwCore and each dependencies


Building a project
==================

:command:`racy fwData LOGLEVEL=fatal`

- Set 'LOGLEVEL' option to 'fatal' for fwData and each dependencies
- Build and install fwData


Building a project
==================

:command:`racy fwData/LOGLEVEL:trace LOGLEVEL=warning`

- Will set 'LOGLEVEL' option to 'trace' for project fwData, and to 'warning'
  for each other dependencies and build and install project
- LOGLEVEL:trace is a 'by project' option
- LOGLEVEL=warning is a 'global' option


Special commands
================

- Passing several options to a project : :command:`racy fwData/LOGLEVEL:warning/CPPUNIT:yes`

- Clean fwData and dependencies : :command:`racy fwData -c`

- Display racy help about global and by project commandline options : :command:`racy -h`








Options
-------

SConspiracy options
~~~~~~~~~~~~~~~~~~~

Options
=======
- SConspiracy use several level of options to build projects
- SConspiracy options priority (lowest to highest) :

  - SConspiracy default options
  - User options
  - Project options
  - User by project options
  - Commandline options
  - Commandline by project options



SConspiracy options files
~~~~~~~~~~~~~~~~~~~~~~~~~


Option file
===========

|begintblock| user.options |endtitletblock|

- Set user's global options

  - DEBUG, LOGLEVEL, CONFIG, USEVISIBILITY, RACY_*_DIR[S], ...

- Is a python script : any python module is usable
- An example is available in :path:`<somewhere>/Config`

|endtblock|


Option file
===========

|begintblock| build.options |endtitletblock|

- This file is in :path:`prj_path/bin` dir
- Set project options, is compatible with the previous version of SConspiracy
  (called yams)
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


SConspiracy configuration variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configurations
==============

- A configuration is particular a set of options
- A configuration is a python script
- There are several kind of 'configs' :

  - SConspiracy internal defined configs
  - User configs
  - By project configs



SConspiracy internal defined configs
====================================

- Override SConspiracy default options
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
- Example : :command:`racy fwData/@crypto`




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



===========
upersetter
===========
upersetter helps with automating basic setup tasks for any kind of project in a general way.
It provides the ability to describe a project in yaml format and create files and folders based on that.

upersetter uses a full-featured templating engine (jinja2) in order to allow custom variables to be used when creating a new project.
It also features an interactive mode to allow guided project creation for end-users.


Getting Started
===============

Installation
------------
To install simply do::

    python setup.py install

As soon as it gets its first release upersetter will be available on pypi

Dependencies
^^^^^^^^^^^^
upersetter has the ability to fetch content from remote sources. This is done via `AnyPath <http://github...>`_
Anypath and has the same dependencies as Anypath does for the different protocols.

(upersetter depends on AnyPath but AnyPath does not install any dependencies for the different protocols by default)


Basic Usage
-----------
Describing your project can be done either in the form of yaml files or in code as dictionaries.

In the most basic case you describe the structure of your project in a file called *structure.yaml*::

   topfolder:
     files:
       - afile:
           content: somecontent
     subfolder:
       subsubfolder:
         files:
           - anotherfile:
               content: abc

You then execute the following command::

   python -m upersetter setup folder path/to/your/structure.yaml

The project will then be created in your current working directory.

In the above example upersetter will create a folder with the name *topfolder*.
Underneath that a file with the name *afile* and the content *somecontent*, as well as a folder with the name *subfolder* will be created. *subfolder* again has a subfolder *subsubfolder* which contains the file *anotherfile* with the content *abc*

Doing more useful stuff
-----------------------
...


Options and templates
^^^^^^^^^^^^^^^^^^^^^

Interactive usage
^^^^^^^^^^^^^^^^^

Contributing
============
You can contribute in any of the following areas, no matter if it is your first OSS contribution or your thousandths.
Contributions are welcome for example:
- If you find any issue or bug when using upersetter
- If you want to add to the documentation or fix incorrect or missing documentation.
- If you want to add features or work on the codebase in general

Just file an issue in the tracker first describing what you would like to do and then create a pull-request.

License
-------
upersetter is licensed under "Mozilla Public License Version 2.0". See LICENSE.txt for the full license.
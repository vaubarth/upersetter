===========
upersetter
===========
upersetter helps with automating basic setup tasks for any kind of project in a general way.
It provides the ability to describe a project in yaml format and create files and folders based on that.

upersetter uses a full-featured templating engine (jinja2) in order to allow custom variables to be used when creating a new project.
It also features an interactive mode to allow guided project creation for end-users.

Learn more about why this project exists and how it is different to e.g. cookiecutter in the section `Why another bootstrapping tool`_.
If you are interested in learning more there are `examples <https://github.com/vaubarth/upersetter/tree/master/examples>`_. which illustrate some usecases.


- `Installation`_

  -  `Dependencies`_

- `Basic Usage`_
- `Advanced usage`_

  - `Structure syntax`_

    - `File creation - The files directive`_
    - `Fetching remote resources - The remote directive`_
    - `Executing external scripts - The scripts directive`_

  - `Templates within structure files`_

  - `The options file - using templates`_
  - `Interactive usage`_

- `Why another bootstrapping tool`_
- `Contributing`_
- `License`_


Installation
============
To install simply do::

    python setup.py install

As soon as it gets its first release upersetter will be available on pypi

Dependencies
------------
upersetter has the ability to fetch content from remote sources. This is done via `AnyPath <http://github.com/vaubarth/anypath>`_
Anypath and has the same dependencies as Anypath does for the different protocols.

(upersetter depends on AnyPath but AnyPath does not install any dependencies for the different protocols by default)


Basic Usage
===========
Describing your project can be done either in the form of yaml files or in code as dictionaries.

In the most basic case you describe the structure of your project in a file called *structure.yaml*::

    topfolder:
        :files:
            - afile:
                content: somecontent
        subfolder:
            subsubfolder:
                :files:
                    - anotherfile:
                        content: {{anotherfile.content}}

`{{anotherfile.content}}` is a template expression which can be resolved by specifying the variable antotherfile.content in a *options.yaml* file::

    anotherfile:
        content: Some content for the file

The template expression can also be resolved by interactive usage of upersetter where you can specify the variable on the commandline (see `Interactive Usage`_)

Given you the files :code:`structure.yaml` and :code:`options.yaml` are in a folder called /user/example you can execute the following::

    python -m upersetter setup folder /user/example

The project will then be created in your current working directory.

In the above example upersetter will create a folder with the name *topfolder*.
Underneath that a file with the name *afile* and the content *somecontent*, as well as a folder with the name *subfolder* will be created.
*subfolder* again has a subfolder *subsubfolder* which contains the file *anotherfile* with the content *Some content for the file* which is specified in the options.yaml file.

However upersetter provides much more dynamic ways to create a project from templates, the commandline or even remote resources.

Advanced usage
==============
Full featured examples can be found in the  examples_ folder which shows usages of all features available.

Structure syntax
----------------
A structure file primarily contains two kinds of elements: folders and files

In general the structure file resembles a directory tree, however there is some special syntax to denote how files and folders should be created or filled with content.

In general a structure file looks like this::

    <name of folder>:
        <name of subfolder>:
            :files:
                - <name of file>:
                    <creation of file: content/template>
        :files:
            - <name of file>:
                <creation of file: content/template>
        <name of second subfolder>:
            :<some_directive>:
                ...

Folders are a dictionary keys in the yaml file. Folders can have files and other folders as sub-entries::

    topfolder:
        subfolder:
            ...
    another topfolder:
        ...


Files and folders can be created in three different ways - called directives. The following directives are available:

- :code:`:files:`
- :code:`:remote:`
- :code:`:script:`

File creation - The files directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The files directive creates files either from a template or directly from given content strings.
It is indicated with :code:`:files:`

After that a list of key value pairs representing the filename as the key and the way how to create the file as the value describes the files::


    :files:
        - somefile.txt:
            <creation of file: content/template>

Files can be created in the following ways:

**content**
:code:`content` is the simplest way to create a file. The content of the file is directly specified in the structure file::


    :files:
        - somefile.txt:
            content: This is the content of the file.

**template**
:code:`template` takes the content to be used in a file from a template which is interpreted with the options from the options file::


    :files:
        - somefile.txt:
            template: /path/to/the/template.txt

The template name doesn't need to match the name of the file to be created. The template gets rendered with the options as variables and then written to the specified filepath.
A full explanation of template-rendering and the options file is given below: `Options and templates`_


Fetching remote resources - The remote directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The remote directive takes a file or folders from a remote location and copies it in the specified directory.
It is indicated with :code:`:remote:`

:code:`remote` is always placed directly underneath a folder::

    topfolder:
        subfolder:
            :remote: 'ssh://user@host:/home/user'

In this example the folder *subfolder* will have the contents of the remote folder after upersetter is executed. If the remote is only a file, only that will be copied to the local directory, else the whole directory tree will be copied.
The remote handling is done by `AnyPath <http://github.com/vaubarth/anypath>`_ - see there to check out supported protocols from where to fetch remote resources.


Executing external scripts - The scripts directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The script directive executes a given script in the given directory.
It is indicated with :code:`:script:`

The script itself follows the file directive and can either be created via a template or directly from a string::

    topfolder:
        :script:
            from:
              - file_info.py:
                  template: file_info.py
            run:
              - python
              - file_info.py

*run* specifies the actual call of the script, it is a list which will be passed to subprocess and follows the same rules, examples::

    ['interpreter', 'script', 'arg', 'arg2']
    ['script', '-arg', 'foo']


Templates within structure files
--------------------------------
It is possible to use the full range of template syntax and interpolation within structure files.
This allows for example to dynamically specify names of files and folders, to use loops to create files and folders and much more::

    {{dynamic_name_of_topfolder}}:
        :files:
            {{dynamic_name_of_file}}

... TODO: Passing inner scope to a template ...

The options file - using templates
----------------------------------

Interactive usage
-----------------


Why another bootstrapping tool
==============================
upersetter aims to be simple and flexible. Some of the design goals do not align with other projects that solve the same need for setting up folders and files in a reproducible and easy way.
This section should explain why another approach was taken and why upersetter exists.

In the python world `cookiecutter <http://github.com/audreyr/cookiecutter>`_ is a popular project that achieves the same goal as upersetter.
It differs in a variety of ways, which makes the suitable for different kind of projects and styles of approaching the problem.
If you are not familiar with cookiecutter, check it out and give it a try, it is an amazing project which is very mature (which cannot be said for upersetter as this point)

Differences...

Contributing
============
You can contribute in any of the following areas, no matter if it is your first OSS contribution or your thousandths.
Contributions are welcome for example:
- If you find any issue or bug when using upersetter
- If you want to add to the documentation or fix incorrect or missing documentation.
- If you want to add features or work on the codebase in general

Just file an issue in the tracker first describing what you would like to do and then create a pull-request.

License
=======
upersetter is licensed under "Mozilla Public License Version 2.0". See LICENSE.txt for the full license.
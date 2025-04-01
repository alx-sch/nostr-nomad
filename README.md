1 nostr-nomad
=============

2 Introduction
==============

This tool allows users to migrate content from **Substack** to
**Nostr**.

3 Requirements
==============

To generate documentation using 'make', you need to install **Texinfo**
and **TeX**:

   - **Ubuntu/Debian**: 'sudo apt install texinfo texlive -y'

   Additionally, you will need **Python 3** (version 3.11.x) and its
dependencies.  The tool will automatically install its dependencies
within a virtual environment when you set up the project.

4 Using the tool
================

Follow these steps to set up and run the project:

4.1 Clone the repository
------------------------

     git clone XXXXX.git nostr-nomad
     cd nostr-nomad

4.2 Provide Substack export
---------------------------

Place your Substack export data ('.zip' file) into the 'export/' folder
in the project directory.  This will allow the tool to process the data
correctly.

4.3 Run the tool
----------------

Run the following command in the project's root directory:

     make

   This will: 1.  Create and activate the virtual environment (stored in
the 'env' folder).  2.  Execute the main script.  3.  Generate the
documentation: 'README.md' and place all other generated documentation
in the 'build_docs' directory.

   After running 'make', the tool will process the provided Substack
export data and generate the desired outputs automatically *(TBD what
output is)*.

4.4 Clean up
------------

To remove generated files, you can use the 'make clean' command.

   This will: 1.  Remove the virtual environment.  2.  Clean up
generated documentation.  3.  Clear cache files like Python bytecode and
other temporary data.

5 Thanks
========

Thanks for using nostr-nomad!


1 Project
*********

This is the documentation for project **nostr-nomad**.

1.1 Introduction
================

This tool allows users to migrate content from **substack.com** to
**nostr**.

1.2 Installation
================

### Requirements

   To generate documentation with 'make', you need to install
**Texinfo** and **TeX**:

   - **Ubuntu/Debian**: 'sudo apt install texinfo texlive -y'

   Additionally, you will need **Python 3** (version 3.11.x) and its
dependencies, which will be automatically installed in a virtual
environment when you set up the project.

   ### Setting up the project

   Follow these steps to set up the project:

   1.  **Clone the repository**:

     git clone XXXXX.git nostr-nomad
     cd nostr-nomad

   2.  **Provide substack export**:

   Place your substack export data ('.zip' file) into the 'export/'
folder in the project directory.  This will allow the tool to process
the data correctly.

   3.  **Run the tool**:

   ### Setting up your Git repository

   You can run the tool by simply executing the following in the
project's root directory:

     make

   This will:

   1.  Create and activate the virtual environment (stored in the 'env'
folder).  2.  Execute the main script.  3.  Generate the documentation:
'README.md' and placing all other generated documentation in the
'build_docs' directory.

   After running 'make', the tool will process the provided substack
export data and generate the desired outputs automatically (TBD what
output is).

   4.  **Clean up**:

   To remove generated files, you can use the 'make clean' command.
This will:

   1.  Remove the virtual environment.  2.  Clean up generated
documentation.  3.  Clear cache files, such as Python bytecode and other
temporary data.

1.3 Thanks
==========

Thanks for using nostr-nomad!


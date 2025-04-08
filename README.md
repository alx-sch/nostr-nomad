# nostr-nomad

This tool allows users to migrate content from **Substack** to **Nostr**.    
It’s a collaboration between **[Natalie](https://github.com/busedame)** and **[Alex](https://github.com/alx-sch)**.

## Requirements

To generate documentation using `make`, you need to install **Texinfo** and **TeX**:

   - **Ubuntu/Debian**: `sudo apt install texinfo texlive -y`

Additionally, you will need **Python 3** (version 3.11.x) and its dependencies.
When you set up the project, the tool will automatically install its dependencies within a virtual environment.

3 Using the tool
================

Follow these steps to set up and run the project:

3.1 Clone the repository
------------------------

     git clone XXXXX.git nostr-nomad
     cd nostr-nomad

3.2 Provide Substack export
---------------------------

Place your Substack export data ('.zip' file) into the 'export/' folder
in the project directory.  This will allow the tool to process the data
correctly.

3.3 Run the tool
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

3.4 Clean up
------------

To remove generated files, you can use the 'make clean' command.

   This will: 1.  Remove the virtual environment.  2.  Clean up
generated documentation.  3.  Clear cache files like Python bytecode and
other temporary data.

4 Thanks
========

Thanks for using nostr-nomad!

## Setting up a local Nostr relay for testing

This [blog post](https://manbytesgnu.org/hello-nostr-with-python.html) by [lash](https://github.com/nolash) is an excellent guide for setting up a local Nostr relay and publishing a message (or event) to it.
Before going public, you can test the `nostr-nomad` tool by publishing to your local relay.

1. **Install Rust and `cargo`**   
   The first step is to install Rust and Cargo (Rust's package manager/build tool). This is needed to compile and run the `nostr-rs-relay` project.
     
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   To make sure the `cargo` tool and `rustc` are available in your terminal, run:

    ```bash
   source $HOME/.cargo/env
   ```

   You can verify that the installation was successful by checking the versions:

   ```bash
   rustc --version
   cargo --version
   ```
   
2. **Clone the `nostr-rs-relay` Repository**
   Now, you’ll clone the `nostr-rs-relay` repository to your local machine. This repository contains the source code for the relay server.

   ```bash
   git clone https://github.com/scsibug/nostr-rs-relay.git nostr-rs-relay && cd nostr-rs-relay
   ```

3. **Build the Relay Server**
   Compile the project with the `cargo` build tool; this might take some time. 

   ```bash
   cargo build --release
   ```

4. 


   
   




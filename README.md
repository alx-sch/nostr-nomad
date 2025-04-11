# nostr-nomad

<p align="center">
    <img src="https://github.com/alx-sch/nostr-nomad/blob/main/.assets/nostr-nomad.png"  alt="nostr-nomad.png" width="500"/>
</p>

This tool allows users to migrate content from **Substack** to **Nostr** relays.    
`nostr-nomad` is a collaboration between **[Natalie](https://github.com/busedame)** and **[Alex](https://github.com/alx-sch)**.

## Requirements

To generate documentation using `make docs`, you need to install **Texinfo** and **TeX**:

   - **Ubuntu/Debian**: `sudo apt install texinfo texlive -y`

Additionally, you will need **Python 3** (version 3.7.x or higher).     
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

4. **Edit Configuration for the Local Relay**    
   In your `config.toml` file, change the following fields to set up a local Nostr relay:
   ```toml
   [network]
   address = "127.0.0.1"           # Or any other appropriate loopback IP, 127.0.0.1 is usually used as localhost.
   port = 8081                     # Use any available port; 8081 is commonly used for development/testing.
   ```

   Since this is for local testing, we will not enable WSS (secure WebSocket). This avoids the need to generate SSL/TLS certificates or configure encryption — keeping the setup simple and focused. The relay will run at: `ws://127.0.0.1:8081` or simply `ws://localhost:8081` (confirm that `localhost` points to `127.0.0.1` by running `ping localhost`).

6. **Starting the Nostr Relay**    
   Before running the relay, you need to create the database directory first (`mkdir db`). The relay will store data such as events and connections here.    
   Once the database directory is created, you can start the relay by running the following command. This will provide detailed log output:
    ```bash
   RUST_LOG=debug ./target/release/nostr-rs-relay -c config.toml -d db
   ```

   The relay should begin running, and you’ll see status updates in the terminal. This confirms that the relay is active and listening for WebSocket connections. Leave the terminal window open to keep the relay running. To interact with the relay, use `nostr-nomad` or other testing methods through a separate terminal window.
   <p align="center">
      <img src="https://github.com/alx-sch/nostr-nomad/blob/main/.assets/relay_running.png" width="800" alt="relay_running.png"/>
   </p>

7. **Checking Messages of the Local Nostr Relay**

   You can use any Nostr client that allows for the inclusion of local relays. For example:
   - [Gossip](https://github.com/mikedilger/gossip)
   - [iris](https://github.com/irislib/iris-messenger)
     
   For adding the local Nostr relay to Gossip, refer to this helpful [blog post](https://manbytesgnu.org/hello-nostr-with-python.html).

   For a quick setup of the iris client, you can use the standalone [desktop release](https://github.com/irislib/iris-messenger/releases). After installation and signing up:
   
   - Go to **Settings** -> **Network**.
   - Add `ws://localhost:8081` as a new relay.
   - Uncheck any other relays you might have subscribed to (to keep the feed focused on the local relay).
   - Check the feed (house symbol).

   If everything is set up correctly, you should now see events published to your local Nostr relay.

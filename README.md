# nostr-nomad

<p align="center">
    <img src="https://github.com/alx-sch/nostr-nomad/blob/main/.assets/nostr-nomad.png"  alt="nostr-nomad.png" width="500"/>
</p>

`nostr-nomad` migrates content from **Substack** to **Nostr** relays.    
This project is a collaboration between **[Natalie](https://github.com/busedame)** and **[Alex](https://github.com/alx-sch)**.

Supports:
- Short-form content (event `kind:1`; [NIP-1](https://nostr-nips.com/nip-01)) — such as "Tweet"-style messages (no formatting).
- **WIP:** Long-form content (event `kind:30023`; [NIP-23](https://nostr-nips.com/nip-23)) — such as blog posts (with Markdown formatting).

---

## Requirements

You need **Python 3** (version 3.7.x or higher) to compile the project.  
All Python dependencies will be automatically installed within the isolated virtual environment `env`. 

To generate documentation using `make docs`, you need to install **Texinfo** and **TeX** first:

   - **Ubuntu/Debian**: `sudo apt install texinfo texlive -y`
   - **macOS**: `brew install texinfo texlive`

---

## How to Use

1. **Clone the Repository**   
   First, clone the repository and navigate into the project directory:  
   ```
   git clone https://github.com/alx-sch/nostr-nomad nostr-nomad && nostr-nomad
   ```
2. **Provide Substack Export**   
 - Export your Substack data (check [here](https://support.substack.com/hc/en-us/articles/360037466012-How-do-I-export-my-posts)).
 - Unzip the archive and remove any posts you don’t want to migrate by deleting the corresponding `.html` files in the `posts/` folder.
 - Place the unzipped export folder into `user_input/export/`. It should contain a `posts.csv` file and a `posts/` directory with your `.html` files.
   
3. **Provide Key and Relays**   
 - Add your private key (in hex or nsec format) and the relays you'd like to publish to in the `config.toml` file in `user_input/`.
 - The private key is used **only** to sign Nostr events and is **never shared**.
 - If you prefer, you can leave the private key empty (`""`) to generate a random key at runtime.
 - ⚠️ Note: Some relays may require prior authorization and might reject events from unknown keys.
      
4. **Run `nostr-nomad`**   
   Once everything is set up, you can run the following commands:
- `make` to build and execute the tool.
- `make docs` to generate the documentation for the project.
- `make clean` to remove compiled files, the virtual environment, and documentation.
- `make clean-all` to also remove the cache (in `user_input/`). Please note that previously published posts are tracked in the cache, preventing duplicates from being sent to the same relay.

--- 

## XXXX TBD

- Short-form vs Long-form message
- not all clients support long-form message or preview of all hyperlinks (eg. while most support previewing .jpeg not all support .avif
- some relays don't seem to like 'fast publishing' --> increase delay between posts (see fct `publish_posts`).

<p align="center">
    <img src="https://github.com/alx-sch/nostr-nomad/blob/main/.assets/running_nostr-nomad.png" width="600" alt="running_nostr-nomad.png"/>
</p>

---

## Setting up a Local Nostr Relay for Testing

Before publishing to public Nostr relays, you might want to test your setup by publishing to a local relay. This allows you to familiarize yourself with how `nostr-nomad` works without impacting the broader network.
Below is a setup guide for `nostr-rs-relay`, but any other compatible relay should work as well.

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

2. **Install the Protocol Buffers Compiler**     
    The build process for `nostr-rs-relay` requires the Protocol Buffers compiler (`protoc`). You can install it on Ubuntu with:
   
   ```bash
   sudo apt install protobuf-compiler
   ```
   
   After installation, confirm that it's available by checking the version:
    ```bash
   protoc --version
   ```
   
2. **Clone the `nostr-rs-relay` Repository**    
   Now, you’ll clone the `nostr-rs-relay` repository to your local machine. This repository contains the source code for the relay server.

   ```bash
   git clone https://github.com/scsibug/nostr-rs-relay.git nostr-rs-relay && cd nostr-rs-relay
   ```

4. **Build the Relay Server**   
   Compile the project with the `cargo` build tool; this might take some time. 

   ```bash
   cargo build --release
   ```

5. **Edit Configuration for the Local Relay**     
   In your `config.toml` file, change the following fields to set up a local Nostr relay:
   ```toml
   [network]
   address = "127.0.0.1"  # Or any other appropriate loopback IP, 127.0.0.1 is usually used as localhost.
   port = 8081            # Use any available port; 8081 is commonly used for development/testing.
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

   ---

   ## Acknowledgements

   We'd like to thank [lash](https://github.com/nolash) for providing the excellent [blog post](https://manbytesgnu.org/hello-nostr-with-python.html), which helped us set up local relays and figure out how to send events to them. Lash has also been a mentor throughout this project.

# nostr-nomad

<p align="center">
    <img src="https://github.com/alx-sch/nostr-nomad/blob/main/.assets/nostr-nomad.png"  alt="nostr-nomad.png" width="500"/>
</p>

`nostr-nomad` migrates content from **Substack** to **Nostr** relays.    
This project is a collaboration between **[Natalie](https://github.com/busedame)** and **[Alex](https://github.com/alx-sch)**.

Supports:
- Short-form content (event `kind:1`; [NIP-1](https://nostr-nips.com/nip-01)) — such as "Tweet"-style messages (no formatting).
- Long-form content (event `kind:30023`; [NIP-23](https://nostr-nips.com/nip-23)) — such as blog posts (with Markdown formatting).

Features:
- Maintains a local archive of all exported post text, associated images, and publishing metadata.
- Optionally re-hosts images to move media off Substack’s CDN
    - Supported hosts: **Imgur** (anonymous uploads) and any self-hosted **HTTP file server running [WALA](https://github.com/nolash/WALA)**

---

## Requirements

All Python dependencies will be automatically installed into a virtual environment located at `env/`. 

#### System Dependencies  

You'll need **Python 3.11.x** to run the project.  

 - Check your Python version: `python3.11 --version`   
 - If the command is not found, please follow the instructions below to install it and check again:   
   - **Ubuntu/Debian**:
     ```bash
     sudo apt update
     sudo apt install software-properties-common -y
     sudo add-apt-repository ppa:deadsnakes/ppa -y
     sudo apt update
     sudo apt install python3.11 python3.11-venv python3.11-dev -y
     ```
   - **macOS**:
     ```bash
     brew install python@3.11
     brew link --force python@3.11 # Makes 'python3.11' command accessible system-wide
     ```

To generate documentation, please install **Texinfo** and **TeX** first:

   - **Ubuntu/Debian**: `sudo apt install texinfo texlive -y`
   - **macOS**: `brew install texinfo texlive`

Make sure groff is installed to display the CLI manual: `groff --version`. If not installed, install it via:  
   - **Ubuntu/Debian**: `sudo apt install groff`
   - **macOS**: `brew install groff`

#### Ready-to-use Codespace

This repo’s codespace is pre-configured with all dependencies through the devcontainer. Feel free to quickly try out `nostr-nomad` there.

---

## How to Use

1. **Clone the Repository**   
   Clone the repository and navigate into the project directory:  
   ```
   git clone https://github.com/alx-sch/nostr-nomad nostr-nomad && nostr-nomad
   ```
2. **Provide Substack Export**   
 - Export your Substack data (check [here](https://support.substack.com/hc/en-us/articles/360037466012-How-do-I-export-my-posts)).
 - **Optional:** After unzipping the archive, you can remove any posts you don’t want to migrate by deleting their corresponding `.html` files in the `posts/` folder. Make sure to also remove these posts from the `posts.csv` file.
 - Place the export zip file or directory into `user_entries/export/`. It should contain a `posts.csv` file and a `posts/` directory with your `.html` files.
   
3. **Set Configurations**
Provide the following information in the `user_entries/config.ini` file:   
- **Private key:** Enter your Nostr private key in hex or nsec format, or set it to `x` to generate a random key at runtime. *This key is used only to sign Nostr events locally and is never shared.*   
⚠️ Note: Some relays may require prior authorization and might reject events from unknown keys.
- **Post type:** Choose what kind of post you want to publish:
  - `note` — short, unformatted notes (like tweets)
  - `blog` — longer, formatted blog-style posts
- **Relays:** List the WebSocket URLs of the relays you want to publish to.
- **Image hosting (optional)**: Choose how you'd like to handle images by setting `image_host` to one of the following:
  - `substack` – Keep the original image URLs from Substack
  - `imgur` – Upload images to [imgur.com](imgur.com)
  - `wala` – Upload images to your own [WALA server](https://github.com/nolash/WALA) (a self-hosted image store)    
  If you choose `wala`, make sure to set your `wala_url`.   
  If you choose `imgur`, you'll need to provide your `imgur_client_id`.   
      
4. **Run `nostr-nomad`**
    - **Build and Run**    
       `make` — Sets up the virtual environment, installs dependencies, and runs the tool.
    - **Generate Documentation** (WIP)    
       `make docs` — Builds documentation in various formats: `README.md`, HTML, PDF.    
       `make clean-docs` — Removes generated documentation files.
    - **View Man Page** (WIP)    
       `make man` — Displays a terminal-friendly manual for quick command reference.
    - **Clean Build Artifacts**    
        `make clean` — Removes the virtual environment and temporary files.
    - **Full Cleanup**   
        `make clean-all` — Removes everything: environment, docs, cache/archive, and Substack export data.
  
5. XXXX (cache/archive etc.)

#### ⚠️ Troubleshooting

If you run into issues like:   
- `ModuleNotFoundError`
- Environment seems broken or misconfigured
- Tool fails to run right after a `make`

Try resetting the environment:
```bash
make uninstall
make install
```

relay publishing issues (timeout, incorrect imgur ID etc)


--- 

## XXXX TBD

- Short-form vs Long-form message
- not all clients support long-form message or preview of all hyperlinks (eg. while most support previewing .jpeg not all support .avif
- some relays don't seem to like 'fast publishing' --> increase delay between posts (see fct `publish_posts`).

<p align="center">
    <img src="https://github.com/alx-sch/nostr-nomad/blob/main/.assets/running_nostr-nomad_2.png" width="600" alt="running_nostr-nomad_2.png"/>
</p>

```python
import requests

def delete_images_from_imgur(cache: dict, client_id: str):
    """
    Deletes images from Imgur using delete tokens stored in the cache 'image.json'.

    Parameters:
        cache (dict): 'image.json' as created by bnostr-nomad.
        client_id (str): Imgur API client ID.
    """
    headers = {"Authorization": f"Client-ID {client_id}"}
    
    for filename, info in cache.items():
        delete_token = info.get("delete_token")
        if not delete_token:
            print(f"Skipping {filename}: no delete token available.")
            continue

        url = f"https://api.imgur.com/3/image/{delete_token}"
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print(f"Deleted {filename} successfully.")
        else:
            print(f"Failed to delete {filename}: {response.status_code} - {response.text}")
```
      
---

## Setting up a Local Nostr Relay for Testing

Before publishing to public Nostr relays, consider testing your setup with a local relay. This lets you explore how `nostr-nomad` works without impacting the broader network.
Below is a setup guide for `nostr-rs-relay`, but any other compatible relay should work, too.

1. **Install Rust**   
   The first step is to install Rust. This is needed to compile and run the `nostr-rs-relay` project.
     
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   To make `rustc` and its package manager `cargo` available in your terminal, run:

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
   Before running the relay, you need to create the database directory first (`mkdir db`) in the root of the `nostr-rs-relay` repository. The relay will store data such as events and connections here.    
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

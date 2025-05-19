.. nostr-nomad documentation master file, created by
   sphinx-quickstart on Mon Mar 31 20:49:10 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nostr-nomad
=====

**nostr-nomad** is a migration tool for publishing Substack content to Nostr relays.  
It supports local archiving and re-hosting of images.

Source code and documentation: https://github.com/alx-sch/nostr-nomad
 
content
--------

.. toctree::
   :maxdepth: 2

   api/main

.. toctree::
   :maxdepth: 2
   :caption: parsing

   api/parse_config
   api/parse_export
   api/keys

.. toctree::
   :maxdepth: 2
   :caption: image handling

   api/imgs
   api/imgs_uploader

.. toctree::
   :maxdepth: 2
   :caption: post building

   api/build_posts
   api/build_post_longform
   api/build_post_shortform
   api/event_builder
   api/event_publisher

.. toctree::
   :maxdepth: 2
   :caption: utils

   api/errors
   api/utils
   api/models

authors
--------

| **Natalie Holbrook**  
| GitHub: https://github.com/busedame   
| Nostr: `npub12mxhsrukz9r2cehyemkltrnpvp4ajaw5vsr0j0250f3a8j773v5shcx7jk`  

| **Alex Schenk**  
| GitHub: https://github.com/alx-sch  
| Nostr: `npub16e8ngadkas6uxv5hk6fpws7w74ne2wy6e3t2m993jcthmrjkkwlsrl0p4x` 

license
--------

This project is licensed under the AGPL3+.
See the full license text in the LICENSE file in the repository.

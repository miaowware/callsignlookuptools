=====================
Callsign Lookup Tools
=====================

A QRZ.com and callook.info API interface in Python with sync and async support.

.. highlight:: none

.. toctree::
    :hidden:
    :maxdepth: 2

    cli
    api
    types

Installation
============

``callsignlookuptools`` requires Python 3.8 at minimum. Install by running:

.. code-block:: sh

    # synchronous requests only
    $ pip install callsignlookuptools

    # asynchronous aiohttp only
    $ pip install callsignlookuptools[async]

    # both sync and async
    $ pip install callsignlookuptools[all]

    # enable the CLI
    $ pip install callsignlookuptools[cli]

.. NOTE:: If ``requests``, ``aiohttp``, or ``rich`` are installed another way, you will also have access to the sync, async, or command-line interface, respectively.

License
=======

Copyright 2021 classabbyamp, 0x5c

Released under the BSD 3-Clause License. See ``LICENSE`` for the full license text.

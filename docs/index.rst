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

``callsignlookuptools`` requires Python 3.9 at minimum. Install by running:

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

Getting Started
===============

Using CallsignLookupTools is designed to be very simple.
The following examples show basic use of the library.

Sync
----

.. code-block:: py

    # import the sync client for the service you want to use
    from callsignlookuptools import QrzSyncClient, CallsignLookupError

    # instantiate the lookup client
    # some clients require a username, password, or other arguments
    lookup_client = QrzSyncClient(username="...", password="...")

    # perform a search query
    try:
        # this will be a CallsignData object
        lookup_result = lookup_client.search("W1AW")
    # if an error occurs while performing the query,
    # it will raise a CallsignLookupError
    except CallsignLookupError as e:
        print(e)
    else:
        print(lookup_result)

Async
-----

.. code-block:: py

    import asyncio

    # import the async client for the service you want to use
    from callsignlookuptools import QrzAsyncClient, CallsignLookupError

    # instantiate the lookup client
    # some clients require a username, password, or other arguments
    lookup_client = QrzAsyncClient(username="...", password="...")

    # for the async client, queries must be run inside coroutines
    async def run_query():
        # perform a search query
        try:
            # this will be a CallsignData object
            lookup_result = await lookup_client.search("W1AW")
        # if an error occurs while performing the query,
        # it will raise a CallsignLookupError
        except CallsignLookupError as e:
            print(e)
        else:
            print(lookup_result)
        # if you're using the internally-generated session,
        # make sure to clean up
        await lookup_client.close_session()

    # run the task
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_query())


License
=======

Copyright 2021 classabbyamp, 0x5c

Released under the BSD 3-Clause License. See ``LICENSE`` for the full license text.

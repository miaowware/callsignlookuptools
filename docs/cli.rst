=========
CLI Usage
=========

.. NOTE:: To use the CLI, install with the extra ``cli`` (e.g. ``pip install callsignlookuptools[cli]``) or otherwise install the library ``rich``.

``callsignlookuptools`` has a basic CLI interface, which can be run using:

.. code-block:: sh

    $ python3 -m callsignlookuptools

It can be used with the following arguments:

.. code-block:: none

    usage: callsignlookuptools [-h] [-v] [--no-pretty] [-q | -l | -a | -r] [-u USERNAME] [-p PASSWORD] [CALL]

    Retrieve callsign data from various sources

    positional arguments:
      CALL                  The callsign to look up

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Show the version of this program and exit
      --no-pretty           Don't pretty-print output
      -q, --qrz             Use QRZ as lookup source
      -l, --callook         Use Callook as lookup source
      -a, --hamqth          Use HamQTH as lookup source
      -r, --qrzcq           Use QRZCQ as lookup source
      -u USERNAME, --user USERNAME, --username USERNAME
                            Data source username. Needed for QRZ, HamQTH, and QRZCQ.
                            If needed and not specified, it will be asked for
      -p PASSWORD, --pass PASSWORD, --password PASSWORD
                            Data source password. Needed for QRZ, HamQTH, and QRZCQ.
                            If needed and not specified, it will be asked for

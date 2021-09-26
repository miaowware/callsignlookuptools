=========
CLI Usage
=========

.. NOTE:: To use the CLI, install with the extra ``cli`` (e.g. ``pip install callsignlookuptools[cli]``) or otherwise install the library ``typer[all]`` and ``click-help-colors``.

``callsignlookuptools`` has a basic CLI interface, which can be run using:

.. code-block:: sh

    $ python3 -m callsignlookuptools

It can be used with the following arguments:

.. code-block:: none

    $ python3 -m callsignlookuptools --help
    Usage: python -m callsignlookuptools [OPTIONS] COMMAND [ARGS]...

      A QRZ, Callook, HamQTH, and QRZCQ API interface in Python with sync and async support.

    Options:
      -v, --version  Show the version of this program and exit.
      -h, --help     Show this message and exit.

    Commands:
      callook  Use Callook to look up a callsign
      hamqth   Use HamQTH to look up a callsign
      qrz      Use QRZ to look up a callsign
      qrzcq    Use QRZCQ to look up a callsign

Each lookup source is a subcommand, and any source-specific options can be viewed by using the ``-h`` or ``--help`` argument on that subcommand.

For example, the QRZ lookup source has the following options:

.. code-block:: none

    $ python3 -m callsignlookuptools qrz --help
    Usage: python -m callsignlookuptools qrz [OPTIONS] CALL

      Use QRZ to look up a callsign

      Requires a QRZ account and an XML Logbook Data or QRZ Premium subscription

    Options:
      -u, --user, --username TEXT  QRZ username (will be prompted if not provided)  [required]
      -p, --pass, --password TEXT  QRZ password (will be prompted if not provided)  [required]
      CALL                         The callsign to look up  [required]
      -h, --help                   Show this message and exit.

An example invocation that looks up W1XYZ on QRZ, where the username is provided, and the password will be prompted for:

.. code-block:: sh

    $ python3 -m callsignlookuptools qrz --username w1aw W1XYZ


"""
callsignlookuptools commandline interface
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from sys import stderr
from typing import Optional

from callsignlookuptools import __info__
from callsignlookuptools.common.enums import DataSource
from callsignlookuptools.cli import run_query, ColourTyper

try:
    import typer
    from typer import colors, echo, style
except ModuleNotFoundError:
    print(f"To use the {__info__.__project__} CLI you must install 'typer[all]'", file=stderr)
    raise SystemExit(42)


app = ColourTyper(add_completion=False)


def version_callback(value: bool):
    if value:
        echo(f"{style(__info__.__project__, fg=colors.BLUE)} {style('v'+__info__.__version__, fg=colors.GREEN)}")
        raise typer.Exit()


@app.callback(no_args_is_help=True)
def main(
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True,
                                           help="Show the version of this program and exit.")
):
    """A QRZ, Callook, HamQTH, and QRZCQ API interface in Python with sync and async support."""
    ...


@app.command()
def qrz(
    username: str = typer.Option(..., "--user", "--username", "-u", prompt=True,
                                 help="QRZ username (will prompt if not provided)"),
    password: str = typer.Option(..., "--pass", "--password", "-p", prompt=True, hide_input=True,
                                 help="QRZ password (will prompt if not provided)"),
    call: str = typer.Argument(..., help="The callsign to look up"),
):
    """Use QRZ to look up a callsign

    Requires a QRZ account and an XML Logbook Data or QRZ Premium subscription"""
    run_query(DataSource.QRZ, call, username, password)


@app.command()
def callook(
    call: str = typer.Argument(..., help="The callsign to look up"),
):
    """Use Callook to look up a callsign"""
    run_query(DataSource.CALLOOK, call)


@app.command()
def hamqth(
    username: str = typer.Option(..., "--user", "--username", "-u", prompt=True,
                                 help="HamQTH username (will prompt if not provided)"),
    password: str = typer.Option(..., "--pass", "--password", "-p", prompt=True, hide_input=True,
                                 help="HamQTH password (will prompt if not provided)"),
    call: str = typer.Argument(..., help="The callsign to look up"),
):
    """Use HamQTH to look up a callsign

    Requires a HamQTH account"""
    run_query(DataSource.HAMQTH, call, username, password)


@app.command()
def qrzcq(
    username: str = typer.Option(..., "--user", "--username", "-u", prompt=True,
                                 help="QRZCQ username (will prompt if not provided)"),
    password: str = typer.Option(..., "--pass", "--password", "-p", prompt=True, hide_input=True,
                                 help="QRZCQ password (will prompt if not provided)"),
    call: str = typer.Argument(..., help="The callsign to look up"),
):
    """Use QRZCQ to look up a callsign

    Requires a QRZCQ account and a QRZCQ Premium subscription"""
    run_query(DataSource.QRZCQ, call, username, password)


if __name__ == "__main__":
    app()

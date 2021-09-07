"""
callsignlookuptools commandline interface
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from sys import stderr
from enum import Enum
from dataclasses import asdict
import argparse
from getpass import getpass
from datetime import datetime
from typing import Callable

from callsignlookuptools import QrzSyncClient, CallookSyncClient, HamQthSyncClient, QrzCqSyncClient
from callsignlookuptools import CallsignData, CallsignLookupError, __version__
from callsignlookuptools.common.enums import DataSource

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.style import Style
except ModuleNotFoundError:
    print("To use the callsignlookuptools CLI you must install 'rich'", file=stderr)
    raise SystemExit(42)


def tabulate(data: CallsignData, colour: bool = False) -> str:
    d = asdict(data)
    result = ""
    indent = "\n    "

    for field, val in d.items():
        if field in ["raw_data", "query", "data_source"]:
            continue
        if val is None:
            continue
        if isinstance(val, datetime):
            val = f"{val:%Y-%m-%d}"
        if isinstance(val, list) or isinstance(val, tuple):
            val = indent + indent.join(val)
        elif isinstance(val, Enum):
            if val.value != "":
                val = val.value
            else:
                continue
        elif isinstance(val, dict):
            if set(val.values()) == set([None]):
                continue
            dv = {}
            for k, v in val.items():
                if isinstance(v, Enum):
                    dv[k] = v.value
                else:
                    dv[k] = v
            if colour:
                val = indent + indent.join([f"[yellow]{k}:[/yellow] {v}" for k, v in dv.items() if v is not None])
            else:
                val = indent + indent.join([f"{k}: {v}" for k, v in dv.items() if v is not None])
        if colour:
            result += f"[blue]{field}:[/blue] [default]{val}[/default]\n"
        else:
            result += f"{field}: {val}\n"
    return result.rstrip("\n")


parser = argparse.ArgumentParser(prog="callsignlookuptools",
                                 description="Retrieve callsign data from various sources")
parser.add_argument("-v", "--version", required=False, action="store_true", dest="version",
                    help="Show the version of this program and exit")
parser.add_argument("--no-pretty", required=False, action="store_false", dest="pretty",
                    help="Don't pretty-print output")

src_group = parser.add_mutually_exclusive_group(required=False)
src_group.add_argument("-q", "--qrz", action="store_const", const=DataSource.QRZ, dest="src",
                       help="Use QRZ as lookup source")
src_group.add_argument("-l", "--callook", action="store_const", const=DataSource.CALLOOK, dest="src",
                       help="Use Callook as lookup source")
src_group.add_argument("-a", "--hamqth", required=False, action="store_const", const=DataSource.HAMQTH, dest="src",
                       help="Use HamQTH as lookup source")
src_group.add_argument("-r", "--qrzcq", required=False, action="store_const", const=DataSource.QRZCQ, dest="src",
                       help="Use QRZCQ as lookup source")

parser.add_argument("-u", "--user", "--username", required=False, type=str, dest="username", action="store",
                    help=("Data source username. Needed for QRZ, HamQTH, and QRZCQ. "
                          "If needed and not specified, it will be asked for"))
parser.add_argument("-p", "--pass", "--password", required=False, type=str, dest="password", action="store",
                    help=("Data source password. Needed for QRZ, HamQTH, and QRZCQ. "
                          "If needed and not specified, it will be asked for"))
parser.add_argument("call", type=str, metavar="CALL", nargs="?", help="The callsign to look up")
args = parser.parse_args()


if args.version:
    print("callsignlookuptools v" + __version__)
    raise SystemExit(0)


if args.pretty:
    c = Console()
    ec = Console(stderr=True, style="bold red")


lookup_classes = {
    DataSource.QRZ: QrzSyncClient,
    DataSource.CALLOOK: CallookSyncClient,
    DataSource.HAMQTH: HamQthSyncClient,
    DataSource.QRZCQ: QrzCqSyncClient,
}


if args.src:
    source = args.src
    lookup: Callable = lookup_classes[args.src]
else:
    print("No lookup source given")
    raise SystemExit(1)


# auth sources
if source in (DataSource.QRZ, DataSource.HAMQTH, DataSource.QRZCQ):
    if args.username:
        username = args.username
    else:
        username = input(f"{source.value.capitalize()} Username: ")

    if args.password:
        password = args.password
    else:
        password = getpass(f"{source.value.capitalize()} Password: ")

    lookup_obj = lookup(username=username, password=password)
# non-auth sources
elif source in (DataSource.CALLOOK,):
    lookup_obj = lookup()


if args.call:
    call = args.call.upper()
    try:
        result = lookup_obj.search(call)
        if args.pretty:
            c.print(
                Panel.fit(
                    tabulate(result, True),
                    title=f"{source.value.capitalize()} Data for {call}",
                    border_style=Style(color="green")
                )
            )
        else:
            print(f"\n{source.value.capitalize()} Data for {call}:")
            print(tabulate(result))
    except CallsignLookupError as e:
        if args.pretty:
            ec.print(
                Panel.fit(
                    str(e),
                    title=f"{source.value.capitalize()} Data for {call}",
                    style=Style(color="red"),
                    border_style=Style(color="red")
                )
            )
        else:
            print(f"\n{source.value.capitalize()} Data for {call}:")
            print(e)
else:
    print("No callsign query given")
    raise SystemExit(1)

"""
callsignlookuptools commandline interface helpers
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""

from sys import stderr
from enum import Enum
from dataclasses import asdict
from datetime import datetime
from typing import Callable, Optional

from callsignlookuptools import QrzSyncClient, CallookSyncClient, HamQthSyncClient, QrzCqSyncClient
from callsignlookuptools import CallsignData, CallsignLookupError, __info__
from callsignlookuptools.common.enums import DataSource

try:
    import typer
    from typer import colors, echo, secho, style
except ModuleNotFoundError:
    print(f"To use the {__info__.__project__} CLI you must install 'typer[all]'", file=stderr)
    raise SystemExit(42)

try:
    from click_help_colors import HelpColorsCommand, HelpColorsGroup  # type: ignore[import]
except ModuleNotFoundError:
    secho(f"To use the {__info__.__project__} CLI you must install 'click-help-colors'", fg=colors.RED, err=True)
    raise typer.Exit(42)


lookup_classes = {
    DataSource.QRZ: QrzSyncClient,
    DataSource.CALLOOK: CallookSyncClient,
    DataSource.HAMQTH: HamQthSyncClient,
    DataSource.QRZCQ: QrzCqSyncClient,
}


def tabulate(data: CallsignData) -> str:
    """tabulates and styles the result of a callsign query"""
    d = asdict(data)
    result = ""
    indent = "\n    "

    for field, val in d.items():
        # don't include the raw data fields
        if field in ["raw_data", "query", "data_source"]:
            continue

        # also don't include fields that are none (empty)
        if val is None or val == "":
            continue

        # datetime handling
        if isinstance(val, datetime):
            val = f"{val:%Y-%m-%d}"

        # list pretty-printing
        if isinstance(val, list) or isinstance(val, tuple):
            val = indent + indent.join(val)

        # enum pretty-printing
        elif isinstance(val, Enum):
            if val.value != "":
                val = val.value
            else:
                continue

        # dict pretty-printing (recursive)
        elif isinstance(val, dict):
            if set(val.values()) == set([None]) or set(val.values()) == set([""]):
                continue
            dv = {}
            for k, v in val.items():
                if isinstance(v, Enum):
                    dv[k] = v.value
                else:
                    dv[k] = v
            val = indent + indent.join([f"{style(k + ':', fg=colors.YELLOW)} {v}"
                                        for k, v in dv.items() if v])

        result += f"{style(field + ':', fg=colors.BLUE, bold=True)} {val}\n"
    return result.rstrip("\n")


def run_query(source: DataSource, query: str, username: Optional[str] = None, password: Optional[str] = None):
    """sets up and runs a callsign query, then prints the result"""
    lookup: Callable = lookup_classes[source]

    # non-auth sources
    if source in (DataSource.CALLOOK,):
        lookup_obj = lookup()
    # auth sources
    else:
        lookup_obj = lookup(username=username, password=password)

    if query:
        call = query.upper()
        try:
            result = lookup_obj.search(call)
            echo(style(source.value.capitalize(), fg=colors.CYAN, bold=True) + style(" data for ", fg=colors.CYAN) +
                 style(call, fg=colors.GREEN, bold=True) + style(":", fg=colors.CYAN))
            echo(tabulate(result))
        except CallsignLookupError as e:
            secho(e, fg=colors.RED, err=True)
    else:
        secho("No callsign given", fg=colors.RED, err=True)
        raise typer.Exit(1)


# The following is for adding colours to command help output
# See https://github.com/tiangolo/typer/issues/47

class CustomHelpColoursGroup(HelpColorsGroup):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = "blue"
        self.help_options_color = "yellow"


class CustomHelpColoursCommand(HelpColorsCommand):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.help_headers_color = "blue"
        self.help_options_color = "yellow"


epilog = (f"Copyright {__info__.__copyright__} by {__info__.__author__}. "
          f"Released under the {__info__.__license__} License")


class ColourTyper(typer.Typer):
    def __init__(self, *args, cls=CustomHelpColoursGroup, context_settings={"help_option_names": ["-h", "--help"]},
                 **kwargs) -> None:
        super().__init__(*args, cls=cls, context_settings=context_settings, epilog=epilog, **kwargs)

    def command(self, *args, cls=CustomHelpColoursCommand, context_settings={"help_option_names": ["-h", "--help"]},
                **kwargs) -> Callable:
        return super().command(*args, cls=cls, context_settings=context_settings, epilog=epilog, **kwargs)

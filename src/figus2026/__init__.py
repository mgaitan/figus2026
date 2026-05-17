"""
figus2026

Nuestro album de figus para el mundial
"""

import argparse
from importlib import metadata


def get_version() -> str:
    try:
        return metadata.version("figus2026")
    except metadata.PackageNotFoundError:
        return "unknown"


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="figus2026")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {get_version()}")
    return parser


def main(args: list[str] | None = None) -> int:
    """Run the main program."""
    parser = get_parser()
    opts = parser.parse_args(args=args)
    print(opts)
    return 0


__all__: list[str] = ["get_parser", "main"]

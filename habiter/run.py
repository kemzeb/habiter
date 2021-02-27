#!/usr/bin/env python3

'''
'   Main program for habiter
'''
import argparse

import habiter.cli as cli

from habiter.commands.habiter import Habiter


def main():
    parser = cli.create_parser()
    cli.exe_using_parser(Habiter(), parser)


if __name__ == "__main__":
    main()

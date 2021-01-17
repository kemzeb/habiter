'''
'   hab.py
'
'   Main program for habiter
'
'''
import argparse

import habiter_cli as cli

from habiter import Habiter
from updater import HAB_JSON_FPATH

def main():
    parser = cli.create_parser()
    cli.exe_using_parser(Habiter(HAB_JSON_FPATH), parser)


if __name__ == "__main__":
    main()

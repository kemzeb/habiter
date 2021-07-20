#!/usr/bin/env python3

'''
'   Main program for habiter
'''

import habiter.internal.cli as cli

from habiter.internal.upkeep.updater import HabiterUpdater


def main():
    HabiterUpdater()
    cli.habiter()


if __name__ == "__main__":
    main()

'''
'	hab.py
'
'	Main program for Habiter
'
'''
import argparse

import habiter_cli as cli
import updater as upt
from habiter import Habiter


def main():
	parser = cli.create_parser()
	args = parser.parse_args() # parse sys args
	cli.exe_using_args( Habiter(upt.HAB_JSON_FPATH), args )


if __name__ == "__main__":
	main()

'''
'	habiter_cli.py
'
'	Command line interface for Habiter
'''
import argparse

from os import path

# User-defined modules
from habiter import Habiter


def exe_using_args(hab, args:argparse.Namespace):
	if args.func != None: # Check if system arguments were inputted
		args.func(hab, args)

## Functions below are used for the set_defaults() method 
def occ(hab, args:argparse.Namespace):	
	if args.num:
		hab.occurrence(args.habits, args.num)
	elif args.zero:
		hab.occurrence(args.habits, 0)
	else:
		hab.occurrence(args.habits)


def add(hab, args:argparse.Namespace):
	hab.add_habits(*args.habits)


def delete(hab, args:argparse.Namespace):
	hab.delete_habits(*args.habits)


def reset(hab, args:argparse.Namespace):
	hab.reset_habits(*args.habits)


def list_habits(hab, args:argparse.Namespace):
	if args.keys:
		hab.list_habits_k()
	elif args.kstats:
		print("[ERROR: CLI:\t--stats not yet implemented.]")
		#hab.list_habits_ks()
	else:
		hab.list_habits()
## - - - - -


def create_parser():
	parser = argparse.ArgumentParser(
			formatter_class= argparse.RawTextHelpFormatter,
			description="Quantifies and keeps tabs on unwanted habits you have \ndeveloped over time.",
			epilog='''For more information about these commands, visit the \ncode repository at https://github.com/kemzeb/habiter.''')
	sub_parser = parser.add_subparsers(dest="subcom")
	parser.set_defaults(func=None)

	# Subparser parent for parsers that require a collection of habits as argument
	parent_parser = argparse.ArgumentParser(add_help=False)
	parent_parser.add_argument("habits",
								type=str,
								nargs="+",
								help="provide a single or a collection of habits")
	## Parser for occurrence feature
	parser_occ = sub_parser.add_parser("occ", 
										parents=[parent_parser], 
										help="increment occurrence for habit(s)")
	group = parser_occ.add_mutually_exclusive_group()
	group.add_argument("-z", "--zero", 
						action="store_true",
						help='''inform Habiter that you had no occurrences for some habit(s)
								(more importantly informs that some habit(s) is/are not inactive)''')
	group.add_argument("-n", "--num", 
						type=int, 
						choices=range(1, 100), 
						metavar="[0-100]",
						help='''provide a specific # of occurrences (note that 
								this will apply to all habits inputted)''')
	parser_occ.set_defaults(func=occ)

	## Parser for add habits feature
	parser_add = sub_parser.add_parser("add", 
										parents=[parent_parser], 
										help="add new habit(s) into record")
	parser_add.set_defaults(func=add)	

	## Parser for delete habits feature
	parser_del = sub_parser.add_parser("del", 
										parents=[parent_parser], 
										help="delete habit(s) from record")
	parser_del.set_defaults(func=delete)	

	## Parser for reset habits feature
	parser_reset = sub_parser.add_parser("reset", 
										parents=[parent_parser], 
										help="reset habit(s) to default state")
	parser_reset.set_defaults(func=reset)	

	## Parser for listing habits feature
	parser_list = sub_parser.add_parser("list", 
										help="list all habits on record")
	parser_list.add_argument("-k", "--keys",
							action="store_true",
							help="list all habits + attributes on record", 
							dest="keys")
	parser_list.add_argument("-s, --stats",
							action="store_true",
							help="list all habits + attributes + stats on record",
							dest="kstats")
	parser_list.set_defaults(func=list_habits)	

	return parser

'''
'	habiter_cli.py
'
'	Command line interface for Habiter
'''
import argparse
import sys

from os import path

# User-defined modules
from habiter import Habiter


def main():
	parser = create_parser()
	args = parser.parse_args()

	habiter = Habiter("records.json")
	compute_using_args(habiter, args)


def compute_using_args(hab, args):
	if args.add:
		hab.add_habits(*args.add)
	if args.delete:
		hab.delete_habits(*args.delete)
	if args.occ:
		hab.occurrence(*args.occ)
	if args.reset:
		hab.reset_habits(*args.reset)

	if args.list:
		hab.list_habits()
	if args.listk:
		hab.list_habits_k()



def create_parser():
	parser = argparse.ArgumentParser(
			description="Quantifies and keeps tabs on unwanted habits you have developed over time.")

	# Add arguments
	parser.add_argument("-o", "--occ",
						type=str,
						metavar='',
						nargs="+",
						help="Increment occurrence for habit(s)")

	parser.add_argument("-a", "--add",
						type=str, 
						metavar='',
						nargs='+', # Allows mutiple habits to be added
						help="Add new habit(s) by providing their name")

	parser.add_argument("-d", "--delete",
						type=str,
						metavar='',
						nargs='+', # Allows mutiple habits to be deleted
						help="Delete habit(s) by providing their name")

	parser.add_argument("--reset",
						type=str,
						metavar='',
						nargs='+', # Allows mutiple habits to be reset
						help="Reset habit(s) to default state")

	parser.add_argument("-l", "--list",
						action="store_true",
						help="List all provided habits")

	parser.add_argument("-lk", "--listk",
						action="store_true",
						help="List all provided habits + attributes")

	parser.add_argument("-lks", "--listks",
						action="store_true",
						help="List all provided habits + attributes + stats")
	return parser



if __name__ == "__main__":
	main()

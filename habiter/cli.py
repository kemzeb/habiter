'''
'   cli.py
'
'   Command line interface for Habiter
'
'   The commands and options below
'   maybe moved in the future to their
'   own corresponding files.
'''
import argparse
import sys

from os import path

from habiter.utils.messenger import display_error_message
from habiter.commands.habiter import Habiter


def exe_using_parser(hab, parser:argparse.Namespace):
    '''Parses command line arguments and uses a 'Habiter' instance to act upon them
    Parameters
        hab:    a Habiter instance
        parser: an ArugmentParser instance
    '''
    args = parser.parse_args() # parse sys args

    if len(sys.argv) > 1:
        args.func(hab, args)
    else:
        parser.print_help()


## Functions below are used for the set_defaults() method
#  utilized during argument parsing
def main_cl(hab, args:argparse.Namespace):
    if args.version:
        from habiter.upkeep.updater import HABITER_VERSION
        print(f"habiter v{HABITER_VERSION}")


def tally(hab, args:argparse.Namespace):
    if args.num:
        hab.tally_habits(args.habits, args.num)
    elif args.zero:
        hab.tally_habits(args.habits, 0)
    else:
        hab.tally_habits(args.habits)


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
        #hab.list_habits_ks()
        display_error_message(" -s/--stats not yet implemented")
    else:
        hab.list_habits()
## - - - - -


def create_parser():
    parser = argparse.ArgumentParser(
            formatter_class= argparse.RawTextHelpFormatter,
            description="Quantifies and keeps tabs on unwanted habits you have \ndeveloped over time.",
            epilog='''For more information, visit the code repository\nat https://github.com/kemzeb/habiter.''')
    # Subparser for subcommnads
    sub_parser = parser.add_subparsers(#title="subcommands"
                                    dest="subcom")

    # Main parser optional arguments
    parser.add_argument("--version",
                        action="store_true")
    parser.set_defaults(func=main_cl)

    # Subparser parent for parsers that require a collection of habits as argument
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("habits",
                                type=str,
                                nargs="+",
                                help="provide a single or a collection of habits")
    ## Parser for tally feature
    occ_parser = sub_parser.add_parser("tally",
                                        parents=[parent_parser],
                                        formatter_class= argparse.RawTextHelpFormatter,
                                        description="Increments the number of occurrences for some habit(s).\nSpecify the '-z/--zero' flag to inform Habiter that\nyou did not have any occurrences for a particular \nday.",
                                        help="increment tally for some habit(s)")

    # Group flags as they cannot share outcomes
    # Note that the 'help' strings below must
    # maintain its indentation as it is mirrored
    # in a particular way for sys.stdout
    group = occ_parser.add_mutually_exclusive_group()
    group.add_argument("-z", "--zero",
                        action="store_true",
                        help="""inform habiter that you had no occurrences for some habit(s) \
                        \n(more importantly informs that some habit(s) is/are active)""")
    group.add_argument("-n", "--num",
                        type=int,
                        choices=range(1, 100),
                        metavar="[0-100]",
                        help='''provide a specific # of occurrences (note that
this will apply to all habits inputted)''')
    occ_parser.set_defaults(func=tally)

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


import argparse

import habiter_cli as cli
from habiter import Habiter

def main():
	parser = cli.create_parser()
	args = parser.parse_args()
	habiter = Habiter("records.json")

	cli.compute_using_args(habiter, args)



if __name__ == "__main__":
	main()
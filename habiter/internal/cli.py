import click

from habiter.internal.commands import (
    add, list, remove, reset, tally
)
from habiter import __version__


@click.group(help="Quantifies and keeps tabs on unwanted habits you have developed over time.",
             epilog='For more information, visit the code repository at https://github.com/kemzeb/habiter.')
@click.version_option(version=__version__)
def habiter():
    pass

habiter.add_command(add.add)
habiter.add_command(list.list)
habiter.add_command(remove.remove)
habiter.add_command(reset.reset)
habiter.add_command(tally.tally)

import click

from habiter.internal.utils.consts import HABITER_VERSION
from habiter.internal.commands import (
    add, list, remove, reset, tally
)


@click.group(help="Quantifies and keeps tabs on unwanted habits you have developed over time.",
             epilog='For more information, visit the code repository at https://github.com/kemzeb/habiter.')
@click.version_option(version=HABITER_VERSION)
def habiter():
    pass

habiter.add_command(add.add)
habiter.add_command(list.list)
habiter.add_command(remove.remove)
habiter.add_command(reset.reset)
habiter.add_command(tally.tally)

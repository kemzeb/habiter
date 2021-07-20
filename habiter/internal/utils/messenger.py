'''
    Module that handles habiter normal
    and error display messages on the
    console.

'''
import click


def echo_success(text: str):
    click.secho(f"[habiter]  {text}", fg='cyan', bold=True)


def echo_failure(text: str):
    click.secho(f"[habiter: error]  {text}", fg='red', bold=True)


def echo_internal_failure(text: str):
    click.secho(f"[habiter: internal_error]  {text}", fg='red', bold=True)


def echo_warning(text: str):
    click.secho(f"[habiter]  {text}", fg='yellow', bold=True)


def echo_info(text: str):
    click.secho(f"[habiter]  {text}", bold=True)


def inquire_choice(choice: str) -> bool:
    echo_info(f"Are you sure you want to {choice}? This cannot be undone.")
    ans = ''
    while True:
        ans = input("[Provide a y/n.]: ")

        if ans != "y" and ans != "n":
            echo_warning("Please try again.")
        else:
            return True if ans == 'y' else False

'''
    Module that handles habiter normal
    and error display messages on the
    console.

'''
import textwrap


def display_message(text:str):
    if len(text) != 0 and text[0] == '\n':
        #...ignore newlines
        text = text[1:]
    print(f"[habiter]  {text}")


def display_error_message(text:str):
    print(f"[habiter: error]  {text}")


def display_internal_error_message(text:str):
    print(f"[habiter: internal_error]  {text}")


def display_wrap_message(text:str, addHeader=True):
    ''' wrap_message_normal(text : string) -> None

    Uses the textwrap public method 'fill' to return
    a wrapped string given the arguments provided
    in its initialization. Definitely needs working
    on
    '''
    header = "[habiter]" if addHeader is True else ""
    print(f"{header} " + textwrap.fill(text,
                            width = 70,
                            initial_indent = "\t",
                            subsequent_indent = "\t\t") )


def inquire_choice(choice:str):
    display_message(f"Are you sure you want to {choice}? This cannot be undone.\n")
    ans = ''
    while True:
        ans = input("[Provide a y/n.]: ")

        if ans != "y" and ans != "n":
            print("[err: INQUIRE_CHOICE] Please try again.")
        else:
            return True if ans == 'y' else False
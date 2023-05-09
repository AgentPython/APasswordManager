from os import path, system, remove, makedirs

from sys import stdout, exit
from rich.console import Console
from rich.prompt import Confirm

console = Console()


def logo():
    """
        No comment.
    """
    text = """
    ██╗  ██╗ █████╗ ██╗   ██╗██╗  ████████╗
    ██║ ██╔╝██╔══██╗██║   ██║██║  ╚══██╔══╝
    █████╔╝ ███████║██║   ██║██║     ██║
    ██╔═██╗ ██╔══██║██║   ██║██║     ██║
    ██║  ██╗██║  ██║╚██████╔╝███████╗██║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝
    """
    console.print(text)


def logo_small():
    """
        No comment.
    """
   
    text = """
    ██   ██  █████  ██    ██ ██      ████████
    ██  ██  ██   ██ ██    ██ ██         ██
    █████   ███████ ██    ██ ██         ██
    ██  ██  ██   ██ ██    ██ ██         ██
    ██   ██ ██   ██  ██████  ███████    ██
    """
    console.print(text)


def create_directory_if_missing(dir_):
    """
        Create the vault and configuration file storage folder if it does not exist
    """

    try:
        if not path.exists(dir_):
            makedirs(dir_)

            return True

        return False
    except Exception:
        print()
        print('We were unable to create the folder `%s` to store the vault and configuration file.' % (
            dir_))
        print('Please check the permissions or run `./vault.py --help` to find out how to specify an alternative path for both files.')
        print()
        exit()


def assess_integrity(vault_path, config_path):
    """
        The vault config file contains a salt. The salt is used to unlock the vault along with the master key.
        By default, config files are created automatically. A new config file will not allow to open an existing vault.
        We are ensuring here that a config file exists if a vault exists.
    """

    if not path.isfile(config_path) and path.isfile(vault_path):
        print()
        print("It looks like you have a vault setup but your config file is missing.")
        print("The vault cannot be unlocked without a critical piece of information from the config file (the salt).")
        print("Please restore the config file before proceeding.")
        print()
        exit()


def erase_vault(vault_path, config_path):
    """
        Will erase the vault and config file after asking user for confirmation
    """ 

    console.print()
    if confirm(prompt='Do you want to permanently erase your vault? All your data will be lost!', resp=False):
        # Delete files
        if path.isfile(vault_path):
            remove(vault_path)
        if path.isfile(config_path):
            remove(config_path)

        print()
        print('The vault and config file have been deleted.')
        print()
        exit()
    else:
        exit()


def confirm(prompt=None, resp=False):

    if prompt is None:
        prompt = 'Confirm' 

    if resp:
        return Confirm.ask(f"{prompt}")
    else:
        return Confirm.ask(f"{prompt}", default=False) 


def is_unicode_supported():
    """
        Returns `True` if stdout supports unicode
    """

    if stdout.encoding:
        return stdout.encoding.lower().startswith('utf-')

    return False


def lock_prefix():
    """
        Will prefix locks with a Unicode Character 'KEY' (U+1F511)
        if the user's stdout supports it
    """

    if is_unicode_supported():
        return u'\U0001F511  '  # Extra spaces are intentional

    return ''


def clear_screen():
    """
        Clear user window
    """

    system('clear')

    return True

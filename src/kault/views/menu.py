import sys
import time

from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

from ..modules.carry import global_scope
from ..modules.misc import lock_prefix, clear_screen, logo_small
from ..lib.Encryption import Encryption
from . import secrets, users, categories

timer = None

console = Console()

def get_notes_input(message='', lowercase=False, check_timer=True):
    try:
        input_ = input(message)
        if check_timer:
            check_then_set_autolock_timer()

        if lowercase:
            input_ = input.lower()
    except KeyboardInterrupt:
        return False
    except Exception:
        return False

    return input_

def get_input(choices = None, message='', secure=False, lowercase=False, check_timer=True, non_locking_values=[]):
    """
        Get and return user input
    """

    try:
        if choices:
            input_ = Prompt.ask(lock_prefix() + message, password=True, choices=choices) if secure else Prompt.ask(message, choices=choices)
        else:
            input_ = Prompt.ask(lock_prefix() + message, password=True) if secure else Prompt.ask(message)

        if check_timer and input_ not in non_locking_values:
            check_then_set_autolock_timer()
        else:
            set_autolock_timer()

        if lowercase:
            input_ = input_.lower()
    except KeyboardInterrupt:
        return False
    except Exception:
        return False

    return input_


def unlock(redirect_to_menu=True, tentative=1):
    """
        Asking the user for his master key and trying to unlock the vault
    """

    # Get master key
    print()
    key = get_input(message='Please enter your master key',
                    secure=True, check_timer=False)

    # Exit if the user pressed Ctrl-C
    if key is False:
        print()
        sys.exit()

    if validate_key(key):
        if redirect_to_menu:
            menu()
        else:
            return True
    else:
        if tentative >= 3:
            # Stop trying after 3 attempts
            print('Vault cannot be opened.')
            print()
            sys.exit()
        else:
            # Try again
            print('Master key is incorrect. Please try again!')
            unlock(redirect_to_menu=redirect_to_menu, tentative=tentative + 1)


def validate_key(key):
    """
        Validate a vault key
    """

    # Create instance of Encryption class with the given key
    global_scope['enc'] = Encryption(key.encode())

    # Attempt to unlock the database
    return users.validation_key_validate(key.encode())


def menu(next_command=None):
    """
        Display user menu
    """

    while (True):
        # Check then set auto lock timer
        check_then_set_autolock_timer()

        # Clear screen
        clear_screen()

        # Small logo
        logo_small()

        # Secret count
        console.print(f"[!] You have [bold]{secrets.count()}[/bold] items in the vault", style="#0074D9")
        if next_command:  # If we already know the next command
            command = next_command
            next_command = None  # reset
        else:  # otherwise, ask for user input
            print()
            table = Table()
            table.add_column("Key")
            table.add_column("Title")

            menu = {
                "s": "Search an item in the vault",
                "v": "View all items in the vault",
                "a": "Add an item to the vault",
                "c": "See all categories in the vault",
                "l": "Lock the vault",
                "q": "Quit"
            }

            for key, title in menu.items():
                table.add_row(key, title)

            console.print(table)

            command = get_input(
                message="Choose an option",
                lowercase=True,
                choices=list(menu.keys()),
                non_locking_values=['l', 'q'])

        # Action based on command
        if command == 's':  # Search an item
            next_command = secrets.search_input()
        elif command == 'v':  # Show all items
            print()
            print(secrets.to_table(secrets.all()))
            next_command = secrets.all_input()
            """ next_command = secrets.search_input() """
        elif command == 'a':  # Add an item
            secrets.add_input()
        elif command == 'c':  # Manage categories
            categories.main_menu()
        elif command == 'l':  # Lock the vault and ask for the master key
            lock()
        elif command == 'q':  # Lock the vault and quit
            quit()


def lock():
    """
        Lock the vault and ask the user to login again
    """

    # Lock the vault
    global_scope['enc'] = None

    # Clear screen
    clear_screen()

    # Small logo
    logo_small()

    # Unlock form
    unlock(False)


def quit():
    """
        Exit the program
    """

    # Exit program
    sys.exit()


def set_autolock_timer():
    """
        Set auto lock timer
    """

    global timer

    timer = int(time.time())


def check_autolock_timer():
    """
        Check auto lock timer and lock the vault if necessary
    """

    global timer

    if timer and int(time.time()) > timer + int(global_scope['conf'].autoLockTTL):
        print()
        print("The vault has been locked due to inactivity.")
        lock()


def check_then_set_autolock_timer():
    """
        Check auto lock timer and lock the vault if necessary, then set it again
    """

    check_autolock_timer()
    set_autolock_timer()

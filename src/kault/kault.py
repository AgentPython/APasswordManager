import os
import sys
import atexit

import click

from .lib.Config import Config
from .modules.misc import logo, create_directory_if_missing, assess_integrity, erase_vault
from .views import setup
from .views.menu import unlock
from .views.import_export import import_, export_
from .views.migration import migrate
from .modules.carry import global_scope

# Default paths
dir_ = os.path.expanduser('~') + '/.kault/'
config_path_default = dir_ + '.config'
vault_path_default = dir_ + '.secure.db'
extra_path_default = dir_ + '.extra.db'

def cleanup():
    os.popen('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')


def get_vault_path(override=None):
    """
        Returns the vault location (either default or user defined)
    """

    global vault_path_default

    if override:
        return override
    return vault_path_default


def get_config_path(override=None):
    """
        Returns the config location (either default or user defined)
    """

    global config_path_default

    if override:
        return override
    return config_path_default


def check_directory(vault_path, config_path):
    """
        Create the vault folder if it does not exists yet
    """

    if vault_path == vault_path_default or config_path == config_path_default:
        return create_directory_if_missing(dir_)

    return None


def config_update(clipboard_TTL=None, auto_lock_TTL=None, hide_secret_TTL=None):
    """
        Update config
    """

    if clipboard_TTL:
        return global_scope['conf'].update('clipboardTTL', clipboard_TTL)
    elif auto_lock_TTL:
        return global_scope['conf'].update('autoLockTTL', auto_lock_TTL)
    elif hide_secret_TTL:
        return global_scope['conf'].update('hideSecretTTL', hide_secret_TTL)


def initialize(kault_location_override, config_location_override, erase=None, clipboard_TTL=None, auto_lock_TTL=None, hide_secret_TTL=None, rekey_vault=None, import_file=None, export_file=None, file_format='json'):
    # Some nice ascii art
    logo()

    # Set vault and config path
    vault_path = get_vault_path(kault_location_override)
    config_path = get_config_path(config_location_override)

    # Set vault path at the global scope
    global_scope['db_file'] = vault_path

    # Create the vault folder if it does not exists yet
    check_directory(vault_path, config_path)

    # Assess files integrity
    assess_integrity(vault_path, config_path)

    # Erase a vault if the user requests it
    if erase:
        erase_vault(vault_path, config_path)
        sys.exit()

    # Load config
    global_scope['conf'] = Config(config_path)

    # Migration from Vault 1.x to Vault 2.x
    if global_scope['conf'].version.split('.')[0] == '1':
        migrate(vault_path=vault_path.strip('.db'), config_path=config_path)
        sys.exit()

    # Update config
    config_update(clipboard_TTL, auto_lock_TTL, hide_secret_TTL)

    # Change vault key
    if rekey_vault:
        print()
        # print("Please consider backing up your vault located at `%s` before proceeding." % (
        #     vault_path))
        # change_key.rekey()
        print('This feature is not currently implemented.')
        print('Please export the vault to a Json file, create a new vault with the new key and import the Json file in the new vault.')
        sys.exit()

    # Import items in the vault
    if import_file:
        print()
        print("Please consider backing up your vault located at `%s` before proceeding." % (
            vault_path))
        import_(format_=file_format, path=import_file)
        sys.exit()

    # Export vault
    if export_file:
        if export_file == 'default':
            export_file = '~/.kault/export'

        if export_file.startswith('~'):
            export_file = os.path.expanduser(export_file)
        else:
            export_file = os.path.abspath(export_file)

        if file_format == 'db':
            global_scope['extra_db_file'] = f"{export_file}.kault"
 
        export_(format_=file_format, path=export_file)
        sys.exit()

    # Check if the vault exists
    if not os.path.isfile(vault_path):
        res = setup.initialize(global_scope['conf'].salt)
        if res is False:
            print()
            return False

    # Unlock the vault
    unlock()

@click.command()
@click.option('-t', '--clipboard_TTL', type=int, help="Set clipboard TTL (in seconds, default: 15)", default=15)
@click.option('-p', "--hide_secret_TTL", type=int, help="Set delay before hiding a printed password (in seconds, default: 15)", default=5)
@click.option('-a', '--auto_lock_TTL', type=int, help="Set auto lock TTL (in seconds, default: 900)", default=900)
@click.option('-k', '--kault_location', type=str, help="Set kault path")
@click.option('-c', '--config_location', type=str, help="Set config path")
@click.option('-ck', '--change_key', is_flag=True, help="Change master key")
@click.option('-i', '--import_file', type=str, help="File to import credentials from")
@click.option('-x', '--export_file', type=str, help="File to export credentials to")
@click.option('-f', '--file_format', type=click.Choice(['json', 'yaml', 'db']), help="Import / export file format (default: 'json')", default='json')
@click.option('-e', '--erase_kault', is_flag=True, help="Erase the kault and config file")
@click.version_option(version='0.0.1', prog_name="Kault")
def run(clipboard_ttl, hide_secret_ttl, auto_lock_ttl, kault_location, config_location, change_key, import_file, export_file, file_format, erase_kault):

    initialize(kault_location_override=kault_location,
               config_location_override=config_location,
               erase=erase_kault,
               clipboard_TTL=clipboard_ttl,
               auto_lock_TTL=auto_lock_ttl,
               hide_secret_TTL=hide_secret_ttl,
               rekey_vault=change_key,
               import_file=import_file,
               export_file=export_file,
               file_format=file_format)

def main():
    atexit.register(cleanup)
    run()


if __name__ == '__main__':
    main()

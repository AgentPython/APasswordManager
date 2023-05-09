from configparser import ConfigParser
from os import path, chmod
from uuid import uuid4
from textwrap import dedent

class Config:
    def __init__(self, config_path):
        self.config = ConfigParser()
        self.config_path = config_path

    def get_config(self):
        """
            Will return a user config and set a default if necessary
        """

        # Generate a default config the first time
        if not path.isfile(self.config_path):
            self.set_default_config_file()

        # Load existing config
        self.config.read(self.config_path)
        return self.config['main']

    def set_default_config_file(self):
        """
            Set a user default config file
        """

        self.config['main'] = {}
        self.config['main']['version'] = '0.1.0'
        self.config['main']['keyVersion'] = '1'
        self.config['main']['salt'] = self.generate_random_salt()
        self.config['main']['clipboardTTL'] = '15'
        self.config['main']['hideSecretTTL'] = '5'
        self.config['main']['autoLockTTL'] = '900'
        self.config['main']['encryptedDB'] = 'True'

        return self.save_config()

    def update(self, name, value):
        """
            Update a config value
        """

        # Set the new value
        self.config['main'][name] = str(value)
        text = f"""
        The setting `{name}` is now set to `{value}`
        """
        print(dedent(text))

        return self.save_config()

    def save_config(self):
        """
            Save user config to a file
        """

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

        chmod(self.config_path, 0o600)

        return True

    def generate_random_salt(self):
        """
            Generate a random salt
            Will be used to generate the vault hash with the user master key
        """

        return str(uuid4())

    def __getattr__(self, name):
        """
            Allows calls to configuration values
            config = Config()
            print(config.salt) # Will print the salt
        """

        try:
            return self.get_config()[name]
        except KeyError:
            return None

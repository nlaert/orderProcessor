from os import environ
from configparser import ConfigParser


class ReadConfig:
    def __init__(self):
        super(ReadConfig, self).__init__()

    def read_configs(self):
        self.__read_from_env()
        if self.config['dropshipping_url'] is None:
            print("Could not ")
            self.read_from_config()
            self.read_general_config()
        return self.config

    def __read_from_env(self):
        self.config['dropshipping_url'] = environ.get('dropshipping_url')
        self.config['dropshipping_login'] = environ.get('dropshipping_login')
        self.config['dropshipping_pass'] = environ.get('dropshipping_pass')
        self.config['store_url'] = environ.get('store_url')
        self.config['headless'] = environ.get('headless', True) == 'True'
        self.config['timeout'] = int(environ.get('timeout'))
        self.config['firefox_binary'] = environ.get('firefox_binary')
        self.config['geckodriver'] = environ.get('geckodriver')

    def read_from_config(self):
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        self.config['dropshipping_url'] = config_parser['DROPSHIPINFO']['url']
        self.config['dropshipping_login'] = config_parser['DROPSHIPINFO']['login']
        self.config['dropshipping_pass'] = config_parser['DROPSHIPINFO']['password']
        self.config['store_url'] = config_parser['STOREINFO']['url']

    def read_general_config(self):
        config_parser = ConfigParser()
        config_parser.read('config.ini')
        self.config['headless'] = config_parser.getboolean('GENERAL', 'headless')
        self.config['remove_files'] = config_parser.getboolean('GENERAL', 'removeFiles')
        self.config['output_file'] = config_parser['GENERAL']['outputFile']
        self.config['timeout'] = int(config_parser['GENERAL']['timeout'])

    config = {
        'dropshipping_url': 'url',
        'dropshipping_login': 'login',
        'dropshipping_pass': 'pass',
        'store_url': 'url',
        'headless': False,
        'remove_files': True,
        'output_file': 'output.csv',
        'timeout': 100
    }
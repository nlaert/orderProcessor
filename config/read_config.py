from os import environ
from configparser import ConfigParser


class ReadConfig:
    def __init__(self):
        super(ReadConfig, self).__init__()
        self.config = {}

    def read_configs(self):
        self.__read_from_env()
        if self.config['dropshipping_url'] is None:
            print("Could not read env data")
            self.read_from_config()
        return self.config

    def __read_from_env(self):
        self.config['dropshipping_url'] = environ.get('dropshipping.url')
        self.config['dropshipping_login'] = environ.get('dropshipping.login')
        self.config['dropshipping_pass'] = environ.get('dropshipping.pass')
        self.config['invoice.url'] = environ.get('invoice.url')
        self.config['invoice.login'] = environ.get('invoice.login')
        self.config['invoice.pass'] = environ.get('invoice.pass')
        self.config['headless'] = environ.get('headless', True) == 'True'
        
    def read_from_config(self):
        configParser = ConfigParser()
        configParser.read("config.ini")
        self.config["dropship_url"] = configParser["DROPSHIP_INFO"]["url"]
        self.config["dropship_login"] = configParser["DROPSHIP_INFO"]["login"]
        self.config["dropship_pass"] = configParser["DROPSHIP_INFO"]["password"]
        self.config["store_url"] = configParser["STORE_INFO"]["url"]
        self.config["store_login"] = configParser["STORE_INFO"]["login"]
        self.config["store_pass"] = configParser["STORE_INFO"]["password"]
        self.read_general_config(configParser)

    
    def read_general_config(self, configParser):
        self.config["headless"] = configParser.getboolean("GENERAL", "headless")
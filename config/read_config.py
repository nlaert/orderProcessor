from os import environ


class ReadConfig:
    def __init__(self):
        super(ReadConfig, self).__init__()
        self.config = {}

    def read_configs(self):
        self.__read_from_env()
        if self.config['dropshipping_url'] is None:
            print("Could not read env data")
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

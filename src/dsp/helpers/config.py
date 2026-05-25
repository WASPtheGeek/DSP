import pathlib


class ConfigHelper:
    def __init__(self, config_file: str | None = None):
        ''' Initialize the ConfigHelper with the path to the configuration file. '''
        if config_file is None:
            return
        
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        config = {}

        try:
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Configuration file '{self.config_file}' not found. Using default configuration.")

        return config

    def get(self, key, default=None):
        if self.config is None:
            return default
        
        return self.config.get(key, default)
    
    def get_root_dir(self):
        '''
        Get the root directory from the configuration.
        '''
        return pathlib.Path(__file__).resolve().parent.parent.parent.parent
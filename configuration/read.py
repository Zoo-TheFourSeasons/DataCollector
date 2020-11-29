import os

from configparser import ConfigParser


config = __file__
dir_path = os.path.dirname(os.path.dirname(config))

app_config = ConfigParser()
app_config.read('/'.join((os.path.dirname(config), r'configs.ini')))

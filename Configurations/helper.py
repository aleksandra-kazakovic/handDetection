import configparser

def read_bin_config():
    config = configparser.ConfigParser()
    config.read('Configurations/binConfigurations.ini')
    return config

def read_port_config():
    config = configparser.ConfigParser()
    config.read('Configurations/portConfigurations.ini')
    return config

def read_video_config():
    config = configparser.ConfigParser()
    config.read('Configurations/videoConfigurations.ini')
    return config
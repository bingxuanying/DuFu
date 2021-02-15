from configparser import ConfigParser

# Read config file
def getConfig():
    config = ConfigParser()
    config.read("./config/connect-soruce.config")
    return config
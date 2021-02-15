from configparser import ConfigParser

config = ConfigParser()

# Read config file
def getConfig():
    config.read("./config/system.config")
    return config

# Reset Broker Host in System Configration File
def reset():
    getConfig()
    config["BROKER"]["host"] = "none"
    with open('./config/connect-soruce.config', 'w') as configfile:
        config.write(configfile)

# Update Broker host and size
def updateBroker(host):
    getConfig()
    config["BROKER"]["host"] = str(host)
    config["BROKER"]["size"] = "1"
    with open('./config/connect-soruce.config', 'w') as configfile:
        config.write(configfile)


# Decrease given property's size by 1
def decreaseSize(topic):
    getConfig()
    currentSize = config[topic]["size"]
    config[topic]["size"] = str(int(currentSize) - 1)
    with open('./config/connect-soruce.config', 'w') as configfile:
        config.write(configfile)

# Increase given property's size by 1
def increaseSize(topic):
    getConfig()
    currentSize = config[topic]["size"]
    config[topic]["size"] = str(int(currentSize) + 1)
    with open('./config/connect-soruce.config', 'w') as configfile:
        config.write(configfile)
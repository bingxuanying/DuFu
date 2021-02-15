from configparser import ConfigParser
import json
from Utils import getConfig


class ClientUtils:
    def __init__(self):
        pass

    def getPort(self, name: str) -> str:
        config = getConfig()
        return config["PORTS"][name]
    
    def increaseClientSize(self):
        config = getConfig()
        currentSize = config["CLIENT"]["size"]
        config["CLIENT"]["size"] = str(int(currentSize) + 1)
        with open('./config/connect-soruce.config', 'w') as configfile:
            config.write(configfile)

    def decreaseClientSize(self):
        config = getConfig()
        currentSize = config["CLIENT"]["size"]
        config["CLIENT"]["size"] = str(int(currentSize) - 1)
        with open('./config/connect-soruce.config', 'w') as configfile:
            config.write(configfile)
    
    def tryReset(self):
        config = getConfig()
        # Reset config file on certain condition
        if config["CLIENT"]["size"] == "0" and config["BROKER"]["size"] == "0":
                config["BROKER"]["host"] = "none"
                with open('./config/connect-soruce.config', 'w') as configfile:
                    config.write(configfile)

    # Encode to Json
    def mogrify(self, topic, msg):
        # prepend topic and encode Json
        return str(topic) + ' ' + json.dumps(msg)

    # Convert Json to readable msg
    def demogrify(self, topicmsg):
        json0 = topicmsg.find('{')
        topic = topicmsg[0:json0].strip()
        msg = json.loads(topicmsg[json0:])
        return topic, msg
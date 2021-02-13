from configparser import ConfigParser
import json


class ClientUtils:
    portConfig = None

    def __init__(self):
        # Init portConfig
        self.portConfig = ConfigParser()
        self.portConfig.read("../../config/connect-soruce.config")

    def getPort(self, name: str) -> str:
        return self.portConfig["port"][name]

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
from configparser import ConfigParser


class SubscriberConfig:
    hasBroker = None
    isDebug = False
    portConfig = None

    def __init__(self, hasBroker, isDebug=False):
        # Init portConfig
        self.portConfig = ConfigParser()
        self.portConfig.read("../../../config/connect-soruce.config")

        # Config if the applicaiton needs broker
        self.hasBroker = hasBroker

        # Config if in Debug mode
        self.isDebug = isDebug

    def getPort(self, name: str) -> str:
        return self.portConfig["port"][name]

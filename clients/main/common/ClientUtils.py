from configparser import ConfigParser


class ClientUtils:
    portConfig = None

    def __init__(self):
        # Init portConfig
        self.portConfig = ConfigParser()
        self.portConfig.read("../../config/connect-soruce.config")

    def getPort(self, name: str) -> str:
        return self.portConfig["port"][name]

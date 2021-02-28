from common import *

class SubscriberConfig(ClientConfig):
    clientId = None
    zookeeperConnectionURL = None
    zookeeperConnectionTimeout = None

    def __init__(self, isDebug):
        ClientConfig.__init__(self, "sub", isDebug)

        # Copy the subset of properties
        props = self.configParser.read("./config/subscriber.config")
        self.zookeeperConnectionURL = props["service_discovery"]["connect"]
        self.zookeeperConnectionTimeout = props["service_discovery"]["connection.timeout.ms"]

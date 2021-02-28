from common import *

class PublisherConfig(ClientConfig):
    clientId = None
    port = None
    zookeeperConnectionURL = None
    zookeeperConnectionTimeout = None

    def __init__(self, isDebug):
        ClientConfig.__init__(self, "pub", isDebug)
        props = self.configParser.read("./config/publisher.config")

        # Copy the subset of properties
        self.port = props["publisher"]["port.pub"]
        self.zookeeperConnectionURL = props["service_discovery"]["connect"]
        self.zookeeperConnectionTimeout = props["service_discovery"]["connection.timeout.ms"]

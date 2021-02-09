import socket
from Leader import Leader


class Node:
    id = None
    host = None
    leader = None
    role = None
    publisherConfig = None

    def __init__(self, publisherConfig):
        # Get current host ip
        host_name = socket.gethostname()
        self.host = socket.gethostbyname(host_name)

        # Init publisherConfig
        self.publisherConfig = publisherConfig

        # Config leader as self
        self.leader = Leader(self.host, self.publisherConfig)

    def startLeaderConfig(self, mqSkt):
        if self.leader.findLeaderPublisher(mqSkt):
            print("(exist) Finish setup Leader")
            # TODO: self.leader.connectToLeader(self.host, mqSkt)
            self.role = "follower"
        else:
            print("(NOT exist) Create Leader")
            self.leader.createLeaderPublisher(self.host)
            self.role = "leader"

        return self.leader.getLookUpTable()

import socket
from Leader import Leader


class Node:
    id = None
    host = None
    leader = None
    role = None

    def __init__(self):
        # Get current host ip
        host_name = socket.gethostname()
        self.host = socket.gethostbyname(host_name)

        # Config leader as self
        self.leader = Leader(self.host)

    def startLeaderConfig(self, mqSkt, publisherConfig):
        print("[SETUP] Establishing connection with Publisher Leader ...")
        if self.leader.findLeaderPublisher(mqSkt, publisherConfig):
            ("(exist) Finish setup Leader.")
            self.role = "follower"
        else:
            ("(NOT exist) Create Leader.")
            self.leader.createLeaderPublisher(self.host)
            self.role = "leader"

        return self.leader.lookUpTable

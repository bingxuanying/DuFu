from Node import Node
from MQSocket import MQSocket


class Publisher:
    mqSkt = None
    node = Node()
    publisherConfig = None
    lookUpTable = None

    def __init__(self, publisherConfig):
        # Init publisherConfig
        self.publisherConfig = publisherConfig

        # Init MQ Socket
        self.mqSkt = MQSocket(self.publisherConfig)

        # Establish connection to Broker or Leader Publisher
        if self.publisherConfig.hasBroker:
            # TODO: connect to Broker
            pass
        else:
            # Init socket REQ and REP
            self.mqSkt.setupReq()
            self.mqSkt.setupRep()

            # Config Leader Publisher
            self.lookUpTable = self.node.startLeaderConfig(
                self.mqSkt, self.publisherConfig)

    def run(self):
        self.mqSkt.setupPub()

        while True:
            try:
                topic = input("Type TOPIC here: ")
                msg = input("Type MESSAGE here: ")
                print("[" + topic + "]: " + msg)
            except KeyboardInterrupt:
                print("Suicide successfully.")
                break
            # socks = dict(self.poller.poll())

            # try:
            #     # In this case, current publisher is NOT leader
            #     if self.sktSet["rep"] in socks and self.sktSet["rep"] == zmq.POLLIN:
            #         pass

            # except KeyboardInterrupt:
            #     print("Attemptting to suicide")
            #     # The leader try to suicide
            #     if self.metadata.host == self.metadata.leaderAddr:
            #         self.metadata.removeLUT(self.metadata.host)
            #         newLeader = random.choice(self.metadata.lookUpTable)
            #         # !! Check
            #         self.sktSet["dealer"].send_multipart(
            #             "NEW_LEADER " + newLeader)
            #         # TODO: notify all subscribers to disconnect

            #     # TODO: notify Leader

            #     print("Suicide successfully.")
            #     break

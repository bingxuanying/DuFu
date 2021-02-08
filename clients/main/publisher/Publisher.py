from zmq import backend
from Metadata import Metadata
import zmq
from configparser import ConfigParser
import random


class Publisher:
    clientId = None
    ctx = zmq.Context()
    sktSet = dict()
    poller = zmq.Poller()
    metadata = Metadata()
    publisherConfig = None
    portConfig = None

    def __init__(self, publisherConfig):
        self.publisherConfig = publisherConfig
        self.portConfig = ConfigParser()
        self.portConfig.read("../../../config/connect-soruce.config")

        if self.publisherConfig.hasBroker:
            self.__connectBroker()
        else:
            self.sktSet["req"] = self.ctx.socket(zmq.REQ)
            self.sktSet["rep"] = self.ctx.socket(zmq.REP)

            # Leader exist. Prepare to receive msg from Leader
            if self.metadata.findLeaderPublisher(self.sktSet):

                self.poller.register(self.sktSet["req"], zmq.POLLIN)
                self.poller.register(self.sktSet["rep"], zmq.POLLIN)
            # Leader does NOT exist. Make the current Publisher the Leader
            else:
                self.__turnLeader()

    # TODO: create the system with broker
    def __connectBroker(self):
        pass

    def __turnLeader(self):
        self.sktSet["router"] = self.ctx.socket(zmq.ROUTER)
        self.sktSet["dealer"] = self.ctx.socket(zmq.DEALER)
        self.sktSet["router"].bind(
            "tcp://*.{0000}".format(self.portConfig["port"]["router"]))
        self.sktSet["dealer"].bind(
            "tcp://*.{0001}".format(self.portConfig["port"]["dealer"]))

        self.poller.register(self.sktSet["router"], zmq.POLLIN)
        self.poller.register(self.sktSet["dealer"], zmq.POLLIN)

    def run(self):
        sktPUB = self.sktSet["pub"] = self.ctx.socket(zmq.PUB)
        port = self.portConfig["port"]["pub"]
        sktPUB.bind("tcp://*:" + port)

        while True:
            # try:
            #     topic = input("Type TOPIC here: ")
            #     msg = input("Type MESSAGE here: ")
            #     print("[" + topic + "]: " + msg)
            socks = dict(self.poller.poll())

            try:
                # In this case, current publisher is NOT leader
                if self.sktSet["rep"] in socks and self.sktSet["rep"] == zmq.POLLIN:
                    message = self.sktSet["rep"].recv()
                    print(message)
                    # !! received TYPE set
                    if type(message) == set:
                        # updated LUT is received
                        self.metadata.updateLUT(message)
                    else:
                        key, val = message.split(' ', 1)
                        if key == "NEW_LEADER":
                            self.sktSet["req"].disconnect(
                                "tcp://{0}:{0}".format(self.metadata.leaderAddr, self.portConfig["port"]["router"]))
                            self.sktSet["rep"].disconnect(
                                "tcp://{0}:{0}".format(self.metadata.leaderAddr, self.portConfig["port"]["dealer"]))

                            self.metadata.removeLUT(self.metadata.leaderAddr)
                            self.metadata.leaderAddr = val
                            if self.metadata.host == val:
                                self.__turnLeader()
                            else:
                                self.sktSet["req"].connect(
                                    "tcp://{0}:{0}".format(val, self.portConfig["port"]["router"]))
                                self.sktSet["rep"].connect(
                                    "tcp://{0}:{0}".format(val, self.portConfig["port"]["dealer"]))

                # In this case, current publisher is leader
                if self.sktSet["router"] in socks and self.sktSet["router"] == zmq.POLLIN:
                    message = self.sktSet["router"].recv()
                    print(message)
                    key, val = message.split(' ', 1)
                    # When new publisher is instantiated, update look up table and notifyall
                    if key == "NEW":
                        self.metadata.addLUT(val)
                        # !! Send out the lookUpTable as TYPE set
                        self.sktSet["dealer"].send_multipart(
                            self.metadata.lookUpTable)
                        # TODO: notify all subscribers to connect

            except KeyboardInterrupt:
                print("Attemptting to suicide")
                # The leader try to suicide
                if self.metadata.host == self.metadata.leaderAddr:
                    self.metadata.removeLUT(self.metadata.host)
                    newLeader = random.choice(self.metadata.lookUpTable)
                    # !! Check
                    self.sktSet["dealer"].send_multipart(
                        "NEW_LEADER " + newLeader)
                    # TODO: notify all subscribers to disconnect

                # TODO: notify Leader

                print("Suicide successfully.")
                break

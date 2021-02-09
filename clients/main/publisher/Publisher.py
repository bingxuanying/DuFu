from Node import Node
from MQSocket import MQSocket
import zmq
import random


class Publisher:
    mqSkt = None
    node = None
    publisherConfig = None

    def __init__(self, publisherConfig):
        print("[SETUP] Publisher initializing ...")
        # Init publisherConfig
        self.publisherConfig = publisherConfig

        # Init Socket with ZMQ
        self.mqSkt = MQSocket(self.publisherConfig)

        # Init Node
        self.node = Node(self.publisherConfig)

        # Establish connection to Broker or Leader Publisher
        if self.publisherConfig.hasBroker:
            print("[SETUP] Establishing connection with Broker ...")
            # TODO: connect to Broker
            pass
        else:
            # Init socket REQ and REP
            print("[SETUP] Setup REQ socket ...")
            self.mqSkt.setupReq()

            # Config Leader Publisher
            print("[SETUP] Establishing connection with existing Publisher ...")
            self.node.establishConnection(self.mqSkt)

    def run(self):
        self.mqSkt.setupPub()
        self.mqSkt.setupRep()
        sktRep, sktPub = self.mqSkt.getRep(), self.mqSkt.getPub()
        while True:
            try:
                messege = sktRep.recv_pyobj()
                sktRep.send_pyobj(["ACK", ""])

                if type(messege) == list:
                    key = messege[0]
                    body = messege[1]
                    if key == "JOIN":
                        sktPub.send_pyobj([key, body])
                        print("Notified SUBs join " + body)

            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
                self.exit()
                break

    def exit(self):
        sktPub = self.mqSkt.getPub()
        sktPub.send_pyobj(["LEAVE", self.node.host])
        print("[EXIT] Suicide success.")

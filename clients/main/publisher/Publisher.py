from common import *
from Node import Node
import zmq


class Publisher:
    mqSkt = MQSocket()
    node = Node()
    config = None

    def __init__(self, config):
        print("[SETUP] Publisher initializing ...")
        # Init config
        self.config = config

        # Establish connection to Broker or Leader Publisher
        if self.config.ifBroker:
            print("[SETUP] Establishing connection with Broker ...")
            # TODO: connect to Broker
            pass
        else:
            # Init socket REQ and REP
            print("[SETUP] Setup REQ/REP/PUB sockets ...")
            self.mqSkt.setupReq()
            self.mqSkt.setupRep()
            self.mqSkt.setupPub()

            # Config Leader Publisher
            print("[SETUP] Establishing connection with existing Publisher ...")
            self.node.establishConnection(self.mqSkt)

    def run(self):
        sktRep, sktPub = self.mqSkt.getRep(), self.mqSkt.getPub()
        poller = self.mqSkt.getPoller()
        while True:
            try:
                socks = dict(poller.poll(100))
                if sktRep in socks and socks.get(sktRep) == zmq.POLLIN:
                    messege = sktRep.recv_pyobj()
                    if type(messege) == list:
                        key = messege[0]
                        body = messege[1]
                        if key == "JOIN":
                            sktPub.send_pyobj([key, body])
                            print("Notified SUBs join " + body)
                    sktRep.send_pyobj(["ACK", ""])

                sktPub.send_pyobj(["test", self.node.host])

            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
                self.exit()
                break

    def exit(self):
        sktPub = self.mqSkt.getPub()
        sktPub.send_pyobj(["LEAVE", self.node.host])
        print("[EXIT] Suicide success.")

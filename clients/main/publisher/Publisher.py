from Node import Node
from MQSocket import MQSocket
import zmq
import random
import time


class Publisher:
    mqSkt = None
    node = None
    publisherConfig = None
    lookUpTable = set()

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
            self.lookUpTable = self.node.establishConnection(self.mqSkt)

    def run(self):
        self.mqSkt.setupPub()
        self.mqSkt.setupRep()
        sktRep, poller = self.mqSkt.getRep(), self.mqSkt.getPoller()
        while True:
            # try:
            #     topic = input("Type TOPIC here: ")
            #     msg = input("Type MESSAGE here: ")
            #     print("[" + topic + "]: " + msg)
            # except KeyboardInterrupt:
            #     print("Suicide successfully.")
            #     break
            try:
                messege = sktRep.recv_string()
                print(messege)
                time.sleep(1)
                sktRep.send_string("Ack")
                # socks = dict(poller.poll(500))
                # if sktRep in socks and sktRep == zmq.POLLIN:
                #     message = sktRep.recv_pyobj()
                #     sktRep.send(b"Ack")
                #     # !! Check if res is TYPE set
                #     # if self.publisherConfig.isDebug:
                #     print(type(message))
                #     if type(message) == type(list):
                #         for idx, item in enumerate(message):
                #             print(type(item) + " " + idx + " " + item)

            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide")
                self.exit()
                break

    def exit(self):
        # The leader try to suicide
        if self.node.role == "leader" and len(self.lookUpTable) > 1:
            self.lookUpTable.remove(self.node.host)
            newLeader = random.choice(self.lookUpTable)
            print("New Leader: " + newLeader)

            # !! Check
            # TODO: notify all subscribers to disconnect

        # TODO: notify Leader
        print("[EXIT] Suicide success.")

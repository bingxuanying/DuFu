from common import *
from SubNode import SubNode


class Subscriber:
    mqSkt = MQSocket()
    node = SubNode()
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
            print("[SETUP] Setup SUB socket ...")
            self.mqSkt.setupSub()

            # Config Leader Publisher
            print("[SETUP] Establishing connection with existing Publisher ...")
            self.node.subscribe(self.mqSkt)

    def run(self):
        sktSub = self.mqSkt.getSub()
        sktSub.subscribe('')

        # topicLst = []
        # while True:
        #     topic = input(
        #         "Enter topics to subscribe (TYPE 'DONE' when finish): ")
        #     if topic == "DONE":
        #         break
        #     topicLst.append(topic)

        while True:
            try:
                message = sktSub.recv_pyobj()
                print(message)
            except KeyboardInterrupt:
                print("interrupted")
                break

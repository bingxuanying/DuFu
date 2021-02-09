from MQSocket import MQSocket
from Node import Node
import zmq


class Subscriber:
    mqSkt = None
    node = None
    subscriberConfig = None

    def __init__(self, subscriberConfig):
        print("[SETUP] Publisher initializing ...")
        # Init subscriberConfig
        self.subscriberConfig = subscriberConfig

        # Init Socket with ZMQ
        self.mqSkt = MQSocket(self.subscriberConfig)

        # Init Node
        self.node = Node(self.subscriberConfig)

        # Establish connection to Broker or Leader Publisher
        if self.subscriberConfig.hasBroker:
            print("[SETUP] Establishing connection with Broker ...")
            # TODO: connect to Broker
            pass
        else:
            # Init socket REQ and REP
            print("[SETUP] Setup REQ socket ...")
            self.mqSkt.setupSub()

            # Config Leader Publisher
            print("[SETUP] Establishing connection with existing Publisher ...")
            self.node.subscribe(self.mqSkt)

    def run(self):
        sktSub = self.mqSkt.getSub()
        while True:
            try:
                message = sktSub.recv_pyobj()
                print(message)
            except KeyboardInterrupt:
                print("\ninterrupted")
                break

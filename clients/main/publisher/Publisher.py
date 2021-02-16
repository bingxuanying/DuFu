from os import times
from common import *
import zmq
from random import randrange
from datetime import datetime


class Publisher:
    mqSkt = MQSocket()
    node = Node()
    config = None
    utils = ClientUtils()

    def __init__(self, config):
        print("[SETUP] Publisher initializing ...")
        # Init config
        self.config = config

        # Setup Socket as PUB
        print("[SETUP] Setup PUB sockets ...")
        self.mqSkt.setupPub()

        # Establish connections
        self.connect()

        # Increase client size by 1
        self.utils.increaseClientSize()

    def run(self):
        print("Local IP Addr: " + self.node.host)
        # poller = self.mqSkt.getPoller()

        while True:
            try:
                zipcode = randrange(10000, 100000)
                body = {
                    "temperature": randrange(-80, 135),
                    "relhumidity": randrange(10, 60),
                    "timestamp": datetime.now().strftime(self.config.timeFormat)
                }

                self.publish(zipcode, body)

            # User Exit
            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
                self.exit()
                break

    def exit(self):
        sktPub = self.mqSkt.getPub()
        msg = {
            "host": self.node.host
        }
        sktPub.send_string(self.utils.mogrify("LEAVE", msg))

        # Decrease client size by 1
        self.utils.decreaseClientSize()
        # Check if config file needs to be reset
        self.utils.tryReset()
        print("[EXIT] Publisher suicide success.")

    """
    **Connect to broker
    """
    def connect(self):
        sktPub = self.mqSkt.getPub()
        # Connect to Broker
        if self.config.ifBroker:
            brokerHost = self.utils.getBrokerHost()
            port = self.utils.getPort('broker_xsub')
            addr = "tcp://{0}:{1}".format(brokerHost, port)
            print("[SETUP] Connecting o Broker at {0} ...".format(addr))
            sktPub.connect(addr)
        # Bind to all hosts
        else:
            print("[SETUP] Binding to all hosts ...")
            sktPub.bind(
                "tcp://*:{0}".format(self.utils.getPort("pub")))
    
    """
    **Publish messages
    @param topic + message in Json format
    """
    def publish(self, topic, body):
        sktPub = self.mqSkt.getPub()
        outMsg = self.utils.mogrify(topic, body)
        # outMsg = self.utils.mogrify("11100", body)

        # Debug Mode
        if self.config.isDebug:
            print(outMsg)

        sktPub.send_string(outMsg)
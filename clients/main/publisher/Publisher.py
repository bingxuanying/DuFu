from os import path
import sys
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(path.dirname(currentdir))
sys.path.append(path.join(parentdir, "main"))

from argparse import ArgumentParser
from random import randrange
from datetime import datetime

from PublisherSockets import PublisherSockets
from common import *


class Publisher:
    socks = None
    node = None
    zk_client = None
    serializer = None
    show_data = None
    broker_mode = None

    def __init__(self, show_data:bool=False, broker_mode:bool=True):
        print("[SETUP/PUB] Initialize the publisher ...")

        # Check if show message when tranfer
        self.show_data = show_data

        # Init broker mode
        self.broker_mode = broker_mode
        
        # Init publisher configuration
        self.node = Node("publisher")
        
        # Init sockets
        self.socks = PublisherSockets()

        # Init publisher configuration
        
        self.zk_client = ZookeeperBrokerManager(self.node.role) if self.broker_mode \
            else ZookeeperNonBrokerManager(self.node.role)

        # Init serializer
        self.serializer = Serializer()


    # Check if the publisher is startable
    def startable(self):
        print("[SETUP/PUB] Check if startable ...")

        # Check if ZK Client is ready (error free)
        # Check if config correctly
        # Start if precheck doesn't raise any error
        if self.zk_client.ready() and self.node.ready():
            print("[SETUP/PUB] Establish connections ...")
            self.connect()
            self.run()


    # Connect to service discovery server (ZooKeeper)
    def connect(self):
        if self.broker_mode:
            self.zk_client.startup(self.socks.connect, self.socks.disconnect)
        else:
            self.socks.bind()
            self.zk_client.publisher_connect(self.node.role, self.node.id, self.node.host)


    # Run publisher instance to produce data
    def run(self):
        print("[RUN] Build Success. Runs on: " + self.node.host)
        print("[RUN] Start publishing messages ... ")

        while True:
            try:
                # Randomly produce zipcode and data
                zipcode = randrange(10000, 100000)
                # zipcode = 22200
                body = {
                    "temperature": randrange(-80, 135),
                    "relhumidity": randrange(10, 60),
                    "timestamp": datetime.now().strftime(self.node.time_format)
                }
                # Send message
                self.publish(zipcode, body)

            # User exits
            except KeyboardInterrupt:
                self.exit()
                break


    # Terminate publisher instance
    def exit(self):
        print("[EXIT] Terminate Publisher ...")

        # Disconnect from service discovery server (ZooKeeper)
        self.zk_client.exit()

        print("[EXIT] Closed")
    

    # Publish messages
    # @param topic + message in Json format
    def publish(self, topic, body):
        pub_sock = self.socks.get_pub()
        msg = self.serializer.json_mogrify(topic, body)
        pub_sock.send_string(msg)

        if self.show_data:
            print(msg)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-s", "--show", 
                            help="console log data being received or sent", 
                            dest="show", action="store_true", default=False)

    parser.add_argument("-b", "--broker", 
                            help="console log data being received or sent", 
                            dest="broker", action="store_true", default=False)

    args = parser.parse_args()

    Publisher(args.show, args.broker).startable()
from random import randrange
from datetime import datetime
from .PublisherSockets import PublisherSockets
from .PublisherConfig import PublisherConfig
from common import *


class Publisher:
    socks = None
    config = None
    zk_client = None
    serializer = None

    def __init__(self, debug_mode):
        print("[SETUP/PUB] Initialize the publisher ...")
        # Init sockets
        self.socks = PublisherSockets()

        # Init publisher configuration
        self.config = PublisherConfig(debug_mode)
        
        # Init publisher configuration
        self.zk_client = ZKClient(self.config.role)

        # Init serializer
        serializer = Serializer()

        print("[SETUP/PUB] Establish connections ...")
        # TODO: Establish connections
        self.connect()


    # Check if the publisher is startable
    def startable(self):
        print("[SETUP/PUB] Check if startable ...")

        # Check if ZK Client is ready (error free)
        # Check if config correctly
        # Start if precheck doesn't raise any error
        if self.zk_client.ready() and self.config.ready():
            self.connect()
            self.run()


    # Run publisher instance to produce data
    def run(self):
        print("[RUN] Build Success. Runs on: " + self.config.host)
        print("[RUN] Start publishing messages ... ")

        while True:
            try:
                # Randomly produce zipcode and data
                zipcode = randrange(10000, 100000)
                body = {
                    "temperature": randrange(-80, 135),
                    "relhumidity": randrange(10, 60),
                    "timestamp": datetime.now().strftime(self.config.timeFormat)
                }
                # Send message
                self.publish(zipcode, body)
                print(zipcode)
                print(body)
                print('')

            # User exits
            except KeyboardInterrupt:
                self.exit()

            finally:
                break


    # Terminate publisher instance
    def exit(self):
        print("[EXIT] Terminate Publisher ...")
        self.zk_client.exit()


    # Connect to service discovery server (ZooKeeper)
    def connect(self):
        self.zk_client.startup(self.socks.connect, self.socks.disconnect)
    

    # Publish messages
    # @param topic + message in Json format
    def publish(self, topic, body):
        pubSkt = self.socks.getPub()
        msg = self.serializer.JsonMogrify(topic, body)

        # Debug Mode
        if self.config.isDebug:
            print(msg)

        pubSkt.send_string(msg)
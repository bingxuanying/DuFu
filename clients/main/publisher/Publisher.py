from random import randrange
from datetime import datetime
import zmq
from common import *


class Publisher:
    socks = ClientSockets()
    config = None
    serializer = Serializer()

    def __init__(self, config):
        print("[SETUP] Initialize a publisher instance ...")
        # Init publisher configuration
        self.config = PublisherConfig(isDebug)

        # Init Socket PUB
        print("[SETUP] Create PUB socket ...")
        self.socks.setPub()

        print("[SETUP] Connect to Service Discovery Server ...")
        # TODO: Establish connections
        self.connect()


    """
    **Start running the current subscriber and listening to ports
    """
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

            # User Exit
            except KeyboardInterrupt:
                print("[EXIT] Attemptting to terminate ...")
                self.exit()
                break


    """
    **Terminate the current publisher instance
    """    
    def exit(self):
        # TODO: Notify and disconnect from service discovery server (ZooKeeper)
        print("[EXIT] Publisher is terminated.")


    """
    TODO: **Connect to service discovery server (ZooKeeper)
    """
    def connect(self):
        pubSkt = self.socks.getPub()
        # # Connect to Broker
        # if self.config.ifBroker:
        #     addr = "tcp://{0}:{1}".format(brokerHost, port)
        #     print("[SETUP] Connecting o Broker at {0} ...".format(addr))
        #     pubSkt.connect(addr)
        # # Bind to all hosts
        # else:
        #     print("[SETUP] Binding to all hosts ...")
        #     pubSkt.bind(
        #         "tcp://*:{0}".format(self.utils.getPort("pub")))
    

    """
    **Publish messages
    @param topic + message in Json format
    """
    def publish(self, topic, body):
        pubSkt = self.socks.getPub()
        msg = self.serializer.JsonMogrify(topic, body)

        # Debug Mode
        if self.config.isDebug:
            print(msg)

        pubSkt.send_string(msg)
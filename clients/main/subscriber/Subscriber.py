from datetime import datetime
import zmq
from common import *


class Subscriber:
    socks = ClientSockets()
    config = None
    serializer = Serializer()
    records = None
    subscription = None

    def __init__(self, isDebug):
        print("[PRE] Subscribe to topics ...")
        # Let user type zipcodes they want to subscribe
        self.subscription = Subscription()

        print("[SETUP] Initialize a subscriber instance ...")
        # Init subscriber configuration
        self.config = SubscriberConfig(isDebug)

        # Init socket SUB
        print("[SETUP] Create SUB socket ...")
        self.socks.setSub()

        print("[SETUP] Begin recording incoming data ...")
        # Init data plot instance
        self.records = SubscriberRecords(self.config.host)

        print("[SETUP] Connect to Service Discovery Server ...")
        # TODO: Establish connections
        self.connect()


    """
    **Start running the current subscriber and listening to ports
    """
    def run(self):
        print("[RUN] Build Success. Runs on: " + self.config.host)
        print("[RUN] Start publishing messages ... ")

        # Acquire sockets and poller
        subSkt = self.socks.getSub()
        poller = self.socks.getPoller()
        
        # Main loop for receiving messages
        while True:
            try:
                pollerSocks = dict(poller.poll(100))
                if subSkt in pollerSocks and pollerSocks.get(subSkt) == zmq.POLLIN:
                    message = subSkt.recv_string()
                    transmissionTime = self.notify(message)
                    self.records.add(transmissionTime)
    
            # User Exit
            except KeyboardInterrupt:
                print("[EXIT] Attempt to terminate ...")
                self.exit()
                break


    """
    **Terminate the current subscriber instance
    """    
    def exit(self):
        # Create data graph
        self.records.createLinePlot()
        # TODO: Notify and disconnect from service discovery server (ZooKeeper)
        print("[EXIT] Subscriber is terminated.")


    """
    TODO: **Connect to service discovery server (ZooKeeper)
    @param 
    """    
    def connect(self):
        subSkt = self.socks.getSub()
    

    """
    **Unpack and process the receiving message
    @param message
    @return transmissionTime: Time it takes to receve the message
    """    
    def notify(self, message):
        topic, body = self.serializer.JsonDemogrify(message)

        if self.config.isDebug:
            print("topic: " + topic)
            for k in body:
                print(str(k) + ": " + str(body[k]))

        startTime = datetime.strptime(body["timestamp"], self.config.timeFormat)
        endTime = datetime.now()
        timeDiff = (endTime - startTime)
        transmissionTime = timeDiff.total_seconds()

        if self.config.isDebug:
            print("Transmission time = ", transmissionTime)
            print("")
        
        return transmissionTime
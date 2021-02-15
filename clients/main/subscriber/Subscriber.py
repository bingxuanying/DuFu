from datetime import datetime
from common import *
import zmq


class Subscriber:
    mqSkt = MQSocket()
    node = Node()
    config = None
    utils = ClientUtils()

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
            self.connect()

        # Increase client size by 1
        self.utils.increaseClientSize()

    def run(self):
        print("Local IP Addr: " + self.node.host)

        # Acquire sockets and poller
        sktSub = self.mqSkt.getSub()
        poller = self.mqSkt.getPoller()


        # Allow user choose what to subscribe
        while True:
            topic = input("Enter zipcode you want to subscribe (enter DONE when finish): ")
            # Leave if DONE
            if topic == "DONE" or topic == "done":
                break

            # Make sure user enters valid zipcode
            if len(topic) == 5 and topic.isnumeric():
                sktSub.subscribe(topic)
                print("Subscribe Success!")
            else:
                print("Please enter valid zipcode:)")
        
        print("Start Listening ...")

        # Main loop for receiving messages
        while True:
            try:
                socks = dict(poller.poll(100))
                if sktSub in socks and socks.get(sktSub) == zmq.POLLIN:
                    message = sktSub.recv_string()
                    t, m = self.utils.demogrify(message)

                    if self.config.isDebug:
                        print("topic: " + t)
                        for k in m:
                            print(str(k) + ": " + str(m[k]))

                    startTime = datetime.strptime(m["timestamp"], self.config.timeFormat)
                    endTime = datetime.now()
                    timeDiff = (endTime - startTime)
                    execTime = timeDiff.total_seconds()
                    if self.config.isDebug:
                        print(endTime, " - ", startTime, " = ", execTime)
                    
                    print("")
    
            # User Exit
            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
                self.exit()
                break

    def exit(self):
        # Decrease client size by 1
        self.utils.decreaseClientSize()
        # Check if config file needs to be reset
        self.utils.tryReset()
        print("[EXIT] Subscriber suicide success.")

    def connect(self):
        sktSub = self.mqSkt.getSub()

        # Connect to Broker
        if self.config.ifBroker:
            print("[SETUP] Establishing connection with Broker ...")
            brokerHost = self.utils.getBrokerHost()
            port = self.utils.getPort('broker_xpub')
            addr = "tcp://{0}:{1}".format(brokerHost, port)
            sktSub.connect(addr)
        # Flood through internet
        else:
            print("[SETUP] Flooding through internet to connect ...")
            masked = self.node.host.rpartition('.')[0]
            port = self.utils.getPort('pub')

            # Flood through internet
            for last in range(1, 256):
                addr = "tcp://{0}.{1}:{2}".format(masked, last, port)
                sktSub.connect(addr)
    
    def notify(self, topic, message):
        if self.config.isDebug:
            print("topic: " + topic)
            for k in message:
                print(str(k) + ": " + str(message[k]))

        startTime = datetime.strptime(message["timestamp"], self.config.timeFormat)
        endTime = datetime.now()
        timeDiff = (endTime - startTime)
        execTime = timeDiff.total_seconds()

        if self.config.isDebug:
            print(endTime, " - ", startTime, " = ", execTime)
                    
        print("")
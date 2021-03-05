from datetime import datetime
import zmq

from .SubscriberSockets import SubscriberSockets
from .SubscriberRecords import SubscriberRecords
from .Subscription import Subscription
from common import *


class Subscriber:
    socks = None
    node = None
    zk_client = None
    serializer = None
    records = None
    subscription = None
    show_data = None

    def __init__(self, show_data:bool=False, broker_mode:bool=True):
        print("[PRE] Subscribe to topics ...")

        # Let user type zipcodes they want to subscribe
        self.subscription = Subscription()

        # Check if show message when tranfer
        self.show_data = show_data

        # Init broker mode
        self.broker_mode = broker_mode

        print("[SETUP/SUB] Initialize the subscriber ...")

        # Init subscriber configuration
        self.node = Node("subscriber")
        
        # Init sockets
        self.socks = SubscriberSockets()

        # Init subscriber configuration
        self.zk_client = ZookeeperBrokerManager(self.node.role) if self.broker_mode \
            else ZookeeperNonBrokerManager(self.node.role)

        # Init serializer
        self.serializer = Serializer()

        # Init data plot instance
        self.records = SubscriberRecords(self.node.host)


    # Check if the subscrber is startable
    def startable(self):
        print("[SETUP/SUB] Check if startable ...")

        # Check if ZK Client is ready (error free)
        # Check if config correctly
        # Start if precheck doesn't raise any error
        if self.zk_client.ready() and self.node.ready():
            print("[SETUP/SUB] Establish connections ...")
            self.connect()
            self.run()


    # Connect to service discovery server (ZooKeeper)
    def connect(self):
        if self.broker_mode:
            self.zk_client.startup(self.socks.connect, self.socks.disconnect)
        else:
            self.zk_client.subscriber_connect(self.node.role, self.socks.connect, self.socks.disconnect)


    # Run subscrber instance to receive data
    def run(self):
        print("[RUN] Build Success. Runs on: " + self.node.host)
        print("[RUN] Wait for incoming messages ... ")

        # Subscribe topics
        self.socks.subscribe(self.subscription.topics)

        # Acquire sockets and poller
        sub_sock = self.socks.get_sub()
        poller = self.socks.get_poller()
        
        # Main loop for receiving messages
        while True:
            try:
                events = dict(poller.poll(100))
                if sub_sock in events and events.get(sub_sock) == zmq.POLLIN:
                    message = sub_sock.recv_string()
                    transmission_time = self.notify(message)
                    self.records.add(transmission_time)
    
            # User exits
            except KeyboardInterrupt:
                self.exit()
                break


    # Terminate the current subscriber instance
    def exit(self):
        print("[EXIT] Terminate Subscriber ...")

        # Create data graph
        self.records.create_line_plot()

        # Disconnect from service discovery server (ZooKeeper)
        self.zk_client.exit()

        print("[EXIT] Closed")
    

    # Unpack and process the receiving message
    # @param message
    # @return transmission_time: Time it takes to receve the message
    def notify(self, message):
        # Deserialize messages
        topic, body = self.serializer.json_demogrify(message)

        # Calculate transmission time
        start_time = datetime.strptime(body["timestamp"], self.node.time_format)
        end_time = datetime.now()
        time_diff = (end_time - start_time)
        transmission_time = time_diff.total_seconds()

        if self.show_data:
            print("topic: " + topic)
            for k in body:
                print(str(k) + ": " + str(body[k]))
            print("Transmission time = ", transmission_time)
            print("")
        
        return transmission_time
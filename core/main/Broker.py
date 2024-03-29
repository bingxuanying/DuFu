import uuid
import netifaces
import sys
from collections import defaultdict 
from ServerSockets import ServerSockets


class Broker:
    id = None
    host = None
    socks = None
    subscription = defaultdict(int)
    show_data = None


    def __init__(self, show_data:bool=False):
        # Set server id
        self.id = str(uuid.uuid4())

        # Check if show message when tranfer
        self.show_data = show_data
        
        # Init host address
        self._init_host_addr()

        # Start Sockets XPUB and XSUB
        print("[SETUP/BROKER] Init broker sever sockets ...")
        self.socks = ServerSockets()
    

    # Init host ip address
    def _init_host_addr(self):
        name_lst = netifaces.interfaces()
        for name in name_lst:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
    

    # Run the broker instance
    def run(self):
        print ("[RUN] Runing ...")

        # Acquire sockets and poller
        xsub_sock = self.socks.get_xsub()
        xpub_sock = self.socks.get_xpub()
        poller = self.socks.get_poller()

        # Subscribe with publishers
        self.xSubscribe("")

        while True:
            try:
                events = dict(poller.poll(1000))
                # From subscribers
                if xpub_sock in events:
                    message = xsub_sock.recv()
                    if self.show_data:
                        print(message)

                # From publishers
                if xsub_sock in events:
                    message = xsub_sock.recv_string()
                    if self.show_data:
                        print(message)

                    xpub_sock.send_string(message)

            except KeyboardInterrupt:
                self.exit()
    

    # Terminate the  broker
    def exit(self):
        print("[EXIT] Terminate broker ...")
        raise KeyboardInterrupt
    

    # Check if ready
    def ready(self):
        if not self.id:
            sys.exit("[ERR] NO valid server id.")
        elif not self.host:
            sys.exit("[ERR] NO valid host ip address.")
        
        return True


    # Subscribe topics with publishers
    # @return topic
    def xSubscribe(self, topic):
        xsub_sock = self.socks.get_xsub()
        zipcode = topic.encode("utf-8")
        message = b'\x01' + bytearray(zipcode)
        xsub_sock.send(message)
        # print("subscribed: " + topic)
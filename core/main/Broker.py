from collections import defaultdict 
from .ServerSockets import ServerSockets


class Broker:
    socks = None
    subscription = defaultdict(int)


    def __init__(self):
        # Start Sockets XPUB and XSUB
        print("[SETUP/BROKER] Init broker sever sockets ...")
        self.socks = ServerSockets()
    

    # Run the broker instance
    def run(self):
        print ("[RUN] Runing ...")

        # Acquire sockets and poller
        xsub_sock = self.socks.get_xsub()
        xpub_sock = self.socks.get_xpub()
        poller = self.socks.get_poller()

        # TODO: subscribe with publishers
        self.xSubscribe("")

        while True:
            try:
                socks = dict(poller.poll(1000))

                # !! if self.isDebug:
                    # print ("Events received = {}".format (socks))

                # From publishers
                if xsub_sock in socks:
                    message = xsub_sock.recv_string()
                    print(message)
                    # !! topic, message = self.utils.demogrify(message)

                    # !! if self.isDebug:
                        # print("topic: " + topic)
                        # for key in message:
                        #     print(str(key) + ": " + str(message[key]))

                    xpub_sock.send_string(message)

            except KeyboardInterrupt:
                self.exit()
    

    # Terminate the  broker
    def exit(self):
        # TODO: Unsubscriber from publishers
        print("[EXIT] Terminate broker ...")
        raise KeyboardInterrupt
    

    # Subscribe topics with publishers
    # @return topic
    def xSubscribe(self, topic):
        xsub_sock = self.socks.get_xsub()
        zipcode = topic.encode("utf-8")
        message = b'\x01' + bytearray(zipcode)
        xsub_sock.send(message)
        print("subscribed: " + topic)
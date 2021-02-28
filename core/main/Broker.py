import sys
import zmq
from collections import defaultdict 

from ServerSockets import ServerSockets


class Broker:
    socks = ServerSockets()

    def __init__(self, isDebug=True):
        # Start Sockets XPUB and XSUB
        print("[SETUP] Start XPUB and XSUB socket ...")
        self.socks.startup()
    
    """
    **Start running the current broker
    """
    def run(self):
        # Acquire sockets and poller
        xSubSkt = self.socks.getXSub()
        xPubSkt = self.socks.getXPub()
        poller = self.socks.getPoller()

        # TODO: subscribe with publishers
        # !! self.xSubscribe("", xsub)

        print ("[SETUP] Done! Runing ...")
        while True:
            try:
                socks = dict(poller.poll(1000))

                # !! if self.isDebug:
                    # print ("Events received = {}".format (socks))

                # From publishers
                if xSubSkt in socks:
                    message = xSubSkt.recv_string()
                    # !! topic, message = self.utils.demogrify(message)

                    # !! if self.isDebug:
                        # print("topic: " + topic)
                        # for key in message:
                        #     print(str(key) + ": " + str(message[key]))

                    xPubSkt.send_string(message)

            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
    
    """
    **Terminate the current broker
    """
    def exit(self):
        # TODO: Notify and disconnect from service discovery server (ZooKeeper)
        print("[EXIT] Broker is terminated.")
    
    # """
    # ** Subscribe topics with publishers
    # @return topic
    # """
    # def xSubscribe(self, topic, xsub):
    #     zipcode = topic.encode("utf-8")
    #     message = b'\x01' + bytearray(zipcode)
    #     xsub.send(message)
    #     if self.isDebug:
    #         print("subscribed: " + topic)
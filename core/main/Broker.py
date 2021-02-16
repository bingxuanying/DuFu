import sys
import zmq
from collections import defaultdict 
import netifaces
import SysConfigUtils
from BrokerUtils import BrokerUtils


class Broker:
    host = None
    role = "broker"
    utils = BrokerUtils()
    subscription = defaultdict(list)
    isDebug = True

    def __init__(self, isDebug=True):
        # Check if debug mode is wanted:
        self.isDebug = isDebug

        # Get current host ip
        host_list = netifaces.interfaces()
        for name in host_list:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
        
        # Update system config if host ip set success
        if self.host:
            print("[SETUP] Broker host: " + self.host)
            SysConfigUtils.updateBroker(self.host)
        # Else raise ERROR
        else:
            raise Exception("Setting up broker host ERROR")
    
    """
    ** Execute when program start
    """
    def run(self):
        # Get the context
        context = zmq.Context()

        # This is a proxy. We create the XSUB and XPUB endpoints
        print ("[SETUP] Creating xsub and xpub sockets")
        xsub = context.socket(zmq.XSUB)
        xsub.bind("tcp://*:{0}".format(self.utils.getPort("broker_xsub")))

        xpub = context.socket (zmq.XPUB)
        xpub.setsockopt(zmq.XPUB_VERBOSE, 1)
        xpub.bind ("tcp://*:{0}".format(self.utils.getPort("broker_xpub")))

        # Now we are going to create a poller
        poller = zmq.Poller()
        poller.register(xsub, zmq.POLLIN)
        poller.register(xpub, zmq.POLLIN)

        self.xSubscribe("", xsub)
        print ("[SETUP] Done! Runing ...")
        while True:
            try:
                socks = dict(poller.poll(1000))

                if self.isDebug:
                    print ("Events received = {}".format (socks))

                # From subscribers
                if xpub in socks:
                    message = xpub.recv_string()
                    if self.isDebug:
                        print(message)
                    # t, m = self.utils.demogrify(message)
                    # t = t.replace(" ", "")

                    # if self.isDebug:
                    #     print("topic: " + t)

                    # if t == "SUBSCRIBE":
                    #     for k in m:
                    #         self.xSubscribe(m[k], xsub)

                # From publishers
                if xsub in socks:
                    message = xsub.recv_string()
                    t, m = self.utils.demogrify(message)

                    if self.isDebug:
                        print("topic: " + t)
                        for k in m:
                            print(str(k) + ": " + str(m[k]))

                    xpub.send_string(message)

            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
                if self.exit(): 
                    print("[EXIT] Broker suicide success.")
                    break
                else: 
                    print("[EXIT] Broker suicide fail. Conitune executing")
                    continue
    
    """
    ** Execute when exit
    @return true => exit success
            false => exit fail
    """
    def exit(self) -> bool:
        config = SysConfigUtils.getConfig()
        # If publishers and subscribers exits, refuse to close broker
        if int(config["CLIENT"]["size"]) > 0:
            print("[ERROR] Please close active publishers/subscribers first!")
            return False
        # If mutiple brokers exist, allow to close current one
        else:
            # Decrease broker size by 1
            SysConfigUtils.decreaseSize("BROKER")
            if int(config["BROKER"]["size"]) == 0:
                # Reset system config
                SysConfigUtils.reset()
            return True
    
    """
    ** Subscribe topics from publishers
    @return topic
    """
    def xSubscribe(self, topic, xsub):
        zipcode = topic.encode("utf-8")
        message = b'\x01' + bytearray(zipcode)
        xsub.send(message)
        if self.isDebug:
            print("subscribed: " + topic)
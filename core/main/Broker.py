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
    topicMap = defaultdict(list)

    def __init__(self):
        # Get current host ip
        host_list = netifaces.interfaces()
        for name in host_list:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
        
        # Update system config if host ip set success
        if self.host:
            SysConfigUtils.updateBroker(self.host)
        # Else raise ERROR
        else:
            raise Exception("Setting up broker host ERROR")
    
    """
    ** Execute when program start
    """
    def run(self):
        while True:
            try:
                ctx = zmq.Context()
                xpub = ctx.socket(zmq.XPUB)
                xpub.bind("tcp://*:{0}".format(self.utils.getPort("broker_xpub")))
                xsub = ctx.socket(zmq.XSUB)
                xsub.bind("tcp://*:{0}".format(self.utils.getPort("broker_xsub")))

                poller = zmq.Poller()
                poller.register(xpub, zmq.POLLIN)
                poller.register(xsub, zmq.POLLIN)
                while True:
                    socks = dict(poller.poll(100))
                    # From subscribers
                    if xpub in socks:
                        message = xpub.recv_string()
                        t, m = self.utils.demogrify(message)

                        print("topic: " + t)
                        for k in m:
                            print(str(k) + ": " + str(m[k]))
                            if k == "TOPIC":
                                self.topicMap[k].append(m[k])
                                print("ADDED")
                                print("")
                                
                        # xsub.send_string(message)

                    # From publishers
                    if xsub in socks:
                        message = xsub.recv_string()
                        t, m = self.utils.demogrify(message)

                        print("topic: " + t)
                        for k in m:
                            print(str(k) + ": " + str(m[k]))
                            if k == "TOPIC":
                                self.topicMap[k].append(m[k])
                                print("ADDED")
                                print("")

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
        # If mutiple brokers exist, allow to close current one
        if config["BROKER"]["size"] > 1:
            # Decrease broker size by 1
            SysConfigUtils.decreaseSize("BROKER")
            return True
        # If publishers and subscribers exits, refuse to close broker
        elif config["CLIENT"]["size"] > 0:
            print("[ERROR] Please close active publishers/subscribers first!")
            return False
        # Close everything
        else:
            # Reset system config
            SysConfigUtils.reset()
            return True

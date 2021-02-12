import netifaces
from common import *

class SubNode:
    id = None
    host = None
    utils = ClientUtils()

    def __init__(self):
        # Get current host ip
        host_list = netifaces.interfaces()
        for name in host_list:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break

        if self.host:
            print("host ip: " + self.host)

    def subscribe(self, mqSkt):
        sktSub = mqSkt.getSub()
        masked = self.host.rpartition('.')[0]
        port = self.utils.getPort('pub')

        # Connect to random Publisher
        for last in range(1, 256):
            addr = "tcp://{0}.{1}:{2}".format(masked, last, port)
            sktSub.connect(addr)

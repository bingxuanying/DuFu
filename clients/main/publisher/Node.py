import netifaces
from common import *


class Node:
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

    def establishConnection(self, mqSkt):
        sktReq = mqSkt.getReq()
        masked = self.host.rpartition('.')[0]
        port = self.utils.getPort('rep')

        # Connect to random Publisher
        for last in range(1, 256):
            if "{0}.{1}".format(masked, last) == self.host:
                continue
            addr = "tcp://{0}.{1}:{2}".format(masked, last, port)
            sktReq.connect(addr)

        # Ask randomly conneted Publisher to notify subscribers to connect
        sktReq.send_pyobj(["JOIN", self.host])

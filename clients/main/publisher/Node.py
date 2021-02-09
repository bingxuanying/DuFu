import netifaces
import zmq


class Node:
    id = None
    host = None
    publisherConfig = None

    def __init__(self, publisherConfig):
        # Init publisherConfig
        self.publisherConfig = publisherConfig

        # Get current host ip
        host_list = netifaces.interfaces()
        for name in host_list:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break

    def establishConnection(self, mqSkt):
        sktReq = mqSkt.getReq()
        masked = self.host.rpartition('.')[0] + '.'
        port = self.publisherConfig.getPort('rep')

        # Connect to random Publisher
        for last in range(1, 256):
            addr = "tcp://{0}.{1}:{0}".format(masked, last, port)
            sktReq.connect(addr)

        # Ask randomly conneted Publisher to notify subscribers to connect
        res = None
        sktReq.send_string("hello")

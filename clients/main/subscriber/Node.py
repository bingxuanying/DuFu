import netifaces


class Node:
    id = None
    host = None
    subscriberConfig = None

    def __init__(self, subscriberConfig):
        # Init subscriberConfig
        self.subscriberConfig = subscriberConfig

        # Get current host ip
        host_list = netifaces.interfaces()
        for name in host_list:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break

        print("host ip: " + self.host)

    def subscribe(self, mqSkt):
        sktSub = mqSkt.getSub()
        masked = self.host.rpartition('.')[0]
        port = self.subscriberConfig.getPort('pub')

        # Connect to random Publisher
        for last in range(1, 256):
            addr = "tcp://{0}.{1}:{2}".format(masked, last, port)
            sktSub.connect(addr)

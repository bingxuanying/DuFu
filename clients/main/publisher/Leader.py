import zmq


class Leader:
    host = None
    lookUpTable = set()

    def __init__(self, host):
        self.host = host

    def findLeaderPublisher(self, mqSkt, publisherConfig) -> bool:
        sktReq = mqSkt.getReq()
        masked = self.host.rpartition('.')[0] + '.'
        port = publisherConfig.getPort('rep')

        for last in range(1, 255):
            sktReq.connect(
                "tcp://{0}.{1}:{0}".format(masked, last, port))
            try:
                sktReq.send_string("NEW " + self.host)
                res = sktReq.recv(zmq.NOBLOCK)
                # !! Check if res is TYPE set
                # !! Check leader ip addr
                if res:
                    self.lookUpTable = res
                    self.leader = "{0}.{1}".format(masked, last)
                    return True
            except zmq.ZMQError:
                continue

        return False

    def createLeaderPublisher(self, host):
        self.host = host
        self.lookUpTable.add(host)

import zmq


class Leader:
    host = None
    lookUpTable = set()
    publisherConfig = None

    def __init__(self, host, publisherConfig):
        self.host = host

        # Init publisherConfig
        self.publisherConfig = publisherConfig

    def findLeaderPublisher(self, mqSkt) -> bool:
        sktReq = mqSkt.getReq()
        masked = self.host.rpartition('.')[0] + '.'
        port = self.publisherConfig.getPort('rep')

        res = None
        for last in range(1, 256):
            # looking for a random Publisher and retrieve Leader ip
            addr = "tcp://{0}.{1}:{0}".format(masked, last, port)
            sktReq.connect(addr)
            try:
                sktReq.send_pyobj(["LEADER"])
                res = sktReq.recv(zmq.NOBLOCK)

                # !! Check if res is TYPE set
                if self.publisherConfig.isDebug:
                    print(type(res))
                    if type(res) == type(list):
                        for item in res:
                            print(type(item))

                # Successfully get Leader ip
                if res:
                    # !! message type
                    self.leader = res
                    sktReq.disconnect(addr)
                    return True
            except zmq.ZMQError:
                continue
        return False

    def connectToLeader(self, localhost, mqSkt):
        sktReq = mqSkt.getReq()
        port = self.publisherConfig.getPort('rep')

        sktReq.connect("tcp://{0}:{0}".format(self.host, port))
        sktReq.send_string("NEW" + localhost)
        res = sktReq.recv()

        # !! Check if res is TYPE set
        if self.publisherConfig.isDebug:
            print(type(res))
            if type(res) == type(list):
                for item in res:
                    print(type(item))

        self.lookUpTable = res

    def createLeaderPublisher(self, host):
        self.host = host
        self.lookUpTable.add(host)

    def getLookUpTable(self):
        return self.lookUpTable

import zmq


class MQSocket:
    ctx = zmq.Context()
    sktSet = dict()
    poller = zmq.Poller()
    publisherConfig = None

    def __init__(self, publisherConfig):
        self.publisherConfig = publisherConfig

    def setupReq(self):
        self.sktSet["req"] = self.ctx.socket(zmq.REQ)

    def setupRep(self):
        self.sktSet["rep"] = self.ctx.socket(zmq.REP)
        self.sktSet["rep"].bind(
            "tcp://*:{0000}".format(self.publisherConfig.getPort("rep")))
        self.poller.register(self.sktSet["rep"], zmq.POLLIN)

    def setupSub(self):
        self.sktSet["sub"] = self.ctx.socket(zmq.SUB)
        self.poller.register(self.sktSet["sub"], zmq.POLLIN)

    def setupPub(self):
        self.sktSet["pub"] = self.ctx.socket(zmq.PUB)
        self.sktSet["pub"].bind(
            "tcp://*:{0000}".format(self.publisherConfig.getPort("pub")))

    def getReq(self):
        return self.sktSet["req"]

    def getRep(self):
        return self.sktSet["rep"]

    def getSub(self):
        return self.sktSet["sub"]

    def getPub(self):
        return self.sktSet["pub"]

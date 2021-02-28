import zmq


class ClientSockets:
    ctx = zmq.Context()
    socks = dict()
    poller = zmq.Poller()

    def __init__(self):
        pass

    def setReq(self):
        self.socks["req"] = self.ctx.socket(zmq.REQ)

    def setRep(self):
        self.socks["rep"] = self.ctx.socket(zmq.REP)
        self.poller.register(self.socks["rep"], zmq.POLLIN)

    def setSub(self):
        self.socks["sub"] = self.ctx.socket(zmq.SUB)
        self.poller.register(self.socks["sub"], zmq.POLLIN)

    def setPub(self):
        self.socks["pub"] = self.ctx.socket(zmq.PUB)

    def getReq(self):
        return self.socks["req"]

    def getRep(self):
        return self.socks["rep"]

    def getSub(self):
        return self.socks["sub"]

    def getPub(self):
        return self.socks["pub"]

    def getPoller(self):
        return self.poller
    
    def close(self):
        self.ctx.destroy();

import zmq


class ServerSockets:
    ctx = zmq.Context()
    socks = dict()
    poller = zmq.Poller()

    def __init__(self):
        pass

    def startup(self):
        self.setXPub()
        self.setXSub()

    def setXSub(self):
        self.socks["xsub"] = self.ctx.socket(zmq.XSUB)
        # TODO: port
        self.socks["xsub"].bind("tcp://*:{0}".format())
        self.poller.register(self.socks["xsub"], zmq.POLLIN)

    def setXPub(self):
        self.socks["xpub"] = self.ctx.socket(zmq.XPUB)
        self.socks["xpub"].setsockopt(zmq.XPUB_VERBOSE, 1)
        # TODO: port
        self.socks["xpub"].bind("tcp://*:{0}".format())

    def getXSub(self):
        return self.socks["xsub"]

    def getXPub(self):
        return self.socks["xpub"]

    def getPoller(self):
        return self.poller
    
    def close(self):
        self.ctx.destroy();

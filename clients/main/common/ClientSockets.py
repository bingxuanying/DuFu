import zmq


class ClientSockets:
    ctx = None
    socks = dict()
    poller = None

    def __init__(self):
        # Init socket context
        self.ctx = zmq.Context()

        # Init poller
        self.poller = zmq.Poller()

    def setSub(self):
        self.socks["sub"] = self.ctx.socket(zmq.SUB)
        self.poller.register(self.socks["sub"], zmq.POLLIN)

    def getSub(self):
        return self.socks["sub"]

    def getPoller(self):
        return self.poller
    
    def close(self):
        self.ctx.destroy();

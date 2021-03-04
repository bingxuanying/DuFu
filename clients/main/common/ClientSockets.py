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

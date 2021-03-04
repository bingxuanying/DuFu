import zmq
from common.ClientSockets import ClientSockets


class SubscriberSockets(ClientSockets):
    port = dict()

    def __init__(self):
        ClientSockets.__init__(self)

        # Init socks
        self._init_socks()


    def _init_socks(self):
        self._init_sub()


    def _init_sub(self):
        self.socks["sub"] = self.ctx.socket(zmq.SUB)
        self.poller.register(self.socks["sub"], zmq.POLLIN)


    def get_sub(self):
        return self.socks["sub"]


    def get_poller(self):
        return self.poller
    

    def subscribe(self, topics):
        for topic in topics:
            self.socks["sub"].subscribe(topic)


    def connect(self, leader_broker_url):
        self.socks["sub"].connect(leader_broker_url)


    def disconnect(self, leader_broker_url):
        self.socks["sub"].disconnect(leader_broker_url)


    def close(self):
        self.ctx.destroy();
from os import path
import sys
import zmq
from configparser import ConfigParser
from common.ClientSockets import ClientSockets


class PublisherSockets(ClientSockets):
    port = dict()

    def __init__(self, port):
        ClientSockets.__init__(self)

        # Copy over ports
        self.port = port

        # Init socks
        self._init_socks()


    def _init_socks(self):
        if not self.port:
            sys.exit("NO valid port to bind.")

        self._init_pub()


    def _init_pub(self):
        self.socks["pub"] = self.ctx.socket(zmq.PUB)


    def get_pub(self):
        return self.socks["pub"]


    def get_poller(self):
        return self.poller
    

    def connect(self, leader_broker_url):
        self.socks["pub"].connect(leader_broker_url)


    def disconnect(self, leader_broker_url):
        self.socks["pub"].disconnect(leader_broker_url)


    def close(self):
        self.ctx.destroy();
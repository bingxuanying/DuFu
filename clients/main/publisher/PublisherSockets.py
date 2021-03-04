import zmq
from os import path
import sys
from ClientSockets import ClientSockets


class PublisherSockets(ClientSockets):
    port = dict()

    def __init__(self) -> None:
        ClientSockets.__init__(self)

        # Init ports
        self._init_port_config()

        # Init socks
        self._init_socks()


    # Init the subset of properties relevant to server
    def _init_port_config(self):
        # Locate config file
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(current_dir)
        config_file_dir = path.join(path.dirname(parent_dir), 'config', 'publisher.config')

        self.config_props.read(config_file_dir)
        self.port["pub"] = self.config_props["port"]["pub"]


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
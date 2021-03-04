from os import path
import sys
import zmq
from configparser import ConfigParser
from common.ClientSockets import ClientSockets


class PublisherSockets(ClientSockets):
    port = dict()
    config_file_dir = None

    def __init__(self):
        ClientSockets.__init__(self)

        # Get config file
        self._get_config_file_addr()

        # Init publisher props
        self._init_config_props()

        # Init socks
        self._init_socks()


    # Locate config file
    def _get_config_file_addr(self):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(path.dirname(path.dirname(current_dir)))
        self.config_file_dir = path.join(parent_dir, 'config', 'publisher.config')


    # Get the subset of properties relevant to broker server and zookeeper
    def _init_config_props(self):        
        # Copy the subset of properties
        props = ConfigParser()
        props.read(self.config_file_dir)
        self.port["pub"] = props["port"]["pub"]


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
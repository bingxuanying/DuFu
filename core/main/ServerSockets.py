from configparser import ConfigParser
import zmq
import sys
from os import path


class ServerSockets:
    ctx = None
    socks = dict()
    poller = None
    port = dict()


    def __init__(self):
        # Init socket context
        self.ctx = zmq.Context()

        # Init poller
        self.poller = zmq.Poller()

        # Init ports
        self._init_port_config()

        # Init socks
        self._init_socks()


    # Init the subset of properties relevant to server
    def _init_port_config(self):
        # Locate config file
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(current_dir)
        config_file_dir = path.join(path.dirname(parent_dir), 'config', 'server.config')

        server_props = ConfigParser()
        server_props.read(config_file_dir)
        self.port["xpub"] = server_props["broker"]["port.xpub"]
        self.port["xsub"] = server_props["broker"]["port.xsub"]


    def _init_socks(self):
        if not self.port or len(self.port) < 2:
            sys.exit("NO valid ports to bind.")

        self._init_xpub()
        self._init_xsub()


    def _init_xsub(self):
        self.socks["xsub"] = self.ctx.socket(zmq.XSUB)
        self.socks["xsub"].bind("tcp://*:{0}".format(self.port["xsub"]))
        self.poller.register(self.socks["xsub"], zmq.POLLIN)


    def _init_xpub(self):
        self.socks["xpub"] = self.ctx.socket(zmq.XPUB)
        self.socks["xpub"].setsockopt(zmq.XPUB_VERBOSE, 1)
        self.socks["xpub"].bind("tcp://*:{0}".format(self.port["xpub"]))


    def get_xsub(self):
        return self.socks["xsub"]


    def get_xpub(self):
        return self.socks["xpub"]


    def get_poller(self):
        return self.poller
    
    
    def close(self):
        self.ctx.destroy();

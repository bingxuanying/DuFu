from configparser import ConfigParser
import uuid
from os import path
from common import *

class PublisherConfig(ClientConfig):
    id = None
    port = dict()
    config_file_dir = None

    def __init__(self, debug_mode:bool=False):
        # Set server id
        self.id = str(uuid.uuid4())

        # Extened ClientConfig
        ClientConfig.__init__(self, "pub", debug_mode)

        # Get config file
        self._get_config_file_addr()

        # Init publisher props
        self._init_config_props()


    # Locate config file
    def _get_config_file_addr(self):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(current_dir)
        self.config_file_dir = path.join(path.dirname(parent_dir), 'config', 'publisher.config')


    # Get the subset of properties relevant to broker server and zookeeper
    def _init_config_props(self):        
        # Copy the subset of properties
        props = ConfigParser()
        props.read(self.config_file_dir)
        self.port["pub"] = props["publisher"]["port.pub"]

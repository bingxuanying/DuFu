import sys
import uuid
import netifaces


class ServerConfig:
    id = None
    host = None
    debug_mode = False


    def __init__(self, debug_mode:bool):
        # Set server id
        self.id = str(uuid.uuid4())

        # Init debug mode
        self.debug_mode = debug_mode
        
        # Init host address
        self._init_host_addr()

        # Init the subset of properties relevant to server
        self._init_port_config()


    # Init host ip address
    def _init_host_addr(self):
        name_lst = netifaces.interfaces()
        for name in name_lst:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
import sys
import netifaces


class ClientConfig:
    debug_mode = False
    role = None
    host = None
    time_format = "%Y/%d/%m %H:%M:%S.%f"

    def __init__(self, role:str, debug_mode:bool=False):
        # Init debug mode
        self.debug_mode = debug_mode

        # Config role as PUB/SUB
        self.role = role

        # Init host address
        self._init_host_addr()
        
    # Get current host ip address
    def _init_host_addr(self):
        name_lst = netifaces.interfaces()
        for name in name_lst:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
        
        if not self.host:
            sys.exit("Setting up client host ERROR")
import uuid
import sys
import netifaces


class Node:
    id = None
    role = None
    host = None
    time_format = None

    def __init__(self, role:str):
        # Set server id
        self.id = str(uuid.uuid4())

        # Config role as PUB/SUB
        self.role = role

        # Init host address
        self._init_host_addr()

        # Init time format
        self.time_format = "%Y/%d/%m %H:%M:%S.%f"
        
    # Get current host ip address
    def _init_host_addr(self):
        name_lst = netifaces.interfaces()
        for name in name_lst:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
    

    # Check if ready
    def ready(self):
        if not self.id:
            sys.exit("[ERR] No id is created")
        elif not self.role:
            sys.exit("[ERR] Role is not assigned")
        elif not self.time_format:
            sys.exit("[ERR] Time format is not assigned")
        elif not self.host:
            sys.exit("[ERR] NO valid host ip address.")
        
        return True
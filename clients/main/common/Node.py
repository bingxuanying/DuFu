import sys
import netifaces


class Node:
    id = None
    host = None

    def __init__(self):
        # Get current host ip
        host_list = netifaces.interfaces()
        for name in host_list:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
        
        if not self.host:
            print("Setting up client host ERROR", file=sys.stderr)

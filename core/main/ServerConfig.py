from configparser import ConfigParser
import sys
import netifaces


class ServerConfig:
    isDebug = False
    role = "broker"
    host = None
    port = {}

    def __init__(self, isDebug:bool):
        # Config if in Debug mode
        self.isDebug = isDebug
        
        # Get host address
        self.getHostAddr()

        # Copy the subset of properties relevant to server
        configParser = ConfigParser()
        serverProps = configParser.read("./config/server.config")
        self.port["xpub"] = serverProps["broker"]["port.xpub"]
        self.port["xsub"] = serverProps["broker"]["port.xsub"]

    # Get current host ip address
    def getHostAddr(self):
        nameLst = netifaces.interfaces()
        for name in nameLst:
            if len(name) > 4 and name[len(name)-4:] == "eth0":
                self.host = netifaces.ifaddresses(
                    name)[netifaces.AF_INET][0]['addr']
                break
        
        if not self.host:
            sys.exit("Setting up client host ERROR")
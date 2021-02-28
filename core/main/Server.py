from kazoo.client import KazooClient
from ServerConfig import ServerConfig
from Broker import Broker


class Server:
    zk = None
    broker = None

    def __init__(self, isDebug):
        # Init zookeeper
        self.zk = KazooClient(hosts='127.0.0.1:2181')

        # Init a broker
        self.broker = Broker()
    
    """
    **Start running the current broker
    """
    def start(self):
        try:
            pass
        except KeyboardInterrupt:
            exit()
    
    """
    **Terminate the server
    """
    def exit(self):
        print("[EXIT] Server is terminated.")
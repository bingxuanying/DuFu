import sys
from ServerConfig import ServerConfig
from ZookeeperLeaderElector import ZookeeperLeaderElector
from Broker import Broker


class BrokerServer:
    config = None
    zk_utils = None
    broker = None


    def __init__(self, isDebug):
        # Init server config
        self.config = ServerConfig()

        # Init zookeeper utils
        self.zk_utils = ZookeeperLeaderElector()
        
        # Init broker instance
        self.broker = Broker()
    

    """
    **Check if the broker server is startable
    """
    def startable(self):
        print("[SETUP/SERVER] Check if startable ...")

        if not self.zk_utils:
            sys.exit("NO valid zookeeper server url to connect.")
        
        if not self.config.id:
            sys.exit("NO valid server id.")
        
        if not self.config.host:
            sys.exit("NO valid host ip address.")
        
        self._start()


    """
    **Start broker server
    """
    def _start(self):
        print("[SETUP/ZK] Connect to zookeeper server ...")

        try:
            self.zk_utils.startup(self.config.id, self.config.host, self.broker.run)
        except KeyboardInterrupt:
            exit()
    

    """
    **Terminate broker server
    """
    def exit(self):
        print("[EXIT] Broker server {} is terminated.".format(self.config.id))
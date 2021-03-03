import sys
from .ServerConfig import ServerConfig
from .ZookeeperLeaderElector import ZookeeperLeaderElector
from .Broker import Broker


class BrokerServer:
    config = None
    zk_utils = None
    broker = None


    def __init__(self, debug_mode=False):
        # Init server config
        self.config = ServerConfig(debug_mode)

        # Init zookeeper utils
        self.zk_utils = ZookeeperLeaderElector()
        
        # Init broker instance
        self.broker = Broker()
    

    """
    **Check if the broker server is startable
    """
    def startable(self):
        print("[SETUP/SERVER] Check if startable ...")

        # Check if ZK Utils is ready (error free)
        # Check if config correctly
        # Start if precheck doesn't raise any error
        if self.zk_utils.ready() and self.config.ready():
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
        print("[EXIT] Shut down Broker server {}.".format(self.config.id))
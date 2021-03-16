from argparse import ArgumentParser
from ZookeeperLeaderElector import ZookeeperLeaderElector

from Broker import Broker


class BrokerServer:
    zk_utils = None
    broker = None


    def __init__(self, show_data:bool=False):
        # Init zookeeper utils
        self.zk_utils = ZookeeperLeaderElector()
        
        # Init broker instance
        self.broker = Broker(show_data)
    

    # Check if the broker server is startable
    def startable(self):
        print("[SETUP/SERVER] Check if startable ...")

        # Check if ZK Utils is ready (error free)
        # Check if broker configured correctly
        # Start if precheck doesn't raise any error
        if self.zk_utils.ready() and self.broker.ready():
            self._start()


    # Start broker server
    def _start(self):
        print("[SETUP/ZK] Connect to zookeeper server ...")

        try:
            self.zk_utils.startup(self.broker.id, self.broker.host, self.broker.run)
        except KeyboardInterrupt:
            exit()
    

    # Terminate broker server
    def exit(self):
        print("[EXIT] Shut down Broker server {}.".format(self.broker.id))


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-s", "--show", 
                            help="console log data being received or sent", 
                            dest="show", action="store_true", default=False)

    args = parser.parse_args()

    BrokerServer(args.show).startable()
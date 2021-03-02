from configparser import ConfigParser
from kazoo.client import KazooClient


class ZookeeperLeaderElector:
    zk = None
    zookeeper_connection_url = None


    def __init__(self):
        # Get the subset of properties relevant to zookeeper
        config_parser = ConfigParser()
        server_props = config_parser.read("./config/zookeeper.config")
        self.zookeeper_connection_url = server_props["zookeeper"]["connect"]

        # Init zookeeper client instance
        self.zk = KazooClient(self.zookeeper_connection_url)


    def startup(self, server_id, host_ip, broker_server_start):
        # Connect to zookeeper server
        self.zk.start()

        try:
            # Ensure a path, create if necessary
            self.zk.ensure_path("/cluster")

            # Create a node with data
            node = "node" + server_id
            path = "/cluster/" + node
            self.zk.create_async(path, bytes(host_ip, 'utf-8'), ephemeral=True)

            # Elect for leadership
            print("[SETUP/ZK] Elect for leadership ...")
            election = self.zk.Election("/cluster", node)
            election.run(broker_server_start)
        
        # Exit
        except KeyboardInterrupt:
            self.exit()
            
        # Alwasys stop the zk instance and disconnect
        finally:
            self.zk.stop()
            self.zk.close()
    

    def exit(self):
        print("[EXIT] Disconnect broker server from zookeeper server.")
from configparser import ConfigParser
from kazoo.client import KazooClient
from os import path
import sys

class ZookeeperLeaderElector:
    zk = None
    zookeeper_connection_url = None
    config_file_dir = None


    def __init__(self):
        # Locate config file
        self._get_config_file_addr()

        # Get the subset of properties relevant to zookeeper
        self._init_config_props()

        # Init zookeeper client instance
        self.zk = KazooClient(self.zookeeper_connection_url)


    # Locate config file
    def _get_config_file_addr(self):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(current_dir)
        self.config_file_dir = path.join(path.dirname(parent_dir), 'config', 'zookeeper.config')


    # Get the subset of properties relevant to zookeeper
    def _init_config_props(self):
        server_props = ConfigParser()
        server_props.read(self.config_file_dir)
        self.zookeeper_connection_url = server_props["connect"]["url"]


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
        print("[EXIT] Disconnect from zookeeper server.")
        raise KeyboardInterrupt

    def ready(self):
        if not self.config_file_dir:
            sys.exit("Doesn't find the config file.")
        elif not self.zookeeper_connection_url:
            sys.exit("Zookeeper server url is EMPTY.")
        elif not self.zk:
            sys.exit("Zookeeper instance instantiation FAILED.")
        
        return True
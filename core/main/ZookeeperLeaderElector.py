from configparser import ConfigParser
from kazoo.client import KazooClient
from os import path
import sys

class ZookeeperLeaderElector:
    zk = None
    default_node_path = None
    zookeeper_connection_url = None
    config_file_dir = None


    def __init__(self):
        # Default zookeeper node path to CRUD
        self.default_node_path = "/cluster"

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
            self.zk.ensure_path(self.default_node_path)

            # Create a node with data
            node = "node" + server_id
            path = self.default_node_path + '/' + node
            self.zk.create_async(path, bytes(host_ip, 'utf-8'), ephemeral=True)

            # Elect for leadership
            print("[SETUP/ZK] Elect for leadership ...")
            election = self.zk.Election(self.default_node_path, node)
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
            sys.exit("[ERR] Doesn't find the config file.")
        elif not self.zookeeper_connection_url:
            sys.exit("[ERR] Zookeeper server url is EMPTY.")
        elif not self.zk:
            sys.exit("[ERR] Zookeeper instance instantiation FAILED.")
        
        return True
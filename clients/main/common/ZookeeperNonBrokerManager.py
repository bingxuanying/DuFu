from configparser import ConfigParser
from kazoo.client import KazooClient
from os import path
import sys

class ZookeeperNonBrokerManager:
    zk = None
    default_node_path = None
    config_file_dir = None
    zookeeper_connection_url = None
    zookeeper_connection_timeout = None
    # subscriber only
    publisher_server_default_port = None
    publisher_server_url_lst = list()


    def __init__(self, role):
        # Default zookeeper node path to CRUD
        self.default_node_path = "/publishers"

        # Get config file
        self._get_config_file_addr(role)

        # Get the subset of properties relevant to zookeeper
        self._init_config_props(role)

        # Init zookeeper client instance
        self.zk = KazooClient(self.zookeeper_connection_url)


    # Locate config file
    def _get_config_file_addr(self, role):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(path.dirname(current_dir))
        filename = role + ".config"
        self.config_file_dir = path.join(path.dirname(parent_dir), "config", filename)


    # Get the subset of properties relevant to zookeeper
    def _init_config_props(self, role):
        props = ConfigParser()
        props.read(self.config_file_dir)
        self.zookeeper_connection_url = props["service_discovery"]["connection.url"]
        self.zookeeper_connection_timeout = int(props["service_discovery"]["connection.timeout.s"])

        if role == "publisher":
            pass
        elif role == "subscriber":
            self.publisher_server_default_port = props["publisher_server"]["port"]
        else:
            sys.exit("[ERR] Role not exists")


    def publisher_connect(self, role, node_id, host_ip):
        # Call prevention
        if role != "publisher":
            sys.exit("[ERR] This method can only be called by publisher")

        # Connect to zookeeper server
        if not self.zk.connected:
            self.zk.start(timeout=self.zookeeper_connection_timeout)

        try:
            # Ensure a path, create if necessary
            self.zk.ensure_path(self.default_node_path)

            # Create a node with data
            node = "node" + node_id
            path = self.default_node_path + '/' + node
            self.zk.create_async(path, bytes(host_ip, 'utf-8'), ephemeral=True)
        
        # Exit
        except KeyboardInterrupt:
            self.exit()

        # Alwasys stop the zk instance and disconnect
        finally:
            self.zk.stop()
            self.zk.close()


    def subscriber_connect(self, role):
        # Call prevention
        if role != "subscriber":
            sys.exit("[ERR] This method can only be called by subscriber")

        # Connect to zookeeper server
        if not self.zk.connected:
            self.zk.start(timeout=self.zookeeper_connection_timeout)

        try:
            # Ensure a path, create if necessary
            self.zk.ensure_path(self.default_node_path)

            # Get publisher server url list
            updated_publisher_server_url_lst = self.zk.get_children(self.default_node_path)
            if not self.publisher_server_url_lst:
                self.publisher_server_url_lst = updated_publisher_server_url_lst
            
            print(updated_publisher_server_url_lst)

            self.watch()
        
        # Exit
        except KeyboardInterrupt:
            self.exit()

        # Alwasys stop the zk instance and disconnect
        finally:
            self.zk.stop()
            self.zk.close()


    # Watch on the leader node, find new leader if the current leader suicides
    def watch(self):
        @self.zk.ChildrenWatch(self.default_node_path)
        def my_func(a, b, c):
            print("[SETUP/ZK] Start watching on leader node")
            print("a = ", a)
            print("b = ", b)
            print("c = ", c)


    def ready(self):
        if not self.config_file_dir:
            sys.exit("[ERR] Doesn't find the config file.")
        elif not self.zookeeper_connection_url:
            sys.exit("[ERR] Zookeeper server url is EMPTY.")
        elif not self.zk:
            sys.exit("[ERR] Zookeeper instance instantiation FAILED.")
        
        return True
    

    def exit(self):
        print("[EXIT] Disconnect from zookeeper server.")
        raise KeyboardInterrupt
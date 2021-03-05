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
            node_path = self.default_node_path + '/' + node
            self.zk.create_async(node_path, bytes(host_ip, "utf-8"), ephemeral=True)
        
        # Exit
        except KeyboardInterrupt:
            self.exit()

        # Alwasys stop the zk instance and disconnect
        finally:
            self.zk.stop()
            self.zk.close()


    def subscriber_connect(self, role, socks_connect, socks_disconnect):
        # Call prevention
        if role != "subscriber":
            sys.exit("[ERR] This method can only be called by subscriber")

        # Connect to zookeeper server
        if not self.zk.connected:
            self.zk.start(timeout=self.zookeeper_connection_timeout)

        try:
            # Ensure a path, create if necessary
            self.zk.ensure_path(self.default_node_path)

            # Watch on children
            self.watch(socks_connect, socks_disconnect)
        
        # Exit
        except KeyboardInterrupt:
            self.exit()

        # Alwasys stop the zk instance and disconnect
        finally:
            self.zk.stop()
            self.zk.close()


    # Watch on the leader node, find new leader if the current leader suicides
    def watch(self, socks_connect, socks_disconnect):
        @self.zk.ChildrenWatch(self.default_node_path)
        def my_func(updated_publisher_server_url_lst):
            if sorted(updated_publisher_server_url_lst) != sorted(self.publisher_server_url_lst):                
                # Find publishers to disconeect
                deleted_publisher_servers = [node for node in self.publisher_server_url_lst if node not in updated_publisher_server_url_lst]
                
                # Find newly join publishers to connect
                new_publisher_servers = [node for node in updated_publisher_server_url_lst if node not in self.publisher_server_url_lst]

                # Update local publisher_server_url_lst
                self.publisher_server_url_lst = updated_publisher_server_url_lst

                for node in deleted_publisher_servers:
                    node_path = self.default_node_path + '/' + node
                    host_ip = "tcp://" + self.zk.get(node_path) + ":" + self.publisher_server_default_port
                    print("disconnect from: " + host_ip)
                    socks_disconnect(host_ip)
                
                for node in new_publisher_servers:
                    node_path = self.default_node_path + '/' + node
                    host_ip = "tcp://" + self.zk.get(node_path) + ":" + self.publisher_server_default_port
                    print("connect to: " + host_ip)
                    socks_connect(host_ip)

                self.watch(socks_connect, socks_disconnect)
            else:
                print("[SETUP/ZK] Start watching on leader node")


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
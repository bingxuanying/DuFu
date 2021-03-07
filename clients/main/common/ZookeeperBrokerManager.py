from kazoo.client import KazooClient
from configparser import ConfigParser
from os import path
import sys

class ZookeeperBrokerManager:
    zk = None
    default_node_path = None
    config_file_dir = None
    zookeeper_connection_url = None
    zookeeper_connection_timeout = None
    broker_server_default_port = None
    leader_broker_node_path = None
    leader_broker_url = None

    def __init__(self, role):
        print("[SETUP/ZK] Communicate through broker")

        # Default zookeeper node path to CRUD
        self.default_node_path = "/cluster"

        # Get config file
        self._get_config_file_addr(role)

        # Init publisher props
        self._init_config_props()

        # Init zookeeper client instance
        self.zk = KazooClient(self.zookeeper_connection_url, read_only=True)


    # Locate config file
    def _get_config_file_addr(self, role):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(path.dirname(current_dir))
        filename = role + ".config"
        self.config_file_dir = path.join(path.dirname(parent_dir), "config", filename)


    # Get the subset of properties relevant to broker server and zookeeper
    def _init_config_props(self):
        props = ConfigParser()
        props.read(self.config_file_dir)
        self.broker_server_default_port = props["broker_server"]["port"]
        self.zookeeper_connection_url = props["service_discovery"]["connection.url"]
        self.zookeeper_connection_timeout = int(props["service_discovery"]["connection.timeout.s"])


    # Called when first start
    def startup(self, socks_connect, socks_disconnect):
        print("[SETUP/ZK] Connect to zookeeper ...")
        self.zk.start(timeout=self.zookeeper_connection_timeout)
        self.find_leader_broker(socks_connect, socks_disconnect)


    # Find the leader broker to connect
    def find_leader_broker(self, socks_connect, socks_disconnect):
        print("[SETUP/ZK] Find leader broker ...")
        # Reconnect if disconnected
        if not self.zk.connected:
            self.zk.start(timeout=self.zookeeper_connection_timeout)

        # Find the leader broker queue
        election = self.zk.Election(self.default_node_path)
        leader_queue = election.contenders()

        # If no leader exists, raise error
        if not leader_queue:
            sys.exit("[ERR] No active brokers.")
        
        # Identiy the leader broker node
        leader_node = leader_queue[0]
        self.leader_broker_node_path = self.default_node_path + '/' + leader_node

        # Read the leader broker connection url
        data, _ = self.zk.get(self.leader_broker_node_path)
        leader_host = data.decode("utf-8")
        self.leader_broker_url = "tcp://{0}:{1}".format(leader_host, self.broker_server_default_port)

        # Connect to leader broker
        socks_connect(self.leader_broker_url)

        # Watch on the leader node in case it dies
        self.watch(socks_connect, socks_disconnect)


    # Watch on the leader node, find new leader if the current leader suicides
    def watch(self, socks_connect, socks_disconnect):
        @self.zk.DataWatch(self.leader_broker_node_path)
        def my_func(data, stat, event):
            if stat:
                print("[SETUP/ZK] Start watching on leader node")
            else:
                socks_disconnect(self.leader_broker_url)
                self.find_leader_broker(socks_connect, socks_disconnect)

    
    # Check if props are ready and error free
    def ready(self):
        if not self.config_file_dir:
            sys.exit("[ERR] Doesn't find the config file.")
        elif not self.broker_server_default_port:
            sys.exit("[ERR] Broker server default port is not given.")
        elif not self.zookeeper_connection_url:
            sys.exit("[ERR] Zookeeper server url is EMPTY.")
        elif not self.zk:
            sys.exit("[ERR] Zookeeper instance instantiation FAILED.")
    
        return True

    
    # Must called on exit
    def exit(self):
        self.zk.stop()
        self.zk.close()
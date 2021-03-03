from kazoo.client import KazooClient
import uuid
from os import path
from configparser import ConfigParser
import sys


class ZKClient:
    zk = None
    config_file_dir = None
    zookeeper_connection_url = None
    broker_server_default_port = None
    leader_broker_node_path = None
    leader_broker_url = None

    def __init__(self):
        # Get config file
        self._get_config_file_addr()

        # Init publisher props
        self._init_config_props()

        # Init zookeeper client instance
        self.zk = KazooClient(self.zookeeper_connection_url, read_only=True)


    # Locate config file
    def _get_config_file_addr(self):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(path.dirname(current_dir))
        self.config_file_dir = path.join(path.dirname(parent_dir), 'config', 'publisher.config')


    # Get the subset of properties relevant to broker server and zookeeper
    def _init_config_props(self):
        props = ConfigParser()
        props.read(self.config_file_dir)
        self.broker_server_default_port = props["broker_server"]["port"]
        self.zookeeper_connection_url = props["service_discovery"]["connect"]


    # Called when first start
    def startup(self):
        self.zk.start()
        self.find_leader_broker()


    # Find the leader broker to connect
    def find_leader_broker(self):
        ret = self.zk.connected

        election = self.zk.Election("/cluster")
        leader_node = election.contenders()[0]
        self.leader_broker_node_path = "/cluster/" + leader_node

        data, _ = self.zk.get(self.leader_broker_node_path)
        leader_host = data.decode("utf-8")
        self.leader_broker_url = leader_host + ":" + self.broker_server_default_port
        print(self.leader_broker_url)

        self.watch()

    def watch(self):
        @self.zk.DataWatch(self.leader_broker_node_path)
        def my_func(data, stat, event):
            if stat:
                print("Start watching on leader node")
            else:
                self.find_leader_broker()

    
    # Check if props are ready and error free
    def ready(self):
        if not self.config_file_dir:
            sys.exit("Doesn't find the config file.")
        elif not self.broker_server_default_port:
            sys.exit("Broker server default port is not given.")
        elif not self.zookeeper_connection_url:
            sys.exit("Zookeeper server url is EMPTY.")
        elif not self.zk:
            sys.exit("Zookeeper instance instantiation FAILED.")
    
        return True

    
    # Must called on exit
    def exit(self):
        self.zk.stop()
        self.zk.close()
from os import path
import sys
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(currentdir)
sys.path.append(path.join(parentdir, "main"))

import unittest
import uuid
from kazoo.client import KazooClient
from common.ZookeeperNonBrokerManager import ZookeeperNonBrokerManager


class ZookeeperNonBrokerManagerTest(unittest.TestCase):

    def setUp(self):
        # Init instance
        self.zk_pub = ZookeeperNonBrokerManager("publisher")
        self.zk_sub = ZookeeperNonBrokerManager("subscriber")
        self.default_node_path = "/publishers"
    
    def tearDown(self) -> None:
        pass

    # Test if read config file from correct path
    def test_config_file_dir(self):
        current_dir = path.dirname(path.realpath(__file__))
        parent_dir = path.dirname(path.dirname(current_dir))

        actual_path = path.join(parent_dir, "config")
        self.assertEqual(self.zk_pub.config_file_dir, path.join(actual_path, "publisher.config"), \
            "Config file should be located at " + path.join(actual_path, "publisher.config"))
        self.assertEqual(self.zk_sub.config_file_dir, path.join(actual_path, "subscriber.config"), \
            "Config file should be located at " + path.join(actual_path, "subscriber.config"))

    # Test if call prevention works
    def test_publisher_connect_call_prevention(self):
        try:
            self.zk_sub.publisher_connect("subscriber", str(uuid.uuid4()), "10.0.0.1")
        except SystemExit as ex:
            actual_err_msg = "[ERR] This method can only be called by publisher"
            self.assertEqual(str(ex), actual_err_msg, "Program should stop and exit")

    # Test if call prevention works
    def test_subscriber_connect_call_prevention(self):
        try:
            self.zk_pub.subscriber_connect("publisher")
        except SystemExit as ex:
            actual_err_msg = "[ERR] This method can only be called by subscriber"
            self.assertEqual(str(ex), actual_err_msg, "Program should stop and exit")

    # Test if call prevention works
    def test_create_node(self):
        fake_host_ip_lst = ["0.0.0.0", "0.0.0.1", "0.0.0.2", "0.0.0.3"]
        for fake_host_ip in fake_host_ip_lst:
            self.zk_pub.publisher_connect("publisher", str(uuid.uuid4()), fake_host_ip)

        test_zk = KazooClient(self.zk_pub.zookeeper_connection_url)
        try:
            test_zk.start(5)
        except Exception:
            self.assertRaises("Couldn't connect to zookeeper server")

        # Test if path exists
        self.assertTrue(test_zk.exists(self.default_node_path), \
            "Path '/publishers' should exist in zookeeper server")
        
        test_node_lst = test_zk.get_children(self.default_node_path)
        test_node_data_lst = []
        for node in test_node_lst:
            data, _ = test_zk.get(self.default_node_path+'/'+node)
            test_node_data_lst.append(data.decode("utf-8"))
        # # Test under condition that ephemeral=False
        # self.assertEqual(sorted(test_node_data_lst), sorted(fake_host_ip_lst), "Create nodes error")

        # Test under condition that ephemeral=True
        self.assertEqual(sorted(test_node_data_lst), [], "Create nodes error")

    def test_subscriber_connect(self):
        test_zk = KazooClient(self.zk_sub.zookeeper_connection_url)
        try:
            test_zk.start(5)
        except Exception:
            self.assertRaises("Couldn't connect to zookeeper server")
            
        # Ensure a path, create if necessary
        test_zk.ensure_path(self.zk_sub.default_node_path)

        fake_host_ip_lst = ["0.0.0.0", "0.0.0.1", "0.0.0.2", "0.0.0.3"]

        try:
            for host_ip in fake_host_ip_lst:
                # Create a node with data
                node = "node" + str(uuid.uuid4())
                path = self.default_node_path + '/' + node
                test_zk.create(path, bytes(host_ip, "utf-8"))
            
            self.zk_sub.subscriber_connect("subscriber")
        finally:
            nodes_to_delete = test_zk.get_children(self.default_node_path)
            for node in nodes_to_delete:
                path = self.default_node_path + '/' + node
                test_zk.delete(path)
        
        children = test_zk.get_children(self.default_node_path)
        self.assertEqual(children, [])


        
if __name__ == '__main__':
    unittest.main()
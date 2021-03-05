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
        self.assertEqual(self.zk_pub.config_file_dir, path.join(actual_path, "publisher.config") \
            ,"Config file should be located at " + path.join(actual_path, "publisher.config"))
        self.assertEqual(self.zk_sub.config_file_dir, path.join(actual_path, "subscriber.config") \
            ,"Config file should be located at " + path.join(actual_path, "subscriber.config"))

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
        self.assertTrue(test_zk.exists(self.default_node_path) \
            ,"Path '/publishers' should exist in zookeeper server")
        
        test_node_lst = test_zk.get_children(self.default_node_path)
        print(test_node_lst)
        self.assertEqual(test_node_lst, fake_host_ip_lst, "Create nodes error")
        

if __name__ == '__main__':
    unittest.main()
from os import path
import sys
import shutil
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(path.dirname(currentdir))
sys.path.append(path.join(parentdir, "main"))

import unittest
import random
from subscriber.SubscriberRecords import SubscriberRecords


class SubscriberRecordsTest(unittest.TestCase):

    def setUp(self):
        # Init instance
        self.subscriber_records = SubscriberRecords("10.0.0.1")
        self.filepath = "D:\\VanderbiltU\\CS6381-Distributed Systems Principles\\PubSub-ZMQ\\assests"

        # Import fake data
        for _ in range(10):
            data = random.randint(1, 10)
            self.subscriber_records.add(data)
    
    def tearDown(self) -> None:
        self._clean_directory()
    
    # Clean directory
    def _clean_directory(self):
        if path.exists(self.filepath):
            shutil.rmtree(self.filepath)

    def test_file_path(self):
        self._clean_directory()

        actual_path = path.join(self.filepath, self.subscriber_records.filename)
        self.assertEqual(self.subscriber_records.filepath, actual_path)

    def test_file_save(self):
        self.subscriber_records.create_line_plot()
        actual_path = path.join(self.filepath, self.subscriber_records.filename)
        self.assertEqual(self.subscriber_records.filepath, actual_path)



if __name__ == '__main__':
    unittest.main()
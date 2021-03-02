import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from main.BrokerServer import BrokerServer

if __name__ == "__main__":
    broker_server = BrokerServer(False)
    broker_server.startable()
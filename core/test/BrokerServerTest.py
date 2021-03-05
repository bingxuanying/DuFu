from os import path
import sys
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(currentdir)
sys.path.append(path.join(parentdir, "main"))

from BrokerServer import BrokerServer


if __name__ == "__main__":
    broker_server = BrokerServer(True)
    broker_server.startable()
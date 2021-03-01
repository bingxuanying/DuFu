import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from main.common.ZKClient import ZKClient

if __name__ == "__main__":
    zk = ZKClient("127.0.0.1:2181")
    zk.startup()
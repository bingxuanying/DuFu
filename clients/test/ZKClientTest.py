import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from main.common.ZKClient import ZKClient

if __name__ == "__main__":
    zk_utils = ZKClient()

    if zk_utils.ready():
        zk_utils.startup()
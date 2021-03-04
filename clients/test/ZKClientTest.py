from os import path
import sys
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(currentdir)
sys.path.append(path.join(parentdir, "main"))

from time import sleep
from common.ZKClient import ZKClient


if __name__ == "__main__":
    zk_utils = ZKClient()

    if zk_utils.ready():
        try:
            zk_utils.startup()
            while 1:
                sleep(2)
                print(".")
        except KeyboardInterrupt:
            zk_utils.exit()
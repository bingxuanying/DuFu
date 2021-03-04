from os import path
import sys
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(currentdir)
sys.path.append(path.join(parentdir, "main"))

from time import sleep
from publisher.Publisher import Publisher


if __name__ == "__main__":
    pub = Publisher(False)

    pub.startable()
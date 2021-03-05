from os import path
import sys
currentdir = path.dirname(path.realpath(__file__))
parentdir = path.dirname(path.dirname(currentdir))
sys.path.append(path.join(parentdir, "main"))

from publisher.Publisher import Publisher


if __name__ == "__main__":
    pub = Publisher(True)
    pub.startable()
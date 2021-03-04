import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from time import sleep
from main.publisher.Publisher import Publisher


if __name__ == "__main__":
    pub = Publisher(False)

    pub.startable()
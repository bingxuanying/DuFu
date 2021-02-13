from os.path import dirname, abspath, realpath
import sys
d = dirname((realpath(__file__)))
sys.path.append(d + "/clients/main/")
sys.path.append(d + "/clients/test")
sys.path.append(d + "/core/test")

from configparser import ConfigParser

from run_client import main as run_client


def main():
    try:
        run_client()
    # On exit
    except KeyboardInterrupt:
        print("Exit Success")
        pass

if __name__ == "__main__":
    main()
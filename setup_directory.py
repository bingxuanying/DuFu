from os.path import dirname, realpath
import sys
root = dirname((realpath(__file__)))

sys.path.append(root + "/clients/main")
sys.path.append(root + "/clients/main/common")
sys.path.append(root + "/clients/main/publisher")
sys.path.append(root + "/clients/main/subscriber")

sys.path.append(root + "/core/main")
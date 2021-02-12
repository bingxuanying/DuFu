from os.path import dirname, abspath, realpath
import sys
d = dirname((realpath(__file__)))
sys.path.append(d + "/common")
sys.path.append(d + "/publisher")
sys.path.append(d + "/subscriber")
from os import path
import sys
rootdir = path.dirname((path.realpath(__file__)))

sys.path.append(path.join(rootdir, "clients", "main"))
sys.path.append(path.join(rootdir, "core", "main"))
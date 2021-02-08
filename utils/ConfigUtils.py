from configparser import ConfigParser


def getPort(name):
    conifg = ConfigParser()
    conifg.read("../config/connect-soruce.config")
    return conifg["port"][name]

from configparser import ConfigParser
import socket
import zmq


class Metadata:
    id = None
    host = None
    leaderAddr = None
    lookUpTable = set()
    portConfig = None

    def __init__(self):
        self.portConfig = ConfigParser()
        self.portConfig.read("../../../config/connect-soruce.config")
        host_name = socket.gethostname()
        self.host = socket.gethostbyname(host_name)

    def addLUT(self, newAddr):
        self.lookUpTable.add(newAddr)

    def removeLUT(self, oldAddr):
        self.lookUpTable.remove(oldAddr)

    def updateLUT(self, newLUT):
        self.lookUpTable = newLUT

    def findLeaderPublisher(self, sktSet) -> bool:
        print("Establishing connection with Publisher Leader ...")

        if self.__establishConnection(sktSet):
            print("Connected to Leader at {0.0.0.0}.".format(
                self.leaderAddr))
            return True
        else:
            print("Doesn't find a Leader.")
            print("Creating Leader ...")
            self.__createLeader()
            return False

    # !! Need Test HERE
    def __establishConnection(self, sktSet) -> bool:
        sktREQ, sktREP = sktSet["req"], sktSet["rep"]
        masked = self.host.rpartition('.')[0] + '.'
        port = self.portConfig["port"]["router"]

        for last in range(1, 255):
            sktREQ.connect("tcp://{0}.{1}:{0}".format(masked, last, port))
            try:
                sktREQ.send_string("NEW " + self.host)
                res = sktREQ.recv(zmq.NOBLOCK)
                # !! Check if res is TYPE set
                # !! Check leader ip addr
                if res:
                    print("Updating LookUpTable ...")
                    self.lookUpTable = res
                    print("Updating Leader Addreess ...")
                    self.leaderAddr = "{0}.{1}".format(masked, last)
                    port = self.portConfig["port"]["dealer"]
                    sktREP.connect("tcp://{0}:{0}".format(res, port))
                    return True
            except zmq.ZMQError:
                continue

        return False

    def __createLeader(self):
        self.leaderAddr = self.host
        self.lookUpTable.add(self.host)

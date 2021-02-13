from common import *
import zmq
from random import randrange


class Publisher:
    mqSkt = MQSocket()
    node = Node()
    config = None
    utils = ClientUtils()

    def __init__(self, config):
        print("[SETUP] Publisher initializing ...")
        # Init config
        self.config = config

        # Establish connection to Broker or Leader Publisher
        if self.config.ifBroker:
            print("[SETUP] Establishing connection with Broker ...")
            # TODO: connect to Broker
            pass
        else:
            # Init socket REQ and REP
            print("[SETUP] Setup REQ/REP/PUB sockets ...")
            self.mqSkt.setupReq()
            self.mqSkt.setupRep()
            self.mqSkt.setupPub()

            # Config Leader Publisher
            # print("[SETUP] Establishing connection with existing Publisher ...")
            # self.node.establishConnection(self.mqSkt)

    def run(self):
        print("Local IP Addr: " + self.node.host)

        sktRep, sktPub = self.mqSkt.getRep(), self.mqSkt.getPub()
        poller = self.mqSkt.getPoller()

        while True:
            try:
                # Recv Part
                socks = dict(poller.poll(1))
                if sktRep in socks and socks.get(sktRep) == zmq.POLLIN:
                    inMsg = sktRep.recv_string()
                    # sktPub.send_string(self.mogrify(key, body))
                    # print("Notified SUBs join " + body)
                    sktRep.send_string(self.utils.mogrify("ACK", ""))

                # Send Part
                zipcode = randrange(10000, 100000)
                body = {
                    "temperature": randrange(-80, 135),
                    "relhumidity": randrange(10, 60)
                }

                outMsg = self.utils.mogrify(zipcode, body)
                sktPub.send_string(outMsg)

                # Debug Mode
                if self.config.isDebug:
                    print(outMsg)

            # User Exit
            except KeyboardInterrupt:
                print("[EXIT] Attemptting to suicide ...")
                self.exit()
                break

    def exit(self):
        sktPub = self.mqSkt.getPub()
        msg = {
            "host": self.node.host
        }
        sktPub.send_string(self.utils.mogrify("LEAVE", msg))
        print("[EXIT] Publisher suicide success.")

    # """
    # Connect to broker
    # """
    # def connect(self):
    #     sktReq = self.mqSkt.getReq()
    #     masked = self.node.host.rpartition('.')[0]
    #     port = self.utils.getPort('rep')

    #     # Connect to random Publisher
    #     for last in range(1, 256):
    #         if "{0}.{1}".format(masked, last) == self.node.host:
    #             continue
    #         addr = "tcp://{0}.{1}:{2}".format(masked, last, port)
    #         sktReq.connect(addr)

    #     # Ask randomly conneted Publisher to notify subscribers to connect
    #     sktReq.send_pyobj(["JOIN", self.node.host])
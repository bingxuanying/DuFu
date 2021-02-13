class ClientConfig:
    ifBroker = None
    isDebug = False

    def __init__(self, ifBroker, isDebug=False):

        # Config if the applicaiton needs broker
        self.ifBroker = ifBroker

        # Config if in Debug mode
        self.isDebug = isDebug
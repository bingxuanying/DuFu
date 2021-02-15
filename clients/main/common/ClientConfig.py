class ClientConfig:
    ifBroker = None
    isDebug = False
    timeFormat = "%Y/%d/%m/%H/%M/%S/%f"

    def __init__(self, ifBroker, isDebug=False):

        # Config if the applicaiton needs broker
        self.ifBroker = ifBroker

        # Config if in Debug mode
        self.isDebug = isDebug

        # Config role to be PUB/SUB/BROKER
        self.role = None
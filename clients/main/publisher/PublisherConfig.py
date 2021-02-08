# from _typeshed import SupportsReadline


class PublisherConfig:
    hasBroker = None
    isDebug = False

    def __init__(self, hasBroker, isDebug=False):
        self.hasBroker = hasBroker
        self.isDebug = isDebug

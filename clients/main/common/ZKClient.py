from kazoo.client import KazooClient


class ZKClient:
    zk = None

    def __init__(self, zookeeperConnectionURL):
        self.zk = KazooClient(zookeeperConnectionURL)

    def startup(self):
        self.zk.start()
        # Ensure a path, create if necessary
        self.zk.ensure_path("/my/favorite")

        # Create a node with data
        self.zk.create("/my/favorite/node", b"host ip")

    def watchNode(self):
        # TODO: if node is delete, get new leader to connect
        pass
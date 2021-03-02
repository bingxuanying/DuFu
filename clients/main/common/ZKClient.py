from kazoo.client import KazooClient
import uuid


class ZKClient:
    zk = None

    def __init__(self, zookeeperConnectionURL):
        self.zk = KazooClient(zookeeperConnectionURL)

    def startup(self):
        self.zk.start()

        try:
            # Ensure a path, create if necessary
            self.zk.ensure_path("/cluster")

            # Create a node with data
            node = "node" + str(uuid.uuid4())
            path = "/cluster/" + node
            self.zk.create_async(path, b"host ip", ephemeral=True)

            election = self.zk.Election("/cluster", node)
            election.run(self.watch)
        except KeyboardInterrupt:
            _node = election.contenders()[0]
            data, stat = self.zk.get(node)
        finally:
            self.zk.stop()
            self.zk.close()


    def watch(self, msg):
        # TODO: if node is delete, get new leader to connect
        print("done " + str(msg))
        while True:
            continue
import zmq


class Subscriber:
    ctx = zmq.Context()
    skt = None
    config = None

    def __init__(self):
        pass

    def run(self):
        while True:
            try:
                msg = input("Type in msg here: ")
                print(msg)
            except KeyboardInterrupt:
                print("\ninterrupted")
                break

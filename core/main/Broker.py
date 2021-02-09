import zmq

# Initialize context and sockets
context = zmq.Context()
producer = context.socket(zmq.ROUTER)
consumer = context.socket(zmq.DEALER)
producer.bind("tcp://*.5555")
consumer.bind("tcp://*.5556")

# Initialize poll set
poller = zmq.Poller()
poller.register(producer, zmq.POLLIN)
poller.register(consumer, zmq.POLLIN)


# Allocate messages
while True:
    socks = dict(poller.poll())

    if socks.get(producer) == zmq.POLLIN:
        message = producer.recv_multipart()
        consumer.send_multipart(message)

    if socks.get(consumer) == zmq.POLLIN:
        message = consumer.recv_multipart()
        producer.send_multipart(message)

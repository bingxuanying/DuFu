import pathex
import logging

from BrokerServer import BrokerServer
from publisher.Publisher import Publisher
from subscriber.Subscriber import Subscriber


def main():
    try:
        # Logging config
        logging.basicConfig(filename='myapp.log', level=logging.INFO)

        # Ask users what instance to create
        name = input("Create a Broker, Publisher, or Subscriber (broker/pub/sub)? ")
        ans_set = {'broker', 'pub', 'sub'}
        while name not in ans_set:
            name = input("Please answer: broker, pub, or sub: ")

        # Ask users if want to enter debug mode to print our all messages
        show_data = input("Do you want to see transfered data being printed on console (y/n)? ")
        ans_set = {'y', 'n'}
        while show_data not in ans_set:
            show_data = input("Please answer: y or n: ")

        # Convert to boolean
        show_data = True if show_data == 'y' else False
        
        # Create corresponding instance and call run()
        if name == "broker":
            instance = BrokerServer(show_data)
        elif name == "pub":
            instance = Publisher(show_data)
        elif name == "sub":
            instance = Subscriber(show_data)
        
        # Start instance
        instance.startable()

    # On exit
    except KeyboardInterrupt:
        print("Stop creating")
        

if __name__ == "__main__":
    main()
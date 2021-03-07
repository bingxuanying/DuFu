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
        
        # Check if in broker mode
        broker_mode = 'y'
        ans_set = {'pub', 'sub'}
        if name in ans_set:
            broker_mode = input("Communicate through broker or not (y/n)? ")
            ans_set = {'y', 'n'}
            while broker_mode not in ans_set:
                broker_mode = input("Please answer: y or n: ")


        # Ask users if want to enter debug mode to print our all messages
        show_data = input("Do you want to see transfered data being printed on console (y/n)? ")
        ans_set = {'y', 'n'}
        while show_data not in ans_set:
            show_data = input("Please answer: y or n: ")

        # Convert to boolean
        show_data = True if show_data == 'y' else False
        broker_mode =  True if broker_mode == 'y' else False
        
        # Create corresponding instance and call run()
        if name == "broker":
            instance = BrokerServer(show_data)
        elif name == "pub":
            instance = Publisher(show_data, broker_mode)
        elif name == "sub":
            instance = Subscriber(show_data, broker_mode)
        
        # Start instance
        instance.startable()

    # On exit
    except KeyboardInterrupt:
        print("[EXIT] Exit success")
        

if __name__ == "__main__":
    main()
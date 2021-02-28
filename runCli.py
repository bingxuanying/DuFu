import setup_directory
import logging

from Broker import Broker
from Publisher import Publisher
from Subscriber import Subscriber


def main():
    try:
        # Logging config
        logging.basicConfig(filename='myapp.log', level=logging.INFO)

        # Ask users if want to enter debug mode to print our all messages
        isDebug = input("Enter debug mode so messages will be printed (y/n)? ")
        ansSet = {'y', 'n'}
        while isDebug not in ansSet:
            isDebug = input("Please answer as y or n: ")
        # Convert to boolean
        isDebug = True if isDebug == 'y' else False

        # Ask users what instance to create
        instance = input("Create a Broker, Publisher, or Subscriber (broker/pub/sub)? ")
        ansSet = {'broker', 'pub', 'sub'}
        while instance not in ansSet:
            instance = input("Please answer as broker, pub, or sub: ")
        
        # Create corresponding instance and call run()
        if instance == "broker":
            client = Broker(isDebug)
        elif instance == "pub":
            client = Publisher(isDebug)
        elif instance == "sub":
            client = Subscriber(isDebug)
        client.run()

    # On exit
    except KeyboardInterrupt:
        print("Exit Success")
        

if __name__ == "__main__":
    main()
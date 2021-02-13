import setup
from common import *
from publisher import *
from subscriber import *


#** Setup Env on user demands
def main():
    # Check if broker is need
    ifBroker = input("Build broker (y/n)? ")
    while ifBroker != 'y' and ifBroker != 'n':
        ifBroker = input("Please answer y or n: ")
    ifBroker = True if ifBroker == 'y' else False

    # Create Client Configration
    config = ClientConfig(ifBroker, True)

    # Check if setup a Publisher or Subscriber
    instance = input("Create a Publisher or Subscriber (pub/sub)? ")
    while instance != 'pub' and instance != 'sub':
        instance = input("Please answer pub or sub: ")
    
    # Create Publisher/Subcriber instance
    if instance == "pub":
        pub = Publisher(config)
        pub.run()
    else:
        sub = Subscriber(config)
        sub.run()


if __name__ == "__main__":
    main()

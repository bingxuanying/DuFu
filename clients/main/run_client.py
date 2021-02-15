import setup
from common import *
from publisher import *
from subscriber import *


#** Setup Env on user demands
def main(ifBroker=False):
    # Ask if enter debug mod
    isDebug = input("Enter Debug mode (y/n)? ")
    while isDebug != 'y' and isDebug != 'n':
        isDebug = input("Please answer y or n: ")
    isDebug = True if isDebug == 'y' else False

    # If the script is run directly, then assume no broker
    # Setup basic Configration
    config = ClientConfig(ifBroker, isDebug)

    # Ask if create a Publisher or Subscriber
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

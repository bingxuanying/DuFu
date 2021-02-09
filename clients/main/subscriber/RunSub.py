from Subscriber import Subscriber
from SubscriberConfig import SubscriberConfig


def main():
    isBroker = input("Build broker (y/n)? ")
    while isBroker != 'y' and isBroker != 'n':
        isBroker = input("Please answer y or n? ")
    isBroker = True if isBroker == 'y' or isBroker == 'Y' else False

    subscriberConfig = SubscriberConfig(isBroker)

    pub = Subscriber(subscriberConfig)
    pub.run()


if __name__ == "__main__":
    main()

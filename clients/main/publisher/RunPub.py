from Publisher import Publisher
from PublisherConfig import PublisherConfig


def main():
    isBroker = input("Build broker (y/n)? ")
    while isBroker != 'y' and isBroker != 'n':
        isBroker = input("Please answer y or n? ")
    isBroker = True if isBroker == 'y' or isBroker == 'Y' else False
    publisherConfig = PublisherConfig(isBroker)
    pub = Publisher(publisherConfig)
    pub.run()


if __name__ == "__main__":
    main()

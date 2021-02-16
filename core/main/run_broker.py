from Broker import Broker


def main():
    # Ask if enter debug mod
    isDebug = input("Enter Debug mode (y/n)? ")
    while isDebug != 'y' and isDebug != 'n':
        isDebug = input("Please answer y or n: ")
    isDebug = True if isDebug == 'y' else False

    broker = Broker(isDebug)
    broker.run()

if __name__ == "__main__":
    main()
from os.path import dirname, abspath, realpath
import sys
d = dirname((realpath(__file__)))
sys.path.append(d + "/clients/main/")
sys.path.append(d + "/core/main")
sys.path.append(d + "/utils")

from run_client import main as run_client
from run_broker import main as run_broker
import SysConfigUtils

# Ask if broker is needed
def setupBroker():
    ifBroker = input("Build broker (y/n)? ")
    while ifBroker != 'y' and ifBroker != 'n':
        ifBroker = input("Please answer y or n: ")
    ifBroker = True if ifBroker == 'y' else False
    return ifBroker

def main():
    try:
        ifBroker = True
        config = SysConfigUtils.getConfig()

        # If broker NOT exists, check if broker is needed
        if config["BROKER"]["host"] == "none":
            ifBroker = setupBroker()
            # Create broker
            if ifBroker:
                run_broker()
            # Does not want broker
            else:
                # Set broker in "abandon" mode
                config["BROKER"]["host"] = "abandon"
                with open('./config/connect-soruce.config', 'w') as configfile:
                    config.write(configfile)
                run_client(ifBroker)
        # If broker is not wanted / in "abandon" mode
        elif config["BROKER"]["host"] == "abandon":
            print("=== In NON-BROKER Mode === ")
            run_client(False)
        # If broker exists, create pub/sub instance
        else:
            print("=== In Broker Mode === ")
            run_client(True)

    # On exit
    except KeyboardInterrupt:
        print("Exit Success")
        

if __name__ == "__main__":
    main()
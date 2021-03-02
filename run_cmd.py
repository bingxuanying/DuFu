import re
from argparse import ArgumentParser

def getPropsFromArgs():
    pass

def main():
    pass

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("zk", 
                            help="connect to zookeeper at given url x.x.x.x:x", 
                            action="store", type=str, metavar="zookeeper_connection_url")

    parser.add_argument("-s", "--show", 
                            help="console log data being received or sent", 
                            dest="show", action="store_true", default=False)

    parser.add_argument("--broker", 
                            help="create # numnber of brokers", 
                            dest="broker", action="store", type=int, default=1)

    parser.add_argument("--pub", "--publisher", 
                            help="create # numnber of publishers", 
                            dest="pub", action="store", type=int, default=1)

    parser.add_argument("--sub", "--subscriber", 
                            help="create # numnber of subscribers", 
                            dest="sub", action="store", type=int, default=1)

    args = parser.parse_args()

    url_format = re.compile("^((\d{,3})\.){3}\d{,3}(:[1-9]\d{,3})?$")
    if url_format.match(args.zk) is None:
        parser.error("invalid zookeeper connection url.")
    
    print(args)
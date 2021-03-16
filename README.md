# DuFu

## Introduction:

Assignment for CS6381

Vanderbilt University

Instructor: Aniruddha Gokhale

This is a pub/sub system ran with Zookeeper in two modes:

1. Subscriber(s) establishes connection with publisher directly.
2. Subscrbier(s) and Publisher(s) communicate via active Broker(s).

## Prerequisites:

- Ubuntu Linux 20.04
- Mininet - Recommend installing from source
- Apache ZooKeeper 3.6.2 - Download and run `$ZOOKEEPER/bin/zkServer.sh start`
- Python 3 `sudo apt install python3`
- XTerm `sudo apt-get install xterm`
- Install packages by `sudo -H python3 -m pip install --upgrade pyzmq netifaces matplotlib`

## Demo

Demo Video URL: https://youtu.be/gyl4japzaV0

- 00:00​ - 01:10 Setup environment
- 01:10​ - 06:30 Direct communication between pub(s) and sub(s)
- 06:30​ - (end) Communicate via active broker(s)

## How to execute code:

### Start Instances (Broker, Publisher, Subscriber)

- **Broker**: ./bin/dufu-server-start.sh
- **Publisher**: ./bin/dufu-publisher-run.sh [broker]
- **Subscriber**: ./bin/dufu-subscriber-run.sh [broker]
  note: If the argument "broker" is given, the client instance will always look for the leader broker to connect.

### Importance:

1. Make sure Mininet is setup.
2. Make sure start zookeeper server on h1 node. Otherwise, modify the default address of zookeeper server on each config files under config folder
3. Make sure brokers, publishers, and subscribers are ran on hx node (e.g. h1, h2, h3, ... etc).

## View Performance

The code will record the tramission time of each piece of the data received from publisher(s). Once the subscriber instance is terminated, the latency data plot will be shown and save at **"./assests** folder.

## Note on Approaches

### Flooding Strategy

Publisher(s) connects to the Zookeeper and registers its ip address with it so that Subscribers can discover them. Publisher(s) binds on all possible ip addressesand sends the multicast message.

Subscriber(s) first connects to Zookeeper server and find all the active Publishers to estabilish TCP connections and receive the multicast message with the topic it subscribed. Subscriber(s) watches on the corresponding node on Zookeeper server for the Publisher(s) status updates.

### Broker Strategy

Broker(s) registers its ip address with Zookeeper server and elect for leadership. Once it's elected as leader, it then start serving for establishing communication between numbers of Publishers and Subscribers.

Publisher(s) read the ip address of the leader broker from Zookeeper server and establish TCP connections. Publisher(s) keeps watching on the corresponding node on Zookeeper server for the leader status updates. If new leader is elected, Publishers(s) will disconnect from the old one and attempt to establish TCP connection with the new leader broker. The multicast messages from the Publisher(s) are sent to the leader broker and then being pulled by Subscriber(s) on their demands.

Subscriber(s) read the ip address of the leader broker from Zookeeper server and establish TCP connections. Subscriber(s) keeps watching on the corresponding node on Zookeeper server for the leader status updates. If new leader is elected, Subscriber(s) will disconnect from the old one and attempt to establish TCP connection with the new leader broker. Subscriber(s) receives multicast message with the topic it subscribes with from the leader broker.

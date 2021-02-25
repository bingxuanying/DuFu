# PubSub-ZMQ


## Important:

* The script can only run on Linux System with Python3 and Mininet installed

# Demo

Demo Video URL: https://youtu.be/iZ8yKDVKD3U

* 00:00​ - 00:37 Brief Introduction

* 00:37​ - 07:28 Present Approach #1 (with broker)

* 07:28​ - end Present Approach #2 (non broker mode)

For both approaches, 

* I have first presented that **one** subscriber can successfuly receive messages of the topic it subscribed from publisher. 

* Then **one** subscriber can successfully received from **two** publishers. 

* Finaly, I presented that **two** subscribers can receive identical messages of the same topics they subscribed from publishers, and messages under different topics can only received by those who subscribed the topics. 


## Instructions:

1. run "sudo -H python3 -m pip install --upgrade pyzmq netifaces matplotlib"

2. run "sudo mn -x --topo=tree,fanout=3,depth=2"

3. On each xTerms Window, run "python3 ./run_test.py" under folder "PubSub-ZMQ" **on host (h1, h2, etc.) but NOT no switch (s1, s2, etc.)**

4. Follow instructions on command line to configure the system and create instance

    * Broker:
        * "y" => will create a broker and enter broker mode
        * "n" => will enter non-broker mode

    * Debug: 
        * "y" => will print out the data being sent or received
        * "n" => will not print anything
    
    * Pub/Sub:\
        * "pub" => create a publisher
        * "sub" => create a subscriber
    
    * (Only in Sub): 
        * enter the zipcode you want to subscribe.
        * enter "done" to indicate finish entering
    
    * Exit: Prese "Ctrl + C" to exit and terminate the program


## Explaination on Each Part

### Broker

* The frist time the user start the script, the user will be asked if he/she wants to build a broker. If "yes", the code will automatically create a broker for user on current host.

* After entering either "Broker Mode" or "Non-Broker Mode", the user cannot exit the mode unless program(s) are all turned off on each host.

* The broker cannot be turned off or stopped by "ctrl + c" if there are publisher(s) or subscriber(s) actively running on other hosts.

### Publisher

* The publisher(s) will randomly produce 5-digits zipcode and publish to either broker or subscriber.

### Subscriber

* The subscriber(s) has to scriber to a **5-digits** zipcode. Otherwise, the program will not take the zipcode, and warn the user.

* When exit, the program will automatically create plot that records the time it taks for the user to receive each pieces of data. There are some plot images on the root folder. Feel free to check it out.

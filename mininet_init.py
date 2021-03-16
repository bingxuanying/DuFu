from mininet.node import Controller
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info

if __name__ == "__main__":
    setLogLevel('info')

    net = Mininet(controller=Controller, cleanup=True, xterms=True)

    info('*** Adding controller\n')
    net.addController('c0')

    info( '*** Adding hosts\n' )
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')
    h5 = net.addHost('h5', ip='10.0.0.5')
    h6 = net.addHost('h6', ip='10.0.0.6')
    h7 = net.addHost('h7', ip='10.0.0.7')
    h8 = net.addHost('h8', ip='10.0.0.8')
    h9 = net.addHost('h9', ip='10.0.0.9')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    info('*** Adding links\n')
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s2, h1)
    net.addLink(s2, h2)
    net.addLink(s2, h3)
    net.addLink(s3, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)
    net.addLink(s4, h7)
    net.addLink(s4, h8)
    net.addLink(s4, h9)
    
    try:
        info('*** Starting network\n')
        net.start()

        # print(h1.cmd('./bin/dufu-server-start.sh'))

        info('*** Running CLI\n')
        CLI(net)

        info('*** Stopping network')
    finally:
        net.stopXterms()
        net.stop()

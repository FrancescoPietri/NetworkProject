#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import subprocess

class ShipTopo( Topo ):
    "Shiptopo"

    def __init__( self ):
        "Create Topo."

        # Initialize topology
        Topo.__init__( self )

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        weakbb_link_config = dict(bw=20)
        strongbb_link_config = dict(bw=50)
        host_link_config = dict()

        # Create switch nodes
        for i in range(6):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(8):
            self.addHost("h%d" % (i + 1), **host_config)

        # Add switch links
        self.addLink("s1", "s2", **weakbb_link_config)
        self.addLink("s1", "s5", **strongbb_link_config)
        self.addLink("s1", "s6", **strongbb_link_config)
        self.addLink("s2", "s4", **weakbb_link_config)
        self.addLink("s2", "s3", **strongbb_link_config)
        self.addLink("s3", "s4", **strongbb_link_config)
        self.addLink("s4", "s5", **weakbb_link_config)
        self.addLink("s5", "s6", **strongbb_link_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s2", **host_link_config)
        self.addLink("h3", "s2", **host_link_config)
        self.addLink("h4", "s3", **host_link_config)
        self.addLink("h5", "s4", **host_link_config)
        self.addLink("h6", "s4", **host_link_config)
        self.addLink("h7", "s5", **host_link_config)
        self.addLink("h8", "s6", **host_link_config)

topos = { 'shiptopo': ( lambda: ShipTopo() ) }

if __name__ == "__main__":
    topo = ShipTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    subprocess.call("./deny_ping.sh")    
    CLI(net)
    net.stop()


#   SpaceShip Topology:
#
#           h8
#            |
#            |
#          _s6_
#        _/    \_
#       /        \
# h1---s1--------s5---h7
#      |          |
#      |          |
# h2---s2--------s4---h6
#      |\_      _/|
#      |  \_  _/  |
#      h3   s3    h5
#            |
#            |
#            h4

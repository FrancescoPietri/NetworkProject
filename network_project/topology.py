#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import networkx as nx
import subprocess

class ShipTopo( Topo ):
    "Shiptopo"

    def __init__( self ):
        "Create Topo."

        # Initialize topology
        Topo.__init__( self )

        # Create switch nodes
        for i in range(6):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1))

        # Create host nodes
        for i in range(8):
            self.addHost("h%d" % (i + 1))

        # Add switch links
        self.addLink("s1", "s2")
        self.addLink("s1", "s5")
        self.addLink("s1", "s6")
        self.addLink("s2", "s4")
        self.addLink("s2", "s3")
        self.addLink("s3", "s4")
        self.addLink("s4", "s5")
        self.addLink("s5", "s6")

        # Add host links
        self.addLink("h1", "s1")
        self.addLink("h2", "s2")
        self.addLink("h3", "s2")
        self.addLink("h4", "s3")
        self.addLink("h5", "s4")
        self.addLink("h6", "s4")
        self.addLink("h7", "s5")
        self.addLink("h8", "s6")

topos = { 'shiptopo': ( lambda: ShipTopo() ) }


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

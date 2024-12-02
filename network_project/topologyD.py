#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import networkx as nx
import subprocess

class ShipTopoD( Topo ):
    "ShiptopoD"

    def __init__( self ):
        "Create Topo."

        # Initialize topology
        Topo.__init__( self )

        # Create switch nodes
        for i in range(6):
            SWdpid = "%016x" % (i + 1)
            self.addSwitch("s%d" % (i + 1), dpid = SWdpid)

        # Create host nodes
        for i in range(4):
            self.addHost("h%d" % (i + 1))

        # Add switch links
        #self.addLink("s1", "s2")
        self.addLink("s1", "s5")
        self.addLink("s1", "s6")
        self.addLink("s2", "s4")
        self.addLink("s2", "s3")
        #self.addLink("s3", "s4")
        self.addLink("s4", "s5")
        self.addLink("s5", "s6")

        # Add host links
        self.addLink("h1", "s1")
        self.addLink("h2", "s2")
        self.addLink("h3", "s6")
        self.addLink("h4", "s3")

topos = { 'shiptopoD': ( lambda: ShipTopoD() ) }


#   SpaceShip Topology:
#
#           h3
#            |
#            |
#          _s6_
#        _/    \_
#       /        \
# h1---s1--------s5
#                 |
#                 |
# h2---s2--------s4
#       \_          
#         \_      
#           s3    
#            |
#            |
#            h4

#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import networkx as nx
from topology import ShipTopo
import subprocess

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
    #controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    #net.addController(controller)
    net.build()
    net.start()
    subprocess.call("./deny_ping.sh")    
    nxTopo = nx.Graph()
    for switch in net.switches:
        print(switch)
        nxTopo.add_node(switch)

    CLI(net)
    net.stop()
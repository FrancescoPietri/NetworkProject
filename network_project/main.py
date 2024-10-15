from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import networkx as nx
from topology import ShipTopo
import subprocess
from CustomCLI import *

if __name__ == "__main__":
    topo = ShipTopo()

    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink
    )

    controller = net.addController('controller', controller=RemoteController, ip='127.0.0.1', port=6633)

    net.build()
    net.start()

    # subprocess.call("./deny_ping.sh")    

    MyCLI(net)  
    net.stop()  

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from topology import ShipTopo
from deployer import WebServiceDeployer 
from CustomCLI import MyCLI

def main():
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

    deployer = WebServiceDeployer()
    print(f"DEBUG: Initialized WebServiceDeployer: {deployer}")

    cli = MyCLI(net, deployer)  
    net.stop()

if __name__ == "__main__":
    main()

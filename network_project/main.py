from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from topology import ShipTopo
from deployer import WebServiceDeployer  # Importa la classe WebServiceDeployer
from CustomCLI import MyCLI  # Importa la tua CLI personalizzata

def main():
    # Crea la topologia e avvia Mininet
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

    # Initialize the WebServiceDeployer
    deployer = WebServiceDeployer()
    print(f"DEBUG: Initialized WebServiceDeployer: {deployer}")

    # Lancia la CLI personalizzata
    cli = MyCLI(net, deployer)  # Pass both net and deployer
    
    net.stop()

if __name__ == "__main__":
    main()

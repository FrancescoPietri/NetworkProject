from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI, CLI as OriginalCLI
from mininet.log import setLogLevel, info
from topology import ShipTopo  # Importa la tua topologia
import networkx as nx
import subprocess


def deploy_web_server(host):
    info(f"*** Starting web server on {host.name}\n")
    host.cmd('python3 -m http.server 80 &')


def deploy_database(host):
    info(f"*** Starting database server on {host.name}\n")
    host.cmd('service mysql start')


def configure_flow(net, src_host_name, dst_host_name):
    nxTopo = nx.Graph()
    for switch in net.switches:
        nxTopo.add_node(switch)

    for host in net.hosts:
        nxTopo.add_node(host)

    for link in net.links:
        nxTopo.add_edge(link.intf1.node.name, link.intf2.node.name)


    path = nx.shortest_path(nxTopo, src_host_name, dst_host_name)

    for step in range(len(path)-1):
        if step == 0:
            port_host_send = net.linksBetween(net.get(path[0]), net.get(path[1]))[0].intf1.name

            if not port_host_send.split('-')[0] == path[1]:
                port_host_send = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name
            port_host_send = int(port_host_send.split('eth')[1])
            subprocess.call(f"sudo ovs-ofctl add-flow {net.get(path[1])} dl_type=0x0800,nw_src=10.0.0.{path[len(path)-1].split('h')[1]},nw_dst=10.0.0.{path[0].split('h')[1]},actions=output:{port_host_send}", shell=True)

        else:
            if step == len(path)-2:
                port_host_reciver = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf1.name

                if not port_host_reciver.split('-')[0] == path[step]:
                    port_host_reciver = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name

                port_host_reciver = int(port_host_reciver.split('eth')[1])
                subprocess.call(f"sudo ovs-ofctl add-flow {net.get(path[step])} dl_type=0x0800,nw_src=10.0.0.{path[0].split('h')[1]},nw_dst=10.0.0.{path[len(path)-1].split('h')[1]},actions=output:{port_host_reciver}", shell=True)
            else:
                port_send = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf1.name
                port_return = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name
                if not port_send.split('-')[0] == path[step]:
                    port_send = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name
                    port_return = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf1.name

                port_send = int(port_send.split('eth')[1])
                subprocess.call(f"sudo ovs-ofctl add-flow {net.get(path[step])} dl_type=0x0800,nw_src=10.0.0.{path[0].split('h')[1]},nw_dst=10.0.0.{path[len(path)-1].split('h')[1]},actions=output:{port_send}", shell=True)

                port_return = int(port_return.split('eth')[1])
                subprocess.call(f"sudo ovs-ofctl add-flow {net.get(path[step+1])} dl_type=0x0800,nw_src=10.0.0.{path[len(path)-1].split('h')[1]},nw_dst=10.0.0.{path[0].split('h')[1]},actions=output:{port_return}", shell=True)


def custom_deploy(net, host_name, program_type):
    host = net.get(host_name)
    if program_type == "web":
        deploy_web_server(host)
    elif program_type == "db":
        deploy_database(host)
    else:
        info(f"*** Program {program_type} not recognized\n")


class CustomCLI(CLI):
    def __init__(self, net):
        self.net = net
        CLI.__init__(self, net)

    def do_deploy(self, line):
        args = line.split()
        if len(args) != 2:
            print("Usage: deploy <host> <program_type>")
            return
        host_name = args[0]
        program_type = args[1]
        custom_deploy(self.net, host_name, program_type)

    def do_flow(self, line):
        args = line.split()
        if len(args) != 2:
            print("Usage: flow <src_host> <dst_host>")
            return
        src_host = args[0]
        dst_host = args[1]
        configure_flow(self.net, src_host, dst_host)


def create_network():
    topo = ShipTopo()
    net = Mininet(topo=topo, controller=RemoteController)  # Usa RemoteController per connetterti a un controller remoto


    info("*** Starting network\n")
    net.start()


    CustomCLI(net)

    # Arresta la rete
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_network()


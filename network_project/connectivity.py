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

    net.build()
    net.start()
    #subprocess.call("./deny_ping.sh")    
    nxTopo = nx.Graph()
    for switch in net.switches:
        nxTopo.add_node(switch)

    for host in net.hosts:
        nxTopo.add_node(host)

    for link in net.links:
        nxTopo.add_edge(link.intf1.node.name, link.intf2.node.name)

    path = nx.shortest_path(nxTopo, "h2", "h6")


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

    CLI(net)
    net.stop()
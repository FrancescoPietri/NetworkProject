#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import networkx as nx
from topology import ShipTopo
import subprocess
import json

class FlowManager():
    
    def delete_flow(self, net, h1, h2):

        flow_write = []

        with open('flow.json', 'r') as json_file:
            flow_entries = json.load(json_file)

        for flow in flow_entries:
            if (flow["src"]==f"10.0.0.{h1.split('h')[1]}" or flow["src"]==f"10.0.0.{h2.split('h')[1]}") and (flow["dst"]==f"10.0.0.{h1.split('h')[1]}" or flow["dst"]==f"10.0.0.{h2.split('h')[1]}"):
                print(f"removed {h1}->{h2}")
            else:
                flow_write.append(flow)

        with open('flow.json', 'w') as json_file:
            json.dump(flow_write, json_file, indent=4)

        net.hosts[0].cmd(f"ping -c 1 {net.hosts[1]}")

    def create_flow(self, net, h1, h2):
        nxTopo = nx.Graph()
        for switch in net.switches:
            nxTopo.add_node(switch)

        for host in net.hosts:
            nxTopo.add_node(host)

        for link in net.links:
            nxTopo.add_edge(link.intf1.node.name, link.intf2.node.name)

        path = nx.shortest_path(nxTopo, h1, h2)

        flow_entries = []

        for step in range(len(path)-1):
            if step == 0:
                port_host_send = net.linksBetween(net.get(path[0]), net.get(path[1]))[0].intf1.name

                if not port_host_send.split('-')[0] == path[1]:
                    port_host_send = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name

                port_host_send = int(port_host_send.split('eth')[1])
                flow_entry = {
                    "dpid": "%016x" % (int(net.get(path[1]).name.split('s')[1])),
                    "src": f"10.0.0.{path[len(path)-1].split('h')[1]}",
                    "dst": f"10.0.0.{path[0].split('h')[1]}",
                    "actions": [{"type": "OUTPUT", "port": port_host_send}]
                }
                flow_entries.append(flow_entry)

            else:
                if step == len(path)-2:
                    port_host_receiver = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf1.name

                    if not port_host_receiver.split('-')[0] == path[step]:
                        port_host_receiver = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name

                    port_host_receiver = int(port_host_receiver.split('eth')[1])
                    flow_entry = {
                        "dpid":  "%016x" % (int(net.get(path[step]).name.split('s')[1])),
                        "src": f"10.0.0.{path[0].split('h')[1]}",
                        "dst": f"10.0.0.{path[len(path)-1].split('h')[1]}",
                        "actions": [{"type": "OUTPUT", "port": port_host_receiver}]
                    }
                    flow_entries.append(flow_entry)
                else:
                    port_send = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf1.name
                    port_return = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name
                    
                    if not port_send.split('-')[0] == path[step]:
                        port_send = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf2.name
                        port_return = net.linksBetween(net.get(path[step]), net.get(path[step+1]))[0].intf1.name

                    port_send = int(port_send.split('eth')[1])
                    flow_entry_send = {
                        "dpid":  "%016x" % (int(net.get(path[step]).name.split('s')[1])),
                        "dst": f"10.0.0.{path[len(path)-1].split('h')[1]}",
                        "src": f"10.0.0.{path[0].split('h')[1]}",
                        "actions": [{"type": "OUTPUT", "port": port_send}]
                    }
                    flow_entries.append(flow_entry_send)

                    port_return = int(port_return.split('eth')[1])
                    flow_entry_return = {
                        "dpid": "%016x" % (int(net.get(path[step+1]).name.split('s')[1])),
                        "dst": f"10.0.0.{path[0].split('h')[1]}",
                        "src": f"10.0.0.{path[len(path)-1].split('h')[1]}",
                        "actions": [{"type": "OUTPUT", "port": port_return}]
                    }
                    flow_entries.append(flow_entry_return)

        with open('flow.json', 'r') as json_file:
            old_flow_entries = json.load(json_file)

        for flow in old_flow_entries:
            flow_entries.append(flow)

        # Write flow entries to flow.json
        with open('flow.json', 'w') as json_file:
            json.dump(flow_entries, json_file, indent=4)

        # Log the created flows for debugging
        print("Flow entries created and saved to flow.json")

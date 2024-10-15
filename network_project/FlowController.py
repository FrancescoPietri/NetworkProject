from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
import json

class FlowController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FlowController, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.load_flows()
        self.installed_flows = set()

    def load_flows(self):
        with open('flow.json', 'r') as f:
            self.flows = json.load(f)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        datapath = ev.msg.datapath  
        dpid = datapath.id
        self.datapaths[dpid] = datapath  

        self.install_flows(dpid)

    def install_flows(self, dpid):
        self.load_flows()

        allowed_flows = set()

        for flow in self.flows:
            allowed_flows.add((flow['src'], flow['dst']))

            if flow['dpid'] == ("%016x" % (dpid)):
                print(f'adding flow {flow["src"]}->{flow["dst"]}')
                match = {
                    'dl_type': 0x0800, 
                    'nw_src': flow['src'],
                    'nw_dst': flow['dst']
                }
                actions = [
                    {'port': flow['actions'][0]['port']}
                ]
                self.add_flow(dpid, match, actions)
                self.installed_flows.add((flow['src'], flow['dst']))  

        flow_removed = set()
        for in_flow in self.installed_flows:
            if in_flow not in allowed_flows:  
                flow_removed.add((in_flow[0], in_flow[1]))
                self.remove_flow(dpid, in_flow)

        for i in flow_removed:
            self.installed_flows.remove(i)

        
    def remove_flow(self, dpid, flow):
        print(f'Removing flow {flow[0]} -> {flow[1]}')
        datapath = self.datapaths[dpid]
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(
            dl_type=0x0800,
            nw_src=flow[0],  
            nw_dst=flow[1]   
        )

        mod = parser.OFPFlowMod(
            datapath=datapath,
            command=ofproto.OFPFC_DELETE,
            priority=1, 
            match=match,
            out_port=ofproto_v1_0.OFPP_NONE  
        )

        datapath.send_msg(mod)

    def add_flow(self, dpid, match, actions):
        datapath = self.datapaths[dpid]
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(**match)

        action_objs = [parser.OFPActionOutput(action['port']) for action in actions]

        mod = parser.OFPFlowMod(datapath=datapath,
                                 priority=1,
                                 match=match,
                                 actions=action_objs)

        datapath.send_msg(mod)





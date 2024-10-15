from mininet.cli import CLI
from mininet.net import Mininet
from connectivity import FlowManager

class MyCLI(CLI):
    def __init__(self, *args, **kwargs):
        super(MyCLI, self).__init__(*args, **kwargs)
        self.mn = self.mn

    def do_initflow(self, line):
        "Create a flow between two hosts: Usage: createFlow <host1> <host2>"
        args = line.split()
        if len(args) != 2:
            print("Usage: initflow <host1> <host2>")
            return

        h1, h2 = args

        fm = FlowManager()
        
        fm.create_flow(self.mn, h1, h2)
    


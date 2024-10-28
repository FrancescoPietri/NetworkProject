from mininet.cli import CLI
from mininet.net import Mininet
from connectivity import FlowManager
from deployer import WebServiceDeployer

class MyCLI(CLI):
    def __init__(self, net, deployer, *args, **kwargs):
        # Print debug information to check if deployer is passed correctly
        print(f"DEBUG: Initializing MyCLI with deployer: {deployer}")

        # Ensure the network object is properly assigned
        self.mn = net
        print(f"DEBUG: Assigned Mininet network to self.mn")

        # Ensure the deployer object is properly assigned
        self.deployer = deployer
        print(f"DEBUG: Assigned deployer to self.deployer")

        # Pass the net object directly to the Mininet CLI constructor
        super(MyCLI, self).__init__(net, *args, **kwargs)

    def do_initflow(self, line):
        "Create a flow between two hosts: Usage: initflow <host1> <host2>"
        args = line.split()
        if len(args) != 2:
            print("Usage: initflow <host1> <host2>")
            return

        h1, h2 = args
        fm = FlowManager()
        fm.create_flow(self.mn, h1, h2)
        print(f"Flow created between {h1} and {h2}")

    def do_removeflow(self, line):
        "delete flow between two hosts usage: removeflow <host1> <host2>"
        args = line.split()
        if len(args) != 2:
            print("Usage: removeflow <host1> <host2>")
            return

        h1, h2 = args
        fm = FlowManager()
        fm.delete_flow(self.mn, h1, h2)

    def do_deploy(self, line):
        "Deploy a web service to a specified host: Usage: deploy <host> <service_name> <service_path>"
        args = line.split()
        if len(args) != 3:
            print("Usage: deploy <host> <service_name> <service_path>")
            return

        host, service_name, service_path = args

        # Print debug information to check if deployer exists when the method is called
        print(f"DEBUG: Calling deploy_service with {host}, {service_name}, {service_path}")

        # Make sure deployer exists before calling deploy_service
        if not hasattr(self, 'deployer'):
            print("ERROR: deployer is not set in MyCLI")
            return

        self.deployer.deploy_service(self.mn, service_name, service_path, host)
        print(f"Service {service_name} deployed on {host}")

    def do_check_status(self, line):
        "Check if the web service is running on a specified host: Usage: check_status <host> [port]"
        args = line.split()
        if len(args) not in (1, 2):
            print("Usage: check_status <host> [port]")
            return

        host = args[0]
        port = int(args[1]) if len(args) == 2 else 80  # Default to port 80 if not provided
        if self.deployer.check_service_status(self.mn, host, port):
            print(f"Service on {host}:{port} is active")
        else:
            print(f"Service on {host}:{port} is not responding or inactive")

    def do_list_deployments(self, line):
        "List all deployments"
        self.deployer.list_deployments()

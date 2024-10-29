from mininet.cli import CLI
from mininet.net import Mininet
from connectivity import FlowManager
from deployer import WebServiceDeployer
import socket


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
        """
        Deploy a web service to a specified host.
        Usage: deploy <service_name> <service_path> [host]
        If no host is specified, the service will be deployed on the host with the fewest active services.
        """
        args = line.split()
        if len(args) < 2 or len(args) > 3:
            print("Usage: deploy <service_name> <service_path> [host]")
            return

        service_name = args[0]
        service_path = args[1]
        host = args[2] if len(args) == 3 else None  # Host is optional

        print(f"DEBUG: Calling deploy_service with service_name={service_name}, service_path={service_path}, host={host}")

        # Chiama il metodo deploy_service; host sarà None se non specificato
        self.deployer.deploy_service(self.mn, service_name, service_path, host)
        print(f"Service {service_name} deployed on {host or 'the host with the fewest active services'}")


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

    def do_stop(self, line):
        """
        Stop a running service on a specified host or on all hosts if the host is not specified.
        Usage: stop <service_name> [host]
        """
        args = line.split()
        if len(args) < 1 or len(args) > 2:
            print("Usage: stop <service_name> [host]")
            return

        service_name = args[0]
        host = args[1] if len(args) == 2 else None  # Host is optional

        print(f"DEBUG: Stopping service {service_name} on {'host ' + host if host else 'all hosts'}")

        # Chiamata al metodo stop_service; passa None come host per fermare il servizio su tutti gli host
        self.deployer.stop_service(self.mn, service_name, host)
        print(f"Service {service_name} stopped on {host or 'all hosts where it is running'}")


    def do_service_count(self, line):
        "Mostra il conteggio e i nomi dei servizi attivi per ogni host: Usage: service_count"
        service_count = self.deployer.get_service_count()
        for host, data in service_count.items():
            print(f"{host}: {data['count']} servizi attivi - {data['services']}")

    def do_run_client(self, line):
        """
        Run a client to connect to a server on a specified host and port.
        Usage: run_client <client_host> <server_host> <port>
        """
        args = line.split()
        if len(args) != 3:
            print("Usage: run_client <client_host> <server_host> <port>")
            return

        client_host_name, server_host_name, port = args
        port = int(port)

        try:
            client_host = self.mn.get(client_host_name)
            server_host = self.mn.get(server_host_name)
            server_ip = server_host.IP()
        except KeyError as e:
            print(f"Errore: {e}. Assicurarsi che i nomi degli host siano corretti.")
            return

        print(f"DEBUG: Connecting from {client_host_name} to {server_host_name} ({server_ip}) on port {port}")

        # Definisci uno script Python inline per eseguire il client
        client_script = f"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('{server_ip}', {port}))
for i in range(3):
    msg = f'Messaggio {{i+1}} dal client'
    s.send(msg.encode())
    print('Inviato al server:', msg)
    response = s.recv(1024)
    print('Risposta dal server:', response.decode())
s.close()
"""

        # Esegui lo script sul client
        output = client_host.cmd(f'python3 -c "{client_script}"')
        print("Output del client:")
        print(output)



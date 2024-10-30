import subprocess
from connectivity import FlowManager
import time
import threading

class WebServiceDeployer:
    def __init__(self):
        self.deployments = []
        self.service_count = {}

    def deploy_service(self, net, service_name, port, host_server = None, host_name=None):
        if not self.service_count:
            self.service_count = {host.name: {"count": 0, "services": []} for host in net.hosts}

        try:
            if not host_name:
                host_name = min(self.service_count, key=lambda h: self.service_count[h]["count"])
                print(f"Deploying on:{host_name}")

            host = net.get(host_name)
            remote_path = f"/home/mininet/{service_name}"

            print(f"Starting {service_name} on {host_name}")
            if service_name == "server.py":
                host.cmd(f'python3 {service_name} {port}&')
            else:
                fm = FlowManager()

                fm.create_flow(net, host_name, host_server)
                host.cmd(f"ping -c 1 {net.get(host_server)}")
                time.sleep(5)

                ip = net.get(host_server)
                ip = ip.IP()
                host.cmd(f'python3 {service_name} {port} {ip}&')

            if host_name not in self.service_count:
                self.service_count[host_name] = {"count": 0, "services": []}
            self.service_count[host_name]["count"] += 1
            self.service_count[host_name]["services"].append(port)

            deployment_info = {
                "service_name": service_name,
                "host": host_name,
                "status": "success",
                "remote_path": remote_path
            }
            self.deployments.append(deployment_info)
            print(f"Successfully deployed {service_name} on {host_name}")
            return host_name 

        except Exception as e:
            deployment_info = {
                "service_name": service_name,
                "host": host_name,
                "status": "failed",
                "error": str(e)
            }
            self.deployments.append(deployment_info)
            print(f"Error during deployment of {service_name} on {host_name}: {e}")
            

    def stop_service(self, net, service_name, port, host_name=None):
        try:
            if host_name:
                self._stop_service_on_host(net, port, host_name)
            else:
                print(f"Stopping all services on port: {port}")
                for host in self.service_count:
                    self._stop_service_on_host(net, port, host, service_name)
        except Exception as e:
            print(f"Error during stopping service on port: {port}: {e}")

    def _stop_service_on_host(self, net, port, host_name, service_name):
        host = net.get(host_name)
        print(f"Stopped service on port:{port} on {host_name}")
        host.cmd(f'fuser -k {port}/tcp')    
        print(host.cmd(f'ps'))

        if host_name in self.service_count and self.service_count[host_name]["count"] > 0:
            if port in self.service_count[host_name]["services"]:
                self.service_count[host_name]["services"].remove(port)
                self.service_count[host_name]["count"] -= 1
                print(f"Service at port: {port} stopped successfully on {host_name}")

    def get_service_count(self):
        return self.service_count


    #NOT USED!
    def list_deployments(self):
        for deployment in self.deployments:
            print(deployment)


    #NOT USED!
    def check_service_status(self, net, host_name, port=80):
        host = net.get(host_name)
        print(f"Verifie if service is active {host_name}:{port}")

        response = host.cmd(f'curl -s -o /dev/null -w "%{{http_code}}" http://{host.IP()}:{port}')
        print(f"response: {response}")

        if response == "200":
            print(f"the server {host_name} is active and working")
            return True
        else:
            print(f"the server {host_name} is not working properly. HTTP Code: {response}")
            return False

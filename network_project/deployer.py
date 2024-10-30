import subprocess
from connectivity import FlowManager
import time

class WebServiceDeployer:
    def __init__(self):
        # Lista dinamica per tenere traccia dei servizi distribuiti
        self.deployments = []
        # Dizionario per tenere traccia del numero e dei nomi dei servizi per host
        self.service_count = {}

    def deploy_service(self, net, service_name, port, host_server = None, host_name=None):
        # Inizializza la struttura del dizionario service_count per ogni host se non è stata già inizializzata
        if not self.service_count:
            self.service_count = {host.name: {"count": 0, "services": []} for host in net.hosts}

        try:
            # Se l'host non è specificato, seleziona quello con meno servizi attivi
            if not host_name:
                host_name = min(self.service_count, key=lambda h: self.service_count[h]["count"])
                print(f"Host non specificato. Selezionato l'host con meno servizi attivi: {host_name}")

            # Trova l'host nella rete Mininet
            host = net.get(host_name)
            remote_path = f"/home/mininet/{service_name}"

            print(f"Avvio del servizio {service_name} su {host_name}")
            if service_name == "server.py":
                host.cmd(f'python3 {service_name} {port}&')
            else:
                fm = FlowManager()

                fm.create_flow(net, host_name, host_server)
                host.cmd(f"ping -c 1 {net.get(host_server)}")
                time.sleep(5)

                ip = net.get(host_server)
                ip = ip.IP()
                output = host.cmd(f'python3 {service_name} {port} {ip}')
                print("host output:\n")
                print(output)


            # Aggiorna il conteggio dei servizi e aggiungi il nome del servizio
            if host_name not in self.service_count:
                self.service_count[host_name] = {"count": 0, "services": []}
            self.service_count[host_name]["count"] += 1
            self.service_count[host_name]["services"].append(service_name)

            deployment_info = {
                "service_name": service_name,
                "host": host_name,
                "status": "success",
                "remote_path": remote_path
            }
            self.deployments.append(deployment_info)
            print(f"Deployment successo per {service_name} su {host_name}")
            return host_name 

        except Exception as e:
            deployment_info = {
                "service_name": service_name,
                "host": host_name,
                "status": "failed",
                "error": str(e)
            }
            self.deployments.append(deployment_info)
            print(f"Errore durante il deploy del servizio {service_name} su {host_name}: {e}")
            

    def stop_service(self, net, service_name, host_name=None):
        """Ferma un servizio attivo su uno specifico host o su tutti gli host se l'host non è specificato."""
        try:
            if host_name:
                # Arresta il servizio solo sull'host specificato
                self._stop_service_on_host(net, service_name, host_name)
            else:
                # Se l'host non è specificato, arresta il servizio su tutti gli host in cui è presente
                print(f"Arresto del servizio {service_name} su tutti gli host")
                for host in self.service_count:
                    self._stop_service_on_host(net, service_name, host)
        except Exception as e:
            print(f"Errore durante l'arresto del servizio {service_name}: {e}")

    def _stop_service_on_host(self, net, service_name, host_name):
        """Arresta il servizio su un host specifico e aggiorna il conteggio."""
        host = net.get(host_name)
        print(f"Arresto del servizio {service_name} su {host_name}")
        host.cmd(f'pkill -f {service_name}')

        # Decrementa il conteggio dei servizi e rimuovi il nome del servizio
        if host_name in self.service_count and self.service_count[host_name]["count"] > 0:
            if service_name in self.service_count[host_name]["services"]:
                self.service_count[host_name]["services"].remove(service_name)
                self.service_count[host_name]["count"] -= 1
                print(f"Servizio {service_name} fermato con successo su {host_name}")

    def get_service_count(self):
        """Restituisce il conteggio e i nomi dei servizi attivi per ogni host"""
        return self.service_count

    def list_deployments(self):
        # Stampa tutte le distribuzioni eseguite
        for deployment in self.deployments:
            print(deployment)

    def check_service_status(self, net, host_name, port=80):
        """Verifica se il servizio è attivo su un determinato host e porta (predefinito: 80)."""
        host = net.get(host_name)
        print(f"Verifica se il servizio è attivo su {host_name}:{port}")

        # Utilizza curl per fare una richiesta HTTP verso l'host stesso
        response = host.cmd(f'curl -s -o /dev/null -w "%{{http_code}}" http://{host.IP()}:{port}')
        print(f"response: {response}")

        if response == "200":
            print(f"Il server su {host_name} è attivo e risponde correttamente.")
            return True
        else:
            print(f"Il server su {host_name} non è attivo o non ha risposto correttamente. Codice HTTP: {response}")
            return False

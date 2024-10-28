import subprocess

class WebServiceDeployer:
    def __init__(self):
        # Lista dinamica per tenere traccia dei servizi distribuiti
        self.deployments = []
        self.service_count = {}  # Dizionario per tenere traccia del numero di servizi per host
        self.semaphore = None

    def deploy_service(self, net, service_name, service_path, host_name=None):
        if not self.semaphore:
            self.service_count = {host.name: 0 for host in net.hosts}
            self.semaphore = 1

        try:
            # Se l'host non è specificato, seleziona quello con meno servizi attivi
            if not host_name:
                #if not self.service_count:
                    # Inizializza la lista di host e imposta 0 per ciascuno se `service_count` è vuoto
                    #self.service_count = {host.name: 0 for host in net.hosts}

                # Trova l'host con il minor numero di servizi attivi
                host_name = min(self.service_count, key=self.service_count.get)
                print(f"Host non specificato. Selezionato l'host con meno servizi attivi: {host_name}")

            # Trova l'host nella rete Mininet
            host = net.get(host_name)
            remote_path = f"/home/mininet/{service_name}"
            print(f"Avvio del servizio {service_name} su {host_name}")
            host.cmd(f'python3 {service_name} &')

            # Aggiorna il conteggio dei servizi per l'host
            if host_name not in self.service_count:
                self.service_count[host_name] = 0
            self.service_count[host_name] += 1

            deployment_info = {
                "service_name": service_name,
                "host": host_name,
                "status": "success",
                "remote_path": remote_path
            }
            self.deployments.append(deployment_info)
            print(f"Deployment successo per {service_name} su {host_name}")
        except Exception as e:
            deployment_info = {
                "service_name": service_name,
                "host": host_name,
                "status": "failed",
                "error": str(e)
            }
            self.deployments.append(deployment_info)
            print(f"Errore durante il deploy del servizio {service_name} su {host_name}: {e}")

    def stop_service(self, net, service_name, host_name):
        """Ferma un servizio attivo su uno specifico host"""
        try:
            host = net.get(host_name)
            print(f"Arresto del servizio {service_name} su {host_name}")
            host.cmd(f'pkill -f {service_name}')

            # Decrementa il conteggio dei servizi per l'host
            if host_name in self.service_count and self.service_count[host_name] > 0:
                self.service_count[host_name] -= 1

            print(f"Servizio {service_name} fermato con successo su {host_name}")
        except Exception as e:
            print(f"Errore durante l'arresto del servizio {service_name} su {host_name}: {e}")

    def get_service_count(self):
        """Restituisce il conteggio dei servizi attivi per ogni host"""
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

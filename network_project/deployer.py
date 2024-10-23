import subprocess

class WebServiceDeployer:
    def __init__(self):
        # Lista dinamica per tenere traccia dei servizi distribuiti
        self.deployments = []

    def deploy_service(self, net, service_name, service_path, host_name):
        try:
            # Trova l'host nella rete Mininet
            host = net.get(host_name)

            # Percorso dove salvare il servizio sull'host remoto
            remote_path = f"/home/mininet/{service_name}"

            # Trasferisci il file del servizio all'host tramite SCP
            print(f"Trasferimento del file {service_name} a {host_name}")
            host.cmd(f'scp {service_path} {host_name}:{remote_path}')

            # Avvia il servizio web usando SSH
            print(f"Avvio del servizio {service_name} su {host_name}")
            host.cmd(f'python3 {remote_path} &')

            # Aggiungi informazioni alla lista dei deployment
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

    def check_service_status(self, net, host_name, port=80):
        """Verifica se il servizio è attivo su un determinato host e porta (predefinito: 80)."""
        host = net.get(host_name)
        print(f"Verifica se il servizio è attivo su {host_name}:{port}")

        # Utilizza curl per fare una richiesta HTTP verso l'host stesso
        response = host.cmd(f'curl -s -o /dev/null -w "%{{http_code}}" http://{host.IP()}:{port}')

        if response == "200":
            print(f"Il server su {host_name} è attivo e risponde correttamente.")
            return True
        else:
            print(f"Il server su {host_name} non è attivo o non ha risposto correttamente. Codice HTTP: {response}")
            return False

    def list_deployments(self):
        # Stampa tutte le distribuzioni eseguite
        for deployment in self.deployments:
            print(deployment)


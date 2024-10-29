import time

def deploy_client():
    print("Client distribuito con successo. In attesa di avvio...")
    # Attendi indefinitamente o fino a quando non viene richiamato per connettersi
    while True:
        time.sleep(1)

if __name__ == "__main__":
    deploy_client()


import time
import socket
import sys

def deploy_client(port, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((f'{ip}', port))
    for i in range(3):
        msg = f'Messaggio {i+1} dal client'
        s.send(msg.encode())
        print('Inviato al server:', msg)
        response = s.recv(1024)
        print('Risposta dal server:', response.decode())
    s.close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 2 else 9090
    ip = str(sys.argv[2]) if len(sys.argv) > 2 else None
    deploy_client(port, ip)


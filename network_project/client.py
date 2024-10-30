import socket
import sys
import threading
import time

def deploy_client_sender(port, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((ip, port))
        print(f'Connected to server at {ip}:{port}')
        while True:
            msg = f'message from client {ip}'
            s.send(msg.encode())
            print('Sent:', msg)
            response = s.recv(1024)
            print('Answer from server:', response.decode())
            time.sleep(10)
    except (socket.timeout, socket.error) as e:
        print(f"Connection error: {e}")
    finally:
        s.close()

def deploy_client_listener(listen_port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(('0.0.0.0', listen_port))
    listener.listen(1)
    print(f'Client listening on port {listen_port}...')
    
    while True:
        conn, addr = listener.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('Received:', data.decode())
                conn.sendall(b'ACK') 

if __name__ == "__main__":

    server_port = int(sys.argv[1])
    server_ip = str(sys.argv[2])  

    threading.Thread(target=deploy_client_sender, args=(server_port, server_ip)).start()
    threading.Thread(target=deploy_client_listener, args=(server_port,)).start()



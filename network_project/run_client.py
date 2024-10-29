# esempio client conntection
import socket
import sys

def connect_to_server(server_ip, port, num_messages=3):
    print(f"Connettendo a {server_ip} sulla porta {port}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))

    for i in range(num_messages):
        message = f"Messaggio {i+1} dal client"
        client.send(message.encode())
        print(f"Inviato al server: {message}")

        response = client.recv(1024).decode()
        print(f"Risposta dal server: {response}")

    client.close()
    print("Connessione chiusa dal client")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 run_client.py <server_ip> <port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])

    connect_to_server(server_ip, port, num_messages=3)

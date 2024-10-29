import socket

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)  # Il server accetta fino a 5 connessioni simultanee
    print(f"Server in ascolto sulla porta {port}")

    while True:
        conn, addr = server.accept()
        print(f"Connessione accettata da {addr}")
        count = 1
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    # Se non ci sono più dati, chiude la connessione
                    break
                print(f"Ricevuto dal client: {data}")
                response = "Risposta automatica dal server" + str(count)
                conn.send(response.encode())
                print(f"Inviato al client: {response}")
                count += 1
        except ConnectionResetError:
            print("Connessione chiusa dal client.")
        finally:
            conn.close()
            print("Connessione terminata con", addr)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9090
    start_server(port)

import socket

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5) 
    print(f"Server listening on port: {port}")

    while True:
        conn, addr = server.accept()
        print(f"Accepted connection {addr}")
        count = 1
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Message from client: {data}")
                response = "Acknowledge message from server" + str(count)
                conn.send(response.encode())
                print(f"Sent to the client {response}")
                count += 1
        except ConnectionResetError:
            print("Connection Closed by the client.")
        finally:
            conn.close()
            print("Connection terminated with", addr)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9090
    start_server(port)

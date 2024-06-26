import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 45000


class TimeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []

    def handle_client(self, client_socket):
        print("Client connected")
        while True:
            try:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break
                if data.strip() == "QUIT":
                    break
                if data.startswith("TIME") and data.endswith("\r\n"):
                    current_time = time.strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    client_socket.sendall(response.encode("utf-8"))
            except Exception as e:
                print("Error:", e)
                break

        client_socket.close()
        print("Client disconnected")

    def start(self):
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server stopped")

if __name__ == "__main__":
    host = HOST
    port = PORT
    server = TimeServer(host, port)
    server.start()
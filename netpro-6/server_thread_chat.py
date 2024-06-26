from socket import *
import socket
import threading
import json
import logging
from chat import Chat

chatserver = Chat()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('server')


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address

    def run(self):
        rcv = ""
        while True:
            try:
                data = self.connection.recv(32)
                if data:
                    d = data.decode()
                    rcv += d
                    if rcv[-2:] == '\r\n':
                        logger.info(f"Data dari client {self.address}: {rcv}")
                        hasil = chatserver.proses(rcv)
                        hasil = json.dumps(hasil) + "\r\n\r\n"
                        logger.info(f"Balas ke client {self.address}: {hasil}")
                        self.connection.sendall(hasil.encode())
                        rcv = ""
                else:
                    break
            except ConnectionResetError:
                logger.warning(f"Koneksi dari client {self.address} terputus.")
                break
            except Exception as e:
                logger.error(f"Terjadi kesalahan: {e}")
                break

        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 8889))
        self.my_socket.listen(1)
        logger.info("Server sudah siap menerima koneksi...")
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logger.info(f"Koneksi dari {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()

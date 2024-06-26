import socket

def main():
    host = "0.0.0.0"
    port = 45000

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Connected to server")

        while True:
            request = input("Enter 'TIME' to get current time or 'QUIT' to exit: ")
            if request.upper() == "QUIT":
                client_socket.sendall("QUIT\r\n".encode("utf-8"))
                break
            elif request.upper() == "TIME":
                client_socket.sendall("TIME\r\n".encode("utf-8"))
                response = client_socket.recv(1024).decode("utf-8")
                print("Server response:", response.strip())
            else:
                print("Invalid command. Please enter 'TIME' or 'QUIT'.")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()

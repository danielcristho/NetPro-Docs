import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    try:
        with open(filename, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode()
        command_str = f"UPLOAD {filename} {file_content}"
        hasil = send_command(command_str)
        if hasil['status'] == 'OK':
            print(hasil['data'])
            return True
        else:
            print("Gagal")
            return False
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(hasil['data'])
        return True
    else:
        print("Gagal")
        return False

def print_menu():
    print("File Client Menu:")
    print("1. List files")
    print("2. Get file")
    print("3. Upload file")
    print("4. Delete file")
    print("5. Exit")

def main():
    global server_address

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            remote_list()
        elif choice == "2":
            filename = input("Enter the filename to get: ")
            remote_get(filename)
        elif choice == "3":
            filename = input("Enter the filename to upload: ")
            if remote_upload(filename):
                print(f"File {filename} uploaded successfully.")
        elif choice == "4":
            filename = input("Enter the filename to delete: ")
            if remote_delete(filename):
                print(f"File {filename} deleted successfully.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    server_address = ('0.0.0.0', 6666)
    main()
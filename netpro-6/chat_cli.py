import socket
import json
import sys

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP, TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid = ""

    def proses(self, cmdline):
        j = cmdline.split(" ")
        try:
            command = j[0].strip()
            if command == 'register':
                username = j[1].strip()
                nama = j[2].strip()
                negara = j[3].strip()
                realm = j[4].strip()
                password = j[5].strip()
                return self.register(username, nama, negara, realm, password)
            elif command == 'auth':
                username = j[1].strip()
                password = j[2].strip()
                return self.login(username, password)
            elif command == 'send':
                usernameto = j[1].strip()
                message = " ".join(j[2:])
                return self.sendmessage(usernameto, message)
            elif command == 'inbox':
                return self.inbox()
            elif command == 'create_group':
                groupname = j[1].strip()
                return self.create_group(groupname)
            elif command == 'join_group':
                groupname = j[1].strip()
                return self.join_group(groupname)
            elif command == 'send_group':
                groupname = j[1].strip()
                message = " ".join(j[2:])
                return self.send_group_message(groupname, message)
            elif command == 'help':
                self.show_help()
                return {'status': 'OK', 'message': 'Menampilkan daftar perintah.'}
            elif command == 'exit':
                return self.exit()
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self, string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(64)
                if data:
                    receivemsg += data.decode()
                    if receivemsg[-4:] == '\r\n\r\n':
                        return json.loads(receivemsg)
        except Exception as e:
            self.sock.close()
            return {'status': 'ERROR', 'message': f'Gagal: {e}'}

    def show_help(self):
        print("\nDaftar Perintah:")
        print("auth <username> <password>: Untuk melakukan autentikasi.")
        print("register <username> <'nama'> <negara> <realm>: Untuk melakukan autentikasi.")
        print("send <username_tujuan> <username_asal> <pesan>: Untuk mengirim pesan ke pengguna lain.")
        print("inbox: Untuk melihat pesan yang masuk.")
        print("create_group <nama_group>: Untuk membuat group baru")
        print("join_group <nama_group>: Untuk gabung ke group")
        print("send_group <nama_group> <pesan>")
        print("help: Untuk menampilkan daftar perintah.")
        print("exit: Untuk keluar dari aplikasi.\n")

    def register(self, username, nama, negara, realm, password):
        string = f"register {username} {nama} {negara} {realm} {password} \r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return f"User {username} registered successfully"
        else:
            return f"Error, {result['message']}"

    def login(self, username, password):
        string = f"auth {username} {password}\r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.tokenid = result['tokenid']
            return f"Username {username} logged in, token {self.tokenid}"
        else:
            return f"Error, {result['message']}"

    def sendmessage(self, usernameto, message):
        if self.tokenid == "":
            return "Error, not authorized"
        string = f"send {self.tokenid} {usernameto} {message} \r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return f"message sent to {usernameto}"
        else:
            return f"Error, {result['message']}"

    def inbox(self):
        if self.tokenid == "":
            return "Error, not authorized"
        string = f"inbox {self.tokenid} \r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return json.dumps(result['messages'])
        else:
            return f"Error, {result['message']}"

    def create_group(self, groupname):
        if self.tokenid == "":
            return "Error, not authorized"
        string = f"create_group {self.tokenid} {groupname} \r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return f"Group {groupname} created"
        else:
            return f"Error, {result['message']}"

    def join_group(self, groupname):
        if self.tokenid == "":
            return "Error, not authorized"
        string = f"join_group {self.tokenid} {groupname} \r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return f"Joined group {groupname}"
        else:
            return f"Error, {result['message']}"

    def send_group_message(self, groupname, message):
        if self.tokenid == "":
            return "Error, not authorized"
        string = f"send_group {self.tokenid} {groupname} {message} \r\n"
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return f"Message sent to group {groupname}"
        else:
            return f"Error, {result['message']}"

    def exit(self):
        self.sock.close()
        return "User telah logout"

if __name__ == "__main__":
    cc = ChatClient()
    while True:
        cmdline = input(f"Command {cc.tokenid}: ")
        print(cc.proses(cmdline))
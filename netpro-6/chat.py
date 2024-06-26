import json
import uuid
import logging
import sys
from queue import Queue

class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.groups = {}
        self.setup_users()

    def setup_users(self):
        self.users['messi'] = {'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'miami', 'realm': 'earthrealm', 'incoming': {}, 'outgoing': {}}
        self.users['henderson'] = {'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'realm': 'earthrealm', 'incoming': {}, 'outgoing': {}}
        self.users['lineker'] = {'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya', 'realm': 'earthrealm', 'incoming': {}, 'outgoing': {}}
        # self.users['neymar'] = {'nama': 'Neymar Jr', 'negara': 'Brazil', 'password': 'santos', 'realm': 'edenia', 'incoming': {}, 'outgoing': {}}

    def proses(self, data):
        j = data.split(" ")
        try:
            command = j[0].strip()
            if command == 'register':
                username = j[1].strip()
                nama = j[2].strip()
                negara = j[3].strip()
                realm = j[4].strip()
                password = j[5].strip()
                logging.warning(f"REGISTER: register {username} {password}")
                return self.register_user(username, nama, negara, password, realm)
            elif command == 'auth':
                username = j[1].strip()
                password = j[2].strip()
                return self.autentikasi_user(username, password)
            elif command == 'send':
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = " ".join(j[3:])
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning(f"SEND: session {sessionid} send message from {usernamefrom} to {usernameto}")
                return self.send_message(sessionid, usernamefrom, usernameto, message)
            elif command == 'inbox':
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning(f"INBOX: {sessionid}")
                return self.get_inbox(username)
            elif command == 'create_group':
                sessionid = j[1].strip()
                groupname = j[2].strip()
                logging.warning(f"CREATE_GROUP: session {sessionid} create group {groupname}")
                return self.create_group(sessionid, groupname)
            elif command == 'join_group':
                sessionid = j[1].strip()
                groupname = j[2].strip()
                logging.warning(f"JOIN_GROUP: session {sessionid} join group {groupname}")
                return self.join_group(sessionid, groupname)
            elif command == 'send_group':
                sessionid = j[1].strip()
                groupname = j[2].strip()
                message = " ".join(j[3:])
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning(f"SEND_GROUP: session {sessionid} send message from {usernamefrom} to group {groupname}")
                return self.send_group_message(sessionid, usernamefrom, groupname, message)
            elif command == 'inbox_group':
                sessionid = j[1].strip()
                groupname = j[2].strip()
                logging.warning(f"INBOX_GROUP: session {sessionid} inbox group {groupname}")
                return self.get_group_inbox(sessionid, groupname)
            elif command == 'send_private':
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = " ".join(j[3:])
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning(f"SEND_PRIVATE: session {sessionid} send private message from {usernamefrom} to {usernameto}")
                return self.send_private_message(sessionid, usernamefrom, usernameto, message)
            elif command == 'inbox_private':
                sessionid = j[1].strip()
                logging.warning(f"INBOX_PRIVATE: session {sessionid} inbox private messages")
                return self.get_private_inbox(sessionid)
            elif command == 'exit':
                logging.warning("EXIT: Pengguna keluar dari aplikasi.")
                sys.exit()
            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        if username not in self.users:
            return {'status': 'ERROR', 'message': 'User Tidak Ada'}

        if self.users[username]['password'] != password:
            return {'status': 'ERROR', 'message': 'Password Salah'}

        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {'username': username, 'userdetail': self.users[username]}

        return {'status': 'OK', 'tokenid': tokenid}


    def register_user(self, username, nama, negara, password, realm):
        if username in self.users:
            return {'status': 'ERROR', 'message': 'User Sudah Ada'}

        self.users[username] = {
            "nama": nama,
            "negara": negara,
            "password": password,
            "realm": realm,
            "incoming": {},
            "outgoing": {},
        }

        return {'status': 'OK', 'message': 'User Berhasil Ditambahkan'}

    def get_user(self, username):
        if username not in self.users:
            return False
        return self.users[username]

    def send_message(self, sessionid, username_from, username_dest, message):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if s_fr == False or s_to == False:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        if s_fr['realm'] != s_to['realm']:
            return {'status': 'ERROR', 'message': 'User tidak dapat mengirim pesan ke realm yang berbeda'}

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[username_dest].put(message)
        except KeyError:
            outqueue_sender[username_dest] = Queue()
            outqueue_sender[username_dest].put(message)
        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def get_inbox(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())

        return {'status': 'OK', 'messages': msgs}

    def create_group(self, sessionid, groupname):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if groupname in self.groups:
            return {'status': 'ERROR', 'message': 'Group Sudah Ada'}
        self.groups[groupname] = {'members': []}
        return {'status': 'OK', 'message': f'Group {groupname} created'}

    def join_group(self, sessionid, groupname):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if groupname not in self.groups:
            return {'status': 'ERROR', 'message': 'Group Tidak Ditemukan'}
        username = self.sessions[sessionid]['username']
        if username in self.groups[groupname]['members']:
            return {'status': 'ERROR', 'message': 'Sudah menjadi anggota grup ini'}
        self.groups[groupname]['members'].append(username)
        return {'status': 'OK', 'message': f'Bergabung ke grup {groupname}'}

    def send_group_message(self, sessionid, username_from, groupname, message):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if groupname not in self.groups:
            return {'status': 'ERROR', 'message': 'Group Tidak Ditemukan'}

        s_fr = self.get_user(username_from)
        if not s_fr:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = {'msg_from': s_fr['nama'], 'msg_to': groupname, 'msg': message}
        members = self.groups[groupname]['members']
        for member in members:
            s_to = self.get_user(member)
            if s_to:
                inqueue_receiver = s_to['incoming']
                try:
                    inqueue_receiver[username_from].put(message)
                except KeyError:
                    inqueue_receiver[username_from] = Queue()
                    inqueue_receiver[username_from].put(message)

        return {'status': 'OK', 'message': f'Pesan terkirim ke grup {groupname}'}

    def get_group_inbox(self, sessionid, groupname):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if groupname not in self.groups:
            return {'status': 'ERROR', 'message': 'Group Tidak Ditemukan'}

        group_msgs = []
        members = self.groups[groupname]['members']

        for member in members:
            user = self.get_user(member)
            if user:
                incoming = user['incoming'].get(groupname, [])
                while not incoming.empty():
                    group_msgs.append(incoming.get_nowait())

        return {'status': 'OK', 'messages': group_msgs}

    def send_private_message(self, sessionid, username_from, username_to, message):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_to)

        if not s_fr or not s_to:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']

        try:
            outqueue_sender[username_to].put(message)
        except KeyError:
            outqueue_sender[username_to] = Queue()
            outqueue_sender[username_to].put(message)

        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)

        return {'status': 'OK', 'message': 'Pesan pribadi terkirim'}

    def get_private_inbox(self, sessionid):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}

        username = self.sessions[sessionid]['username']
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = {}

        for user, messages in incoming.items():
            msgs[user] = []
            while not messages.empty():
                msgs[user].append(messages.get_nowait())

        return {'status': 'OK', 'messages': msgs}

if __name__ == "__main__":
    j = Chat()
    while True:
        data = input("Command : ")
        hasil = j.proses(data)
        print(json.dumps(hasil))

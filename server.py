import socket
import threading
import pickle
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

HOST = '192.168.178.183'
PORT = 5555

clients = {}
public_keys = {}

# Server RSA Keys
server_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

server_public_key = server_private_key.public_key()


def broadcast_user_list():
    users = list(public_keys.keys())
    data = {
        'type': 'users',
        'users': users,
        'keys': {
            user: public_keys[user].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ) for user in public_keys
        }
    }

    for client in clients.values():
        client.send(pickle.dumps(data))


def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()

        public_key_data = client_socket.recv(4096)
        public_key = serialization.load_pem_public_key(public_key_data)

        clients[username] = client_socket
        public_keys[username] = public_key

        print(f"[+] {username} connected")

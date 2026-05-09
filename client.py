import socket
import threading
import pickle
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

HOST = '192.168.178.183'
PORT = 5555

# RSA Keys for Client
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

users = {}


def encrypt_message(message, receiver_public_key):
    encrypted = receiver_public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def decrypt_message(ciphertext):
    decrypted = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()


def receive_messages(client_socket):
    global users

    while True:
        try:
            data = client_socket.recv(8192)
            if not data:
                break

            message = pickle.loads(data)

            if message['type'] == 'users':
                users = {}

                for user, key_data in message['keys'].items():
                    users[user] = serialization.load_pem_public_key(key_data)

                print("\nConnected users:")
                for user in users:
                    print(f"- {user}")

            elif message['type'] == 'message':
                sender = message['from']
                encrypted_message = message['message']

                decrypted = decrypt_message(encrypted_message)
                print(f"\n[Encrypted message from {sender}] {decrypted}")

        except Exception as e:
            print(f"Receive error: {e}")
            break

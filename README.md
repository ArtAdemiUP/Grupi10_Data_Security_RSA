# Grupi10_Data_Security_RSA
# 🔐 RSA Encrypted Chat

A peer-to-peer encrypted chat application built with Python, using **RSA 2048-bit** end-to-end encryption. Messages are encrypted on the sender's machine and can only be decrypted by the intended recipient — the server never sees the plaintext.

---

1. Each client generates a **2048-bit RSA key pair** on startup.
2. Public keys are shared with the server, which distributes them to all connected users.
3. When sending a message, the sender **encrypts it with the recipient's public key**.
4. The server **forwards the ciphertext** without ever decrypting it.
5. Only the recipient, who holds the matching **private key**, can decrypt the message.

---

### `server.py`
- Accepts multiple simultaneous client connections (one thread per client)
- Stores each client's **public key** in memory
- Broadcasts the updated user list (with public keys) whenever someone joins or leaves
- Routes encrypted messages to the correct recipient — **reads no plaintext**

### `client.py`
- Generates a fresh RSA key pair on every run
- Registers username + public key with the server
- Receives the public keys of all online users
- Encrypts outgoing messages with the **recipient's public key** (OAEP + SHA-256)
- Decrypts incoming messages with its own **private key**

---

## Requirements

- Python 3.8+
- [`cryptography`](https://cryptography.io/) library

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/rsa-encrypted-chat.git
cd rsa-encrypted-chat

# 2. Install dependencies
pip install cryptography
```

---

## Usage

### 1. Configure the IP address

In both `server.py` and `client.py`, set `HOST` to the server machine's IP:

```python
HOST = '192.168.178.183'  # change to your server's IP
PORT = 5555
```

### 2. Start the server

```bash
python server.py
```

```
Server listening on 192.168.178.183:5555
```

### 3. Start a client (run in separate terminals for each user)

```bash
python client.py
```

```
Enter your username: Alice
```

### 4. Send a message

Once connected, you'll see a list of online users. To send a message:

```
Connected users:
- Alice
- Bob

Send to: Bob
Message: Hello Bob, this is encrypted!
```

You can run as many clients as you want simultaneously. Each one communicates independently.

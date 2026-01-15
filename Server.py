import socket
import hashlib

HOST = "0.0.0.0"
PORT = 57889

FLAG = "FLAG{crypt0_i5_th3_K3y_2026}"

hash_chain = [
    ("482c811da5d5b4bc6d497ffa98491e38", "password"),
    ("eca8e05d94c236e78c389e15e1cad71ff9326bdfa5e1d79d92766f38414e66e5", "qwerty098"),
    ("916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745", "letmin"),
]

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[+] Listening on port {PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            conn.send(b"Welcome!! Looking For the Secret?\n\n")

            for i, (h, answer) in enumerate(hash_chain):
                conn.send(f"We have identified a hash: {h}\n".encode())
                conn.send(b"Enter the password for identified hash: ")

                user = conn.recv(1024).decode().strip()

                if len(h) == 32:      # MD5
                    valid = md5(user) == h
                else:                 # SHA256
                    valid = sha256(user) == h

                if not valid:
                    conn.send(b"\n❌ Incorrect password. Bye!\n")
                    break

                conn.send(b"\n✅ Correct!\n\n")

            else:
                conn.send(b"🎉 All hashes solved!\n")
                conn.send(f"FLAG: {FLAG}\n".encode())

import socket
import hashlib

HOST = "0.0.0.0"
PORT = 57889

FLAG = "FLAG{crypto_progression}"

challenges = [
    ("eca8e05d94c236e78c389e15e1cad71ff9326bdfa5e1d79d92766f38414e66e5", "crypto"),
    ("916e8c4f79b25028c9e467f1eb8eee6d6bbdff965f9928310ad30a8d88697745", "is"),
    ("e7cb7a3068654b3ecf1fd0d571a81271a2fde4bfbbd451072f1061f4b45744cd", "fun"),
]

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[+] Listening on {PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            conn.send(b"=== SHA-256 Sequential Challenge ===\n\n")

            for i, (hash_value, answer) in enumerate(challenges, 1):
                conn.send(f"🔐 Hash {i}:\n{hash_value}\n".encode())
                conn.send(b"Enter plaintext: ")

                user_input = conn.recv(1024).decode().strip()

                if sha256(user_input) != hash_value:
                    conn.send(b"\n❌ Incorrect. Connection closed.\n")
                    break

                conn.send(b"✅ Correct!\n\n")

            else:
                conn.send(b"🎉 All hashes solved!\n")
                conn.send(f"FLAG: {FLAG}\n".encode())

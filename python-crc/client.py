# import socket
# import zlib

# HOST = "127.0.0.1"   # Server IP
# PORT = 5000

# # Client firmware
# with open("data.txt", "rb") as f:
#     firmware = f.read()

# crc = zlib.crc32(firmware) & 0xFFFFFFFF

# crc_hex = f"{crc:08X}"

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((HOST, PORT))

# client.sendall(crc_hex.encode())

# response = client.recv(1024)

# print("Server Response:", response.decode())

# client.close()

import socket
import zlib

HOST = "127.0.0.1"
PORT = 5000

LOCAL_FILE = "data_test.txt"

# Calculate CRC of local firmware
with open(LOCAL_FILE, "rb") as f:
    data = f.read()

crc = zlib.crc32(data) & 0xFFFFFFFF

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Send CRC
client.sendall(f"{crc:08X}".encode())

response = client.recv(32)

print("Server:", response.decode())

if response == b"HELLO":

    client.sendall(b"READY")

    # Receive file size
    filesize = int.from_bytes(client.recv(8), "big")

    received = 0

    with open("data.txt", "wb") as f:

        while received < filesize:

            chunk = client.recv(1024)

            if not chunk:
                break

            f.write(chunk)
            received += len(chunk)
            print(chunk)

            print(f"{received}/{filesize} bytes")

    print("Download Complete")

client.close()
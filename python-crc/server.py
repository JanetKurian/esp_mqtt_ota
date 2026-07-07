# import socket
# import zlib

# HOST = "0.0.0.0"      # Listen on all interfaces
# PORT = 5000

# # Firmware stored on the server
# with open("data.txt", "rb") as f:
#     firmware = f.read()

# server_crc = zlib.crc32(firmware) & 0xFFFFFFFF

# print(f"Server CRC : {server_crc:08X}")

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen(1)

# print(f"Server listening on port {PORT}")

# while True:
#     conn, addr = server.accept()
#     print(f"Connected by {addr}")

#     # Receive CRC from client
#     data = conn.recv(8)          # Expecting 8 ASCII hex characters

#     client_crc = int(data.decode(), 16)

#     print(f"Client CRC : {client_crc:08X}")

#     if client_crc == server_crc:
#         conn.sendall(b"HELLO")
#         print("CRC Match")
#     else:
#         conn.sendall(b"CRC_FAIL")
#         print("CRC Mismatch")

#     conn.close()

import socket
import zlib
import os

HOST = "0.0.0.0"
PORT = 5000
CHUNK_SIZE = 1024

FIRMWARE_FILE = "data_test.txt"

# Calculate server CRC
with open(FIRMWARE_FILE, "rb") as f:
    firmware = f.read()

server_crc = zlib.crc32(firmware) & 0xFFFFFFFF

print(f"Server CRC : {server_crc:08X}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")

while True:

    conn, addr = server.accept()
    print(f"\nConnected : {addr}")

    # Receive CRC from client
    client_crc = conn.recv(8).decode()

    print("Client CRC :", client_crc)

    if int(client_crc, 16) == server_crc:

        conn.sendall(b"HELLO")

        # Wait until client is ready
        ready = conn.recv(16)

        if ready == b"READY":

            filesize = os.path.getsize(FIRMWARE_FILE)

            # Send file size (8 bytes)
            conn.sendall(filesize.to_bytes(8, "big"))

            with open(FIRMWARE_FILE, "rb") as f:

                while True:

                    chunk = f.read(CHUNK_SIZE)

                    if not chunk:
                        break

                    conn.sendall(chunk)

            print("Firmware sent.")

    else:

        conn.sendall(b"CRC_FAIL")

    conn.close()
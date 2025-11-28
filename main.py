# Made by tienanh109 ^-^

import socket
import struct
import time

HOST = "0.0.0.0" # ip, 0.0.0.0 if u run local
PORT = 19132  # sv port
MOTD = "tienanh109dz fr"
PROTOCOL = 84 # 0.15.10 protocol ver
VERSION_NAME = "0.15.10" # u know lol
ONLINE = 0
MAX_PLAYERS = 20
SERVER_ID = 1234567890123456789  # long

# Magic bytes for offline message id (RakNet), jst nvm ts if u dont know
MAGIC = bytes.fromhex("00ffff00fefefefefdfdfdfd12345678")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("Fake MCPE server running at 0.0.0.0:19132, made by tienanh109")

while True:
    data, addr = sock.recvfrom(2048)
    if len(data) < 1:
        continue
    packet_id = data[0]
    # Unconnected Ping = 0x01
    if packet_id == 0x01:
        # extract client timestamp (ulong long, 8 bytes)
        # data layout: 0x01 | time (8) | magic (16) | client GUID (8)
        try:
            # echo back timestamp, then server GUID, then magic, then payload string
            client_time = data[1:9]
            pong = b'\x1c' + client_time
            pong += struct.pack(">Q", SERVER_ID) # server GUID 8 bytes BE/LE tùy doc
            pong += MAGIC
            # payload: the “server list string”
            # format: Edition;MOTD;Protocol;VersionName;Online;Max;ServerId;MOTD2;GameMode;GameModeNum;PortIPv4;PortIPv6
            s = f"MCPE;{MOTD};{PROTOCOL};{VERSION_NAME};{ONLINE};{MAX_PLAYERS};{SERVER_ID};{MOTD};Survival;1;{PORT};0;"
            pong += struct.pack(">H", len(s)) + s.encode('utf-8')
            sock.sendto(pong, addr)
            print("Responded pong to", addr)
        except Exception as e:
            print("Error building pong:", e)
    else:
        # ignore other packets
        pass
      

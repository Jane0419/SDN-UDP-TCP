# udpserver.py
import socket
import random
import time
import struct

# 配置选项
server_ip = "0.0.0.0"  # ip
server_port = 12345  # 端口
rate = 0.5  # 可能性
size = 1024  # 缓冲区


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))
    print(f"接收 {server_ip}:{server_port}")

    while True:
        # 接收request + ip、端口号
        client_request, inf = server_socket.recvfrom(size)

        # 随机丢包
        if random.random() < rate:
            print(f"丢包")
            continue

        # 序列号、版本号
        sequence_number, ver = struct.unpack('!HB', client_request[:3])

        # 时间
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        current_time = time.strftime('%H-%M-%S', local_time).encode('utf-8')

        # 序列号、版本号、时间
        response = struct.pack('!HB', sequence_number, ver) + current_time
        server_socket.sendto(response, inf)

        print(f"响应 {inf}，序列号: {sequence_number}")


if __name__ == "__main__":
    main()

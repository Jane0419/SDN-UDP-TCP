# udpclient.py
import socket
import time
import struct
import sys
import statistics

# 配置选项
nums = 12  # request
timeout = 0.1  # 100ms
max_retry = 2  # 重传

server_ip = sys.argv[1]
server_port = int(sys.argv[2])


# python udpclient.py 192.168.128.128 12345
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)

    bag = 0
    rtts = []
    time_begin = None
    time_end = None
    ver = 2
    server_time = f"**-**-**"

    for sequence_number in range(1, nums + 1):
        retry = 0
        while retry <= max_retry:
            # 请求，sequence_number、ver、其他内容
            message = struct.pack('!I B', sequence_number, ver) + b'others'
            time_send = time.time()  # 发送时间

            try:
                # 发送request + ip、端口号
                client_socket.sendto(message, (server_ip, server_port))
                # 接收response 序列号、版本号、时间
                response, _ = client_socket.recvfrom(1024)
                time_receive = time.time()  # 接收时间
                rtt = (time_receive - time_send) * 1000  # RTT（ms）
                numbers, _ = struct.unpack('!I B', response[:5])  # 序列号
                server_time = response[5:].decode('utf-8')  # 服务器时间

                if time_begin is None:
                    time_begin = time_receive  # 响应开始
                time_end = time_receive  # 响应结束
                bag += 1
                rtts.append(rtt)
                print(f"sequence no:{numbers},serverIP:{server_ip},RTT:{rtt:.2f}ms")
                break

            except socket.timeout:  # 重传
                retry += 1
                if retry > max_retry:  # 超时
                    print(f"sequence no:{sequence_number},request time out")
                else:
                    print("重传中……")

    if rtts:
        rtt_max = max(rtts)
        rtt_min = min(rtts)
        rtt_average = sum(rtts) / len(rtts)
        rtt_sd = statistics.stdev(rtts)  # 标准差
        total = (time_end - time_begin) * 1000  # 整体响应时间（ms）
    else:
        rtt_max = rtt_min = rtt_average = rtt_sd = total = 0

    print(f"\n【汇总】信息:")
    print(f"服务器时间: {server_time}")
    print(f"接收到的 udp packets 数目: {bag}")
    print(f"丢包率: {(1 - bag / nums) * 100:.2f}%")
    print(f"最大RTT: {rtt_max:.2f} ms")
    print(f"最小RTT: {rtt_min:.2f} ms")
    print(f"平均RTT: {rtt_average:.2f} ms")
    print(f"RTT的标准差: {rtt_sd:.2f} ms")
    print(f"server的整体响应时间: {total:.2f} ms")

    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"用法: {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(1)
    main()

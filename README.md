
UDP socket programming
概述
这是一个基于UDP协议的client-server程序，模拟了TCP连接的建立过程。
client端向server端发送12个请求数据包，server端接收到请求后进行响应，随机丢包。
client端设置了超时时间，若在100ms内未收到server端响应则进行重传，两次重传失败则放弃。
最后输出汇总信息，包括接收到的数据包数目、丢包率、RTT和server端响应时间。

运行环境
Python 3.8.10

配置选项
server_ip：服务器的ip地址，默认为"0.0.0.0"。
server_port：服务器监听的端口，默认为12345。
rate：丢包概率，默认为20%。 
size：缓冲区的大小，默认为1024Bytes。
nums：发送的请求次数，默认为12次。
timeout：超时时间，默认为100毫秒。
max_retry：最大重传次数，默认为2次。

运行方式
guest os上，
python3 udpserver.py
host os的命令行方式下，
python udpclient.py <server_ip> <server_port>

注意事项
请确保udpserver.py在udpclient.py运行之前已经启动，并且udpserver.py的ip地址和端口与udpclient.py一致。



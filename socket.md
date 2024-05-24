socket是什么：

Socket是应用层与TCP/IP协议族通信的中间软件抽象层，它是一组接口。在设计模式中，Socket其实就是一个门面模式，它把复杂的TCP/IP协议族隐藏在Socket接口后面，对用户来说，一组简单的接口就是全部，让Socket去组织数据，以符合指定的协议。

所以，我们无需深入理解tcp/udp协议，socket已经为我们封装好了，我们只需要遵循socket的规定去编程，写出的程序自然就是遵循tcp/udp标准的。
 套接字分类：1、基于文件类型的套接字家族；套接字家族的名字：AF_UNIX
                        2、基于网络类型的套接字家族；套接字家族的名字：AF_INET

先从服务器端说起。服务器端先初始化Socket，然后与端口绑定(bind)，对端口进行监听(listen)，调用accept阻塞，等待客户端连接。在这时如果有个客户端初始化一个Socket，然后连接服务器(connect)，如果连接成功，这时客户端与服务器端的连接就建立了。客户端发送数据请求，服务器端接收请求并处理请求，然后把回应数据发送给客户端，客户端读取数据，最后关闭连接，一次交互结束。

示例代码：

```python
import socket
import base64
#server
IP = '127.0.0.1' #ip
PORT = 8000 #端口
BUFLEN = 512 #缓冲区一次读入的数据数

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#AF_INET代表使用的是ip协议
#SOCK_STREAM代表使用的是tcp协议
#上面语句相当于创建了一个套接字（socket，并且指定这个socket使用的协议和标准
#绑定端口和地址
server.bind((IP,PORT))

server.listen(2)
#最多连接两个客户端，把服务器置于listen状态

print(f'服务器创建成功')
data,address = server.accept()
#accept阻塞状态，意思是服务端不执行代码，等待客户端链接，什么时候客户端连接什么时候才能继续执行代码
#对于两个返回值：accept接受连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。
while True:
    receive = data.recv(BUFLEN)

    if not receive:
        break

    info = receive.decode('utf-8')
    info1 =base64.b64decode(info)#对数据进行解码
    print(info1)

data.close()
server.close()
#关闭两个套接字，结束进程
```

```python
import socket
import base64
#client
IP = '127.0.0.1' #ip
PORT = 8000 #端口
BUFLEN = 512 #缓冲区一次读入的数据数

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#AF_INET代表使用的是ip协议
#SOCK_STREAM代表使用的是tcp协议
#上面语句相当于创建了一个套接字（socket，并且指定这个socket使用的协议和标准
#连接服务端的端口和地址
client.connect((IP,PORT))

print(f'客户端连接成功')

while True:
    msg = input('>>> ')

    client.send(base64.b64encode(msg.encode('utf-8')))

    received= client.recv(BUFLEN)
    if not received:
        break
    received1=received.decode('utf-8')
    print(base64.b64decode(received))

client.close()
#关闭进程
```

注解：1.注意传出和读入需要进行utf-8编解码

2.先驱动服务端再启动客户端

3.本代码只是采用base64加密解密方式，还可以采用其他方式进行加解密通信

常用的方法：

**sk.bind(address)**

　　s.bind(address) 将套接字绑定到地址。address地址的格式取决于地址族。在AF_INET下，以元组（host,port）的形式表示地址。

**sk.listen(backlog)**

　　开始监听传入连接。backlog指定在拒绝连接之前，可以挂起的最大连接数量。

   backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
    这个值不能无限大，因为要在内核中维护连接队列

**sk.setblocking(bool)**

　　是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。

**sk.accept()**

　　接受连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。

　　接收TCP 客户的连接（阻塞式）等待连接的到来

**sk.connect(address)**

　　连接到address处的套接字。一般，address的格式为元组（hostname,port）,如果连接出错，返回socket.error错误。

**sk.connect_ex(address)**

　　同上，只不过会有返回值，连接成功时返回 0 ，连接失败时候返回编码，例如：10061

**sk.close()**

　　关闭套接字

**sk.recv(bufsize[,flag])**

　　接受套接字的数据。数据以字符串形式返回，bufsize指定**最多**可以接收的数量。flag提供有关消息的其他信息，通常可以忽略。

**sk.recvfrom(bufsize[.flag])**

　　与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。

**sk.send(string[,flag])**

　　将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。即：可能未将指定内容全部发送。

**sk.sendall(string[,flag])**

　　将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。

   内部通过递归调用send，将所有内容发送出去。

**sk.sendto(string[,flag],address)**

　　将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。该函数主要用于UDP协议。

**sk.settimeout(timeout)**

　　设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如 client 连接最多等待5s ）

**sk.getpeername()**

　　返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。

**sk.getsockname()**

　　返回套接字自己的地址。通常是一个元组(ipaddr,port)

**sk.fileno()**

　　套接字的文件描述符
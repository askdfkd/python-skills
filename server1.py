import socket
#加密算法RC4
def KSA(key):
    """ Key-Scheduling Algorithm (KSA) """
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S):
    """ Pseudo-Random Generation Algorithm (PRGA) """
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key, text):
    """ RC4 encryption/decryption """
    S = KSA(key)
    keystream = PRGA(S)
    res = []
    for char in text:
        res.append(char ^ next(keystream))
    return bytes(res)

#server
IP = '127.0.0.1' #ip
PORT = 8001 #端口
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
    key = b'encode_key'

    info =RC4(key, receive)#对数据进行解码
    info1 = info.decode('utf-8')
    print(info)

data.close()
server.close()
#关闭两个套接字，结束进程
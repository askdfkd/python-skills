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

#client
IP = '127.0.0.1' #ip
PORT = 8001 #端口
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
    key = b'encode_key'
    client.send(RC4(key,msg.encode('utf-8')))

    received= client.recv(BUFLEN)
    if not received:
        break
    received1=received.decode('utf-8')
    print(RC4(key,received))

client.close()
#关闭进程
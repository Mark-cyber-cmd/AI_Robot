#__author:   han-zhang
#date:  2018/12/23 10:21
#file:  server.py
#IDE:   PyCharm

import socket,threading

def c_thread(s_client,addr):
    print(addr,'成功连接') #打印连接者地址信息
    while True:
        data = s_client.recv(33) #接收客户端数据
        print('收到',addr,'信息为',data.hex())
        s_client.sendall(data)
        print('发送成功')
        if data == '再见':
            s_client.close()
            print('该子进程已关闭')
            break

#实例化
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#绑定端口
s.bind(('192.168.43.186',8000))
#监听
s.listen(10)
print('服务器上线')

while True:
    s_client,addr =s.accept()    #会话阻塞
    #创建子线程（执行与客户端的读写交互）
    sc_client = threading.Thread(target=c_thread,args=(s_client,addr))
    #启动子线程
    sc_client.start()
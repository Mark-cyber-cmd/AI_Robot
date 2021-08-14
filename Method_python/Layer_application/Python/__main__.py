# coding utf-8
import socket
import os
import shutil
import time
import threading
import Gyro as gyro
import Servo as servo


def setdir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)


if __name__ == '__main__':
    """           建立一个服务端            """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.43.186', 8000))
    server.listen(5)
    time_start = time.time()
    print("服务器准备就绪,等待客户端上线..........")
    """     清空临时数据文件夹 开启按键检测  """
    setdir("./Data/Data_tmp")
    while True:
        s_client, addr = server.accept()  # 不阻塞
        gyro_app = threading.Thread(target=gyro.gyro_thread, args=(s_client, addr))
        gyro_app.start()
        servo_app = threading.Thread(target=servo.bus_thread, args=(s_client, addr))
        servo_app.start()

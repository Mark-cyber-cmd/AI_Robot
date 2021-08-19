# coding utf-8
import socket
import threading
import time
import Gyro as gyro
import Servo as servo
import Control as control
if __name__ == '__main__':

    """     清空临时数据文件夹 开启按键检测  """
    control.setdir("./Data/Data_tmp")

    """           建立一个服务端            """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.43.186', 8000))
    server.listen(5)
    
    """         设置系统开始工作时间        """
    time_start = time.time()
    print("服务器准备就绪,等待客户端上线..........")
    while True:
        s_client, addr = server.accept()  # 不阻塞
        gyro_app = threading.Thread(target=gyro.gyro_thread, args=(s_client, addr))
        gyro_app.start()
        servo_app = threading.Thread(target=servo.bus_thread, args=(s_client, addr))
        servo_app.start()

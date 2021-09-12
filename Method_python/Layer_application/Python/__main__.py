# coding utf-8
import threading
from Gyro import *
from Robot import *
from Control import *


if __name__ == '__main__':

    """     清空临时数据文件夹 开启按键检测  """
    setdir("./Data/Data_tmp")

    connect_wifi("AI_Robot", "88888888")
    server = server_init(8000)  # 自动获取本机ip 并在8000端口创建服务器
    """建立控制对象"""
    gyro_1 = Gyro(server)
    gyro_2 = Gyro(server)
    gyro_3 = Gyro(server)
    gyro_4 = Gyro(server)
    gyro_1.connect(1)
    gyro_2.connect(2)
    gyro_3.connect(3)
    gyro_4.connect(4)

    robot = Robot(server)
    robot.connect()

    gyro_1_app = threading.Thread(target=gyro_1.activate(), args=())
    gyro_1_app.start()
    gyro_2_app = threading.Thread(target=gyro_2.activate(), args=())
    gyro_2_app.start()
    gyro_3_app = threading.Thread(target=gyro_3.activate(), args=())
    gyro_3_app.start()
    gyro_4_app = threading.Thread(target=gyro_4.activate(), args=())
    gyro_4_app.start()
    robot_app = threading.Thread(target=control_main(gyro_1, gyro_2, gyro_3, gyro_4, robot), args=())
    robot_app.start()

# coding utf-8
from Control import *
import threading

"""   清空临时数据文件夹  """
setdir("./Data/Data_tmp")

if __name__ == '__main__':

    gyro_control_app = threading.Thread(target=control_gyro, args=())
    gyro_control_app.start()

    if Gyro.client_index[1 - 1] == 1 and Gyro.client_index[2 - 1] == 1:
        gyro_1_app = threading.Thread(target=gyro_1.activate, args=())
        gyro_1_app.start()

        gyro_2_app = threading.Thread(target=gyro_2.activate, args=())
        gyro_2_app.start()

    print("Main threading exit")


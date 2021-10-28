# coding utf-8
from Control import *

if __name__ == '__main__':

    """   清空临时数据文件夹  """
    setdir("./Data/Data_tmp")

    while 1:
        if connect_wifi("AI_Robot", "88888888"):
            break
        else:
            time.sleep(0.05)

    gyro_control_app = threading.Thread(target=control_gyro(), args=())
    gyro_control_app.start()

    # todo 以下代码均未执行 gyro_control_app进程卡死！！！
    print("我执行了")
    while 1:
        print(Gyro.client_index[3 - 1], Gyro.client_index[4 - 1])
        time.sleep(1)
        if Gyro.client_index[3 - 1] == 1 and Gyro.client_index[4 - 1] == 1:
            print("我执行了")
            gyro_3_app = threading.Thread(target=gyro_3.activate(), args=())
            gyro_3_app.start()

            gyro_4_app = threading.Thread(target=gyro_4.activate(), args=())
            gyro_4_app.start()
            break

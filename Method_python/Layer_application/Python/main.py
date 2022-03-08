# coding utf-8
from Control import *
from Display import *
from threading import Thread

"""   清空临时数据文件夹  """
setdir("./Data/Data_tmp")

""" 开启树莓派反向代理"""
# os.system("setsid sunny clientid 151150344278 &")

if __name__ == '__main__':

    connect_thread = Thread(target=connect_all, args=())
    connect_thread.setDaemon(True)
    connect_thread.start()

    print("Simulation open?")
    print('[Y] yes [N] no')
    print('>>', end=' ')
    if input() == 'Y':
        simulation_thread = Thread(target=simulation_start, args=())
        simulation_thread.setDaemon(True)
        simulation_thread.start()

    while 1:
        if (1 in Gyro.client_index) and (3 in Gyro.client_index) and robot.status:
            gyro_1_thread = Thread(target=gyro_1.activate, args=())
            gyro_1_thread.setDaemon(True)
            gyro_1_thread.start()

            gyro_3_thread = Thread(target=gyro_3.activate, args=())
            gyro_3_thread.setDaemon(True)
            gyro_3_thread.start()
            break

    control_thread = Thread(target=control_main, args=())
    control_thread.setDaemon(True)
    control_thread.start()

    display_main()

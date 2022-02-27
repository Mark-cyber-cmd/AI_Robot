# coding:utf-8
from threading import Thread
import socket
from Robot import *
from Gyro import *

'''Input: 连续字符串  Output： 二进制数据数组     '''


def format_data(gyro_data):
    gyro_data = gyro_data.split()
    data = []
    for i in range(len(gyro_data)):
        data.append(struct.pack('h', int(float(gyro_data[i]))))
    return data


def pack_data(data_roll, data_yaw, data_pitch):
    data = []
    len_min = min(len(data_roll), len(data_yaw), len(data_pitch))
    for i in range(len_min):
        data.append(b''.join([b'\x55\x53', data_roll[i], data_pitch[i], data_yaw[i], b'\x00\x00\x00']))
    return data


def simulated_gyro(gyro_data, s_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建客户端套接字
    client.connect(Adder)  # 发起TCP连接

    client.send(s_id)
    time.sleep(0.1)
    while 1:
        for i in gyro_data:
            client.send(i)


def simulated_robot(s_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建客户端套接字
    client.connect(Adder)  # 发起TCP连接

    client.send(s_id)
    time.sleep(0.1)
    while 1:
        pass


def simulation_start():
    simulated_gyro_1 = Thread(target=simulated_gyro, args=(gyro_data_1, Id_1))
    simulated_gyro_1.setDaemon(True)
    simulated_gyro_1.start()

    simulated_gyro_4 = Thread(target=simulated_gyro, args=(gyro_data_4, Id_3))
    simulated_gyro_4.setDaemon(True)
    simulated_gyro_4.start()

    simulated_Robot = Thread(target=simulated_robot, args=(Id_robot,))
    simulated_Robot.setDaemon(True)
    simulated_Robot.start()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while 1:
        try:
            s.connect(('198.168.1.1', 80))
            ip = s.getsockname()[0]
            break
        finally:
            s.close()
    return ip


HOST = get_ip()
PORT = 8000  # 通信端口号
BUF_siz = 1024  # 接收数据缓冲大小
Adder = (HOST, PORT)

Id_1 = b'\x55\x01\x01\x00\x00\x00\x00\x00\x00\x00'
Id_2 = b'\x55\x01\x02\x00\x00\x00\x00\x00\x00\x00'
Id_3 = b'\x55\x01\x03\x00\x00\x00\x00\x00\x00\x00'
Id_4 = b'\x55\x01\x04\x00\x00\x00\x00\x00\x00\x00'

Id_robot = b'\x55\x00\x01\x00\x00\x00\x00\x00\x00\x00'

with open('./Data/Data_base/zzm/大腿数据_8/gyro_roll1.txt', 'r') as f:
    gyro_data_roll1 = f.read()
    gyro_data_roll1 = format_data(gyro_data_roll1)
with open('./Data/Data_base/zzm/大腿数据_8/gyro_yaw1.txt', 'r') as f:
    gyro_data_yaw1 = f.read()
    gyro_data_yaw1 = format_data(gyro_data_yaw1)
with open('./Data/Data_base/zzm/大腿数据_8/gyro_pitch1.txt', 'r') as f:
    gyro_data_pitch1 = f.read()
    gyro_data_pitch1 = format_data(gyro_data_pitch1)


gyro_data_1 = pack_data(gyro_data_roll1, gyro_data_yaw1, gyro_data_pitch1)


with open('./Data/Data_base/zzm/大腿数据_3/gyro_roll4.txt', 'r') as f:
    gyro_data_roll4 = f.read()
    gyro_data_roll4 = format_data(gyro_data_roll4)
with open('./Data/Data_base/zzm/大腿数据_3/gyro_yaw4.txt', 'r') as f:
    gyro_data_yaw4 = f.read()
    gyro_data_yaw4 = format_data(gyro_data_yaw4)
with open('./Data/Data_base/zzm/大腿数据_3/gyro_pitch4.txt', 'r') as f:
    gyro_data_pitch4 = f.read()
    gyro_data_pitch4 = format_data(gyro_data_pitch4)

gyro_data_4 = pack_data(gyro_data_roll4, gyro_data_yaw4, gyro_data_pitch4)

if __name__ == '__main__':

    print('IP: ', HOST)
    print('Simulation start')

    simulation_start()

    while True:
        pass

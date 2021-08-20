import numpy as np
import os
import Gyro as gyro
import Servo as servo
import time
import shutil

"""                  神经网络控制参数                 """
w1 = np.loadtxt("./Data/BP_net/Net6/w1.txt", delimiter=" ", dtype="float")
w2 = np.loadtxt("./Data/BP_net/Net6/w2.txt", delimiter=" ", dtype="float")
b1 = np.loadtxt("./Data/BP_net/Net6/b1.txt", delimiter=" ", dtype="float")
b2 = np.loadtxt("./Data/BP_net/Net6/b2.txt", delimiter=" ", dtype="float")
b1 = np.array([b1.tolist()]).T
"""                  TCP客户端连接管理                """
client_index = {'bus': 0, 'gyro_1': 0, 'gyro_2': 0, 'gyro_3': 0, 'gyro_4': 0}
client_status = {'bus': False, 'gyro_1': False, 'gyro_2': False, 'gyro_3': False, 'gyro_4': False}
"""                      控制参数                     """
con_time = 100  # ms
N = 1  # 控制采样频率相对指令的倍数
gravity = 0


def control_algorithm():
    bus_data_s = [500, 500, 500, 500]
    global gravity

    if gyro.gyro_data['roll4'] - gyro.gyro_data_before['roll4'] > 0.1 and gravity == 0:
        servo.servo_move(client_index['bus'], [1, 4], 3, [440, 440], 200)
        time.sleep(0.2)
        servo.servo_move(client_index['bus'], [2, 3, 5, 6], 3, [500, 500, 500, 500], 500)  # 步距补偿
        time.sleep(0.5)
        gravity = 1

    if abs(gyro.gyro_data['roll4'] + gyro.gyro_data['roll1']) > 1 and gravity == 1:
        bus_data_s[0] = \
            500 + gyro.gyro_data['roll4'] / 270 * 1000
        bus_data_s[1] = \
            500 + gyro.gyro_data['roll4'] / 270 * 1000
        bus_data_s[2] = \
            500 + gyro.gyro_data['roll4'] / 270 * 1000
        bus_data_s[3] = \
            500 + gyro.gyro_data['roll4'] / 270 * 1000
        servo.servo_move(client_index['bus'], [2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(con_time / 1000)

        if gyro.gyro_data['roll4'] + 8 * gyro.gyro_data['roll1'] < 5:
            servo.servo_move(client_index['bus'], [1, 4], 3, [500, 500], 200)
            time.sleep(0.2)
            gravity = 0

    if gyro.gyro_data['roll1'] - gyro.gyro_data_before['roll1'] > 0.1 and gravity == 0:
        servo.servo_move(client_index['bus'], [1, 4], 3, [560, 560], 200)
        time.sleep(0.2)
        servo.servo_move(client_index['bus'], [2, 3, 5, 6], 3, [500, 500, 500, 500], 500)
        time.sleep(0.5)
        gravity = -1

    # data_set = [[gyro_data['ax1'], gyro_data['ay1'], gyro_data['az1'], gyro_data['ax4'],
    #             gyro_data['ay4'], gyro_data['az4'], gyro_data['roll1'], gyro_data['pitch1'],
    #             gyro_data['yaw1'], gyro_data['roll4'], gyro_data['pitch4'], gyro_data['yaw4']]]
    # data_set = np.array(data_set).T
    # if settle_down(data_set):
    #     servo_move(client_index['bus'], [1, 4], 3, [500, 500], 200)
    #     time.sleep(0.2)
    #     gravity = 0

    if abs(gyro.gyro_data['roll4'] + gyro.gyro_data['roll1']) > 1 and gravity == -1:
        bus_data_s[0] = \
            500 - gyro.gyro_data['roll1'] / 270 * 1000
        bus_data_s[1] = \
            500 - gyro.gyro_data['roll1'] / 270 * 1000
        bus_data_s[2] = \
            500 - gyro.gyro_data['roll1'] / 270 * 1000
        bus_data_s[3] = \
            500 - gyro.gyro_data['roll1'] / 270 * 1000
        servo.servo_move(client_index['bus'], [2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(con_time / 1000)

        if gyro.gyro_data['roll1'] + 8 * gyro.gyro_data['roll4'] < 5:
            servo.servo_move(client_index['bus'], [1, 4], 3, [500, 500], 200)
            time.sleep(0.2)
            gravity = 0
    return


# 创建激活函数sigmoid
def sigmoid(z):
    return 2 / (1 + np.exp(-2 * z)) - 1


def settle_down(data):
    step1 = np.dot(w1, data)
    step2 = sigmoid(step1 - b1)
    step3 = np.dot(w2, step2)
    step4 = sigmoid(step3 - b2)
    output = np.heaviside(step4 - 0.5, 1)
    return output


def setdir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)


def key_scan(self, flag):
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('space'):  # if key 'space' is pressed
            print('记录落脚一次')
            flag = 1
    except BaseException:
        pass  # if user pressed a key other than the given key the loop will break
    return flag
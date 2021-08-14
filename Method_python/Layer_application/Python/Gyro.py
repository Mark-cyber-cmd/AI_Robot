import keyboard
import math
import struct
import time
import Control as control
import Servo as servo
"""陀螺仪参数设置"""
command_setup_open = b'\xFF\xAA\x69\x88\xB5'
command_setup_zero = b'\xFF\xAA\x01\x08\x00'
command_setup_close = b'\xFF\xAA\x00\x00\x00'
command_setup_speed_100Hz = b'\xFF\xAA\x03\x09\x00'
command_setup_data_angel = b'\xFF\xAA\x02\x08\x00'
command_setup_data_all = b'\xFF\xAA\x02\x0A\x00'

"""陀螺仪数据"""
gyro_data = {'temper1': 0, 'roll1': 0, 'pitch1': 0, 'yaw1': 0, 'ax1': 0, 'ay1': 0, 'az1': 0, 'fps1': 0,
             'temper2': 0, 'roll2': 0, 'pitch2': 0, 'yaw2': 0, 'ax2': 0, 'ay2': 0, 'az2': 0, 'fps2': 0,
             'temper3': 0, 'roll3': 0, 'pitch3': 0, 'yaw3': 0, 'ax3': 0, 'ay3': 0, 'az3': 0, 'fps3': 0,
             'temper4': 0, 'roll4': 0, 'pitch4': 0, 'yaw4': 0, 'ax4': 0, 'ay4': 0, 'az4': 0, 'fps4': 0}
gyro_data_before = {'temper1': 0, 'roll1': 0, 'pitch1': 0, 'yaw1': 0, 'ax1': 0, 'ay1': 0, 'az1': 0, 'fps1': 0,
                    'temper2': 0, 'roll2': 0, 'pitch2': 0, 'yaw2': 0, 'ax2': 0, 'ay2': 0, 'az2': 0, 'fps2': 0,
                    'temper3': 0, 'roll3': 0, 'pitch3': 0, 'yaw3': 0, 'ax3': 0, 'ay3': 0, 'az3': 0, 'fps3': 0,
                    'temper4': 0, 'roll4': 0, 'pitch4': 0, 'yaw4': 0, 'ax4': 0, 'ay4': 0, 'az4': 0, 'fps4': 0}
"""绘图参数"""
gyro_address = r".\Data\Data_tmp"
servo_address = r".\Data\Data_tmp"
gravity_flag = 0


def gyro_thread(gyro_client, gyro_addr):
    global gravity_flag
    if gyro_addr[0] == '192.168.43.157' or gyro_addr[0] == '192.168.43.52' \
            or gyro_addr[0] == '192.168.43.28' or gyro_addr[0] == '192.168.43.38':
        gyro_client.send(command_setup_open)
        time.sleep(0.1)
        gyro_client.send(command_setup_zero)
        time.sleep(0.1)
        gyro_client.send(command_setup_speed_100Hz)
        time.sleep(0.1)
        gyro_client.send(command_setup_data_all)
        time.sleep(0.1)
        gyro_client.send(command_setup_close)
        time.sleep(0.1)
        raw_data = gyro_client.recv(11)
        client_id = raw_data[2]
        control.client_index['gyro_' + str(client_id)] = gyro_client
        control.client_status['gyro_' + str(client_id)] = True
        print("陀螺仪ID:", client_id, '成功连接并校准')
        time_before = time.time()
        time_start = time.time()
        fps = 0
        while True:
            try:
                raw_data = gyro_client.recv(11)
                gyro_data_before['roll' + str(client_id)] = gyro_data['roll' + str(client_id)]
                gyro_data_before['pitch' + str(client_id)] = gyro_data['roll' + str(client_id)]
                gyro_data_before['yaw' + str(client_id)] = gyro_data['roll' + str(client_id)]
                gravity_flag = key_scan(gravity_flag)
                if client_id == 1:
                    with open(gyro_address + r"\human_status.txt", "a") as f_hs:
                        f_hs.write(str(gravity_flag))
                        f_hs.write(" ")
                        gravity_flag = 0
                if raw_data[1] == 83:
                    gyro_data['roll' + str(client_id)] = \
                        struct.unpack('h', raw_data[2:4])[0] / 32768 * 180
                    gyro_data['pitch' + str(client_id)] = \
                        struct.unpack('h', raw_data[4:6])[0] / 32768 * 180
                    gyro_data['yaw' + str(client_id)] = \
                        struct.unpack('h', raw_data[6:8])[0] / 32768 * 180

                    if time.time() - time_before > 1:
                        time_before = time.time()
                        gyro_data['fps' + str(client_id)] = fps
                        print('fps' + str(client_id) + ": ", fps)
                        fps = 0
                    else:
                        fps = fps + 1

                    with open(gyro_address + r"\gyro_roll" + str(client_id) + ".txt", "a") as f_gyro_roll:
                        f_gyro_roll.write(str(gyro_data['roll' + str(client_id)]))
                        f_gyro_roll.write(" ")
                    with open(gyro_address + r"\gyro_pitch" + str(client_id) + ".txt", "a") as f_gyro_pitch:
                        f_gyro_pitch.write(str(gyro_data['pitch' + str(client_id)]))
                        f_gyro_pitch.write(" ")
                    with open(gyro_address + r"\gyro_yaw" + str(client_id) + ".txt", "a") as f_gyro_yaw:
                        f_gyro_yaw.write(str(gyro_data['yaw' + str(client_id)]))
                        f_gyro_yaw.write(" ")
                    with open(gyro_address + r"\gyro_angel_time" + str(client_id) + ".txt",
                              "a") as f_angel_time:
                        f_angel_time.write(str(time.time() - time_start))
                        f_angel_time.write(" ")

                if raw_data[1] == 81:
                    gyro_data['ax' + str(client_id)] = \
                        struct.unpack('h', raw_data[2:4])[0] / 32768 * 16 * 9.8
                    gyro_data['ay' + str(client_id)] = \
                        struct.unpack('h', raw_data[4:6])[0] / 32768 * 16 * 9.8
                    gyro_data['az' + str(client_id)] = \
                        struct.unpack('h', raw_data[6:8])[0] / 32768 * 16 * 9.8

                    with open(gyro_address + r"\gyro_ax" + str(client_id) + ".txt", "a") as f_gyro_ax:
                        f_gyro_ax.write(str(gyro_data['ax' + str(client_id)]))
                        f_gyro_ax.write(" ")
                    with open(gyro_address + r"\gyro_ay" + str(client_id) + ".txt", "a") as f_gyro_yx:
                        f_gyro_yx.write(str(gyro_data['ay' + str(client_id)]))
                        f_gyro_yx.write(" ")
                    with open(gyro_address + r"\gyro_az" + str(client_id) + ".txt", "a") as f_gyro_zx:
                        f_gyro_zx.write(str(gyro_data['az' + str(client_id)]))
                        f_gyro_zx.write(" ")
                    with open(gyro_address + r"\gyro_a_time" + str(client_id) + ".txt", "a") as f_a_time:
                        f_a_time.write(str(time.time() - time_start))
                        f_a_time.write(" ")
            except BaseException:
                break
    return 1


def math_test():
    print("1.冲激信号 2.阶跃信号 3.斜坡信号 4.正弦信号")
    print("请选择输出信号：")
    # sys_status = sys.stdin.readline()
    sys_status = '2'
    if sys_status[0] == '1':
        for i in range(0, 1000):
            if i == 500:
                servo.bus_data['angel'][4] = 800
            else:
                servo.bus_data['angel'][4] = 500
            time.sleep(0.01)

    if sys_status[0] == '2':
        for i in range(0, 1000):
            if i > 500:
                servo.bus_data['angel'][4] = 800
            else:
                servo.bus_data['angel'][4] = 500
            time.sleep(0.01)

    if sys_status[0] == '3':
        for i in range(0, 1000):
            servo.bus_data['angel'][4] = int(500 + i * 0.3)
            time.sleep(0.01)

    if sys_status[0] == '4':
        for i in range(0, 1000):
            servo.bus_data['angel'][4] = int(500 + 300 * math.sin(2 * math.pi * i / 1000))
            time.sleep(0.01)
    return


def key_scan(flag):
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('space'):  # if key 'q' is pressed
            print('记录落脚一次')
            flag = 1
    except BaseException:
        pass  # if user pressed a key other than the given key the loop will break
    return flag

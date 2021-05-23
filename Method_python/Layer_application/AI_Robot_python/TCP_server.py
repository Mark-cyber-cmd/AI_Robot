import socket
import time
import struct
import threading
import math

"""这是test分支里面的python程序 第二遍 哈哈哈 """
"""陀螺仪参数设置"""
command_single_data = b'\xFF\xAA\x03\x0C\x00'
command_setup_open = b'\xFF\xAA\x69\x88\xB5'
command_setup_zero = b'\xFF\xAA\x01\x08\x00'
command_setup_close = b'\xFF\xAA\x00\x00\x00'
command_setup_speed_50Hz = b'\xFF\xAA\x03\x09\x00'
command_setup_data_angel = b'\xFF\xAA\x02\x08\x00'
"""控制舵机参数"""
con_time = 100  # ms
N = 4
"""绘图参数"""
axis_servo3_address = r"C:\Users\dingy\Desktop\Matlab\servo3_data.txt"
axis_servo6_address = r"C:\Users\dingy\Desktop\Matlab\servo6_data.txt"
axis_x_init = 0
axis_y_init = 0
axis_x = [axis_x_init, ]
axis_y = [axis_y_init, ]
"""陀螺仪数据"""
gyro_data = {'temper1': 0, 'roll1': 0, 'pitch1': 0, 'yaw1': 0, 'fps1': 0,
             'temper2': 0, 'roll2': 0, 'pitch2': 0, 'yaw2': 0, 'fps2': 0,
             'temper3': 0, 'roll3': 0, 'pitch3': 0, 'yaw3': 0, 'fps3': 0,
             'temper4': 0, 'roll4': 0, 'pitch4': 0, 'yaw4': 0, 'fps4': 0}
gyro_data_before = {'temper1': 0, 'roll1': 0, 'pitch1': 0, 'yaw1': 0, 'fps1': 0,
                    'temper2': 0, 'roll2': 0, 'pitch2': 0, 'yaw2': 0, 'fps2': 0,
                    'temper3': 0, 'roll3': 0, 'pitch3': 0, 'yaw3': 0, 'fps3': 0,
                    'temper4': 0, 'roll4': 0, 'pitch4': 0, 'yaw4': 0, 'fps4': 0}
"""总线舵机数据"""
bus_data = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500],
            'time': con_time, 'cmd': 3}
bus_data_back = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500]}
gravity = 0
"""TCP客户端连接管理"""
client_index = {'bus': 0, 'gyro_1': 0, 'gyro_2': 0, 'gyro_3': 0, 'gyro_4': 0}
client_status = {'bus': False, 'gyro_1': False, 'gyro_2': False, 'gyro_3': False, 'gyro_4': False}


def control_algorithm_n():
    bus_data_s = [500, 500, 500, 500]
    global gyro_data_before, gravity

    if gyro_data['roll4'] - gyro_data_before['roll4'] > 0.1 and gravity == 0:
        servo_move(client_index['bus'], [1, 4], 3, [440, 440], 200)
        time.sleep(0.2)
        gravity = 1

    if abs(gyro_data['roll4'] + gyro_data['roll1']) > 1 and gravity == 1:
        bus_data_s[0] = \
            500 + gyro_data['roll4'] / 270 * 1000
        bus_data_s[1] = \
            500 + gyro_data['roll4'] / 270 * 1000
        bus_data_s[2] = \
            500 + gyro_data['roll4'] / 270 * 1000
        bus_data_s[3] = \
            500 + gyro_data['roll4'] / 270 * 1000
        servo_move(client_index['bus'], [2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(0.1)

        if gyro_data['roll4'] + 8 * gyro_data['roll1'] < 5:
            servo_move(client_index['bus'], [1, 4], 3, [500, 500], 200)
            time.sleep(0.2)
            gravity = 0

    if gyro_data['roll1'] - gyro_data_before['roll1'] > 0.1 and gravity == 0:
        servo_move(client_index['bus'], [1, 4], 3, [560, 560], 200)
        time.sleep(0.2)
        gravity = -1

    if abs(gyro_data['roll4'] + gyro_data['roll1']) > 1 and gravity == -1:
        bus_data_s[0] = \
            500 - gyro_data['roll1'] / 270 * 1000
        bus_data_s[1] = \
            500 - gyro_data['roll1'] / 270 * 1000
        bus_data_s[2] = \
            500 - gyro_data['roll1'] / 270 * 1000
        bus_data_s[3] = \
            500 - gyro_data['roll1'] / 270 * 1000
        servo_move(client_index['bus'], [2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(0.1)

        if gyro_data['roll1'] + 8 * gyro_data['roll4'] < 5:
            servo_move(client_index['bus'], [1, 4], 3, [500, 500], 100)
            time.sleep(0.01)
            gravity = 0

        with open(r"C:\Users\dingy\Desktop\Matlab\gyro1_data.txt", "a") as f_gyro1:
            f_gyro1.write(str(gyro_data['roll1']))
            f_gyro1.write(" ")
        with open(r"C:\Users\dingy\Desktop\Matlab\gyro4_data.txt", "a") as f_gyro4:
            f_gyro4.write(str(gyro_data['roll4']))
            f_gyro4.write(" ")

        servo_record(client_index['bus'])
    return


def gyro_thread(gyro_client, gyro_addr):
    if gyro_addr[0] == '192.168.43.157' or gyro_addr[0] == '192.168.43.52' \
            or gyro_addr[0] == '192.168.43.28' or gyro_addr[0] == '192.168.43.38':
        gyro_client.send(command_setup_open)
        time.sleep(0.1)
        gyro_client.send(command_setup_zero)
        time.sleep(0.1)
        gyro_client.send(command_setup_speed_50Hz)
        time.sleep(0.1)
        gyro_client.send(command_setup_data_angel)
        time.sleep(0.1)
        gyro_client.send(command_setup_close)
        time.sleep(0.1)
        raw_data = gyro_client.recv(11)
        client_id = raw_data[2]
        client_index['gyro_' + str(client_id)] = gyro_client
        client_status['gyro_' + str(client_id)] = True
        print("陀螺仪ID:", client_id, '成功连接并校准')
        time_before = time.time()
        fps = 0
        while True:
            try:
                raw_data = gyro_client.recv(11)
                gyro_data_before['roll' + str(client_id)] = gyro_data['roll' + str(client_id)]
                gyro_data_before['pitch' + str(client_id)] = gyro_data['roll' + str(client_id)]
                gyro_data_before['yaw' + str(client_id)] = gyro_data['roll' + str(client_id)]
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
                        fps = 0
                    else:
                        fps = fps + 1
            except BaseException:
                pass
    return 1


def bus_thread(bus_client, bus_addr):
    if bus_addr[0] == '192.168.43.189':
        client_index['bus'] = bus_client
        client_status['bus'] = True
        print("舵机总线控制器成功连接")
        while True:
            control_algorithm_n()
            print("ID:4 ", int(gyro_data['roll4']), "ID:1", int(gyro_data['roll1']), "g:", gravity)
    return


def servo_record(bus_client):
    if client_status['bus']:
        servo_pos(bus_client, [3, 6])
        with open(axis_servo3_address, "a") as f_servo3:
            f_servo3.write(str(bus_data_back['angel'][3 - 1]))
            f_servo3.write(" ")

        with open(axis_servo6_address, "a") as f_servo6:
            f_servo6.write(str(bus_data_back['angel'][6 - 1]))
            f_servo6.write(" ")
    return


def servo_move(bus_client, s_id, s_cmd, s_angle, s_time):
    servo_cmd = [b'\x55', b'\x55', struct.pack('B', len(s_id) * 3 + 5), struct.pack('B', s_cmd),
                 struct.pack('B', len(s_id)), struct.pack('H', s_time)]
    for i in range(len(s_id)):
        servo_cmd.append(struct.pack('B', s_id[i]))
        servo_cmd.append(struct.pack('H', int(s_angle[i])))
    servo_cmd = b''.join(servo_cmd)
    bus_client.send(servo_cmd)
    return


def servo_pos(bus_client, s_id):
    for i in range(len(s_id)):
        servo_cmd = [b'\x55', b'\x55', struct.pack('B', 4), b'\x15', struct.pack('B', 1), struct.pack('B', s_id[i])]
        servo_cmd = b''.join(servo_cmd)
        bus_client.send(servo_cmd)
        pos_data = bus_client.recv(8)
        try:
            bus_data_back['angel'][s_id[i] - 1] = struct.unpack('H', pos_data[6:8])[0]
        except BaseException:
            print("舵机数据回传错误")
    return


def math_test():
    print("1.冲激信号 2.阶跃信号 3.斜坡信号 4.正弦信号")
    print("请选择输出信号：")
    # sys_status = sys.stdin.readline()
    sys_status = '2'
    if sys_status[0] == '1':
        for i in range(0, 1000):
            if i == 500:
                bus_data['angel'][4] = 800
            else:
                bus_data['angel'][4] = 500
            time.sleep(0.01)

    if sys_status[0] == '2':
        for i in range(0, 1000):
            if i > 500:
                bus_data['angel'][4] = 800
            else:
                bus_data['angel'][4] = 500
            time.sleep(0.01)

    if sys_status[0] == '3':
        for i in range(0, 1000):
            bus_data['angel'][4] = int(500 + i * 0.3)
            time.sleep(0.01)

    if sys_status[0] == '4':
        for i in range(0, 1000):
            bus_data['angel'][4] = int(500 + 300 * math.sin(2 * math.pi * i / 1000))
            time.sleep(0.01)
    return


"""           建立一个服务端            """

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.43.186', 8000))
server.listen(5)
time_start = time.time()
file = open(r"C:\Users\dingy\Desktop\Matlab\x_axis.txt", "w").close()
file = open(r"C:\Users\dingy\Desktop\Matlab\y_axis.txt", "w").close()
file = open(r"C:\Users\dingy\Desktop\Matlab\gyro1_data.txt", "w").close()
file = open(r"C:\Users\dingy\Desktop\Matlab\gyro4_data.txt", "w").close()
print("服务器准备就绪,等待客户端上线..........")

if __name__ == '__main__':
    while True:
        s_client, addr = server.accept()  # 不阻塞
        gyro_app = threading.Thread(target=gyro_thread, args=(s_client, addr))
        gyro_app.start()
        servo_app = threading.Thread(target=bus_thread, args=(s_client, addr))
        servo_app.start()

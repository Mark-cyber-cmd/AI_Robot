import socket
import time
import struct
import threading
import math

"""这是test分支里面的python程序 第二遍 哈哈哈"""
"""陀螺仪参数设置"""
command_single_data = b'\xFF\xAA\x03\x0C\x00'
command_setup_open = b'\xFF\xAA\x69\x88\xB5'
command_setup_zero = b'\xFF\xAA\x01\x08\x00'
command_setup_close = b'\xFF\xAA\x00\x00\x00'
command_setup_speed_50Hz = b'\xFF\xAA\x03\x09\x00'
command_setup_data_angel = b'\xFF\xAA\x02\x08\x00'
"""控制舵机参数"""
con_time = 400  # ms
N = 1
"""绘图参数"""
axis_x_address = r"C:\Users\dingy\Desktop\Matlab\x_axis.txt"
axis_y_address = r"C:\Users\dingy\Desktop\Matlab\y_axis.txt"
axis_x_init = 0
axis_y_init = 0
axis_x = [axis_x_init, ]
axis_y = [axis_y_init, ]
"""陀螺仪数据"""
gyro_data = {'temper1': 0, 'roll1': 0, 'pitch1': 0, 'yaw1': 0, 'fps1': 0,
             'temper2': 0, 'roll2': 0, 'pitch2': 0, 'yaw2': 0, 'fps2': 0,
             'temper3': 0, 'roll3': 0, 'pitch3': 0, 'yaw3': 0, 'fps3': 0,
             'temper4': 0, 'roll4': 0, 'pitch4': 0, 'yaw4': 0, 'fps4': 0}
"""总线舵机数据"""
bus_data = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500],
            'time': con_time, 'cmd': 3}
bus_data_back = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500]}
"""TCP客户端连接管理"""
client_index = {'bus': 0, 'gyro_1': 0, 'gyro_2': 0, 'gyro_3': 0, 'gyro_4': 0}
client_status = {'bus': False, 'gyro_1': False, 'gyro_2': False, 'gyro_3': False, 'gyro_4': False}


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
        print("陀螺仪ID:", client_id, '成功连接并校准')
        time_before = time.time()
        fps = 0
        while True:
            raw_data = gyro_client.recv(11)
            if raw_data[1] == 83:
                gyro_data['roll' + str(client_id)] = \
                    struct.unpack('h', raw_data[2:4])[0] / 32768 * 180
                gyro_data['pitch' + str(client_id)] = \
                    struct.unpack('h', raw_data[4:6])[0] / 32768 * 180
                gyro_data['yaw' + str(client_id)] = \
                    struct.unpack('h', raw_data[6:8])[0] / 32768 * 180

                if client_id == 1:
                    bus_data["angel"][1 - 1] = \
                        500 + gyro_data['yaw1'] / 270 * 1000
                    if gyro_data['roll2'] > 0:
                        bus_data["angel"][2 - 1] = \
                            500 + (gyro_data['roll1'] + gyro_data['roll2']) / 270 * 1000
                    else:
                        bus_data["angel"][2 - 1] = 500
                if client_id == 2:
                    bus_data["angel"][3 - 1] = \
                        500 + gyro_data['roll2'] / 270 * 1000
                if client_id == 3:
                    bus_data["angel"][4 - 1] = \
                        500 + gyro_data['yaw3'] / 270 * 1000
                    if gyro_data['roll4'] > 0:
                        bus_data["angel"][5 - 1] = \
                            500 - (gyro_data['roll3'] + gyro_data['roll4']) / 270 * 1000
                    else:
                        bus_data['angel'][5 - 1] = 500
                if client_id == 4:
                    bus_data["angel"][6 - 1] = \
                        500 - gyro_data['roll4'] / 270 * 1000
                if time.time() - time_before > 1:
                    time_before = time.time()
                    gyro_data['fps' + str(client_id)] = fps
                    fps = 0
                else:
                    fps = fps + 1
    return 1


def bus_thread(bus_client, bus_addr):
    if bus_addr[0] == '192.168.43.189':
        client_index['bus'] = bus_client
        client_status['bus'] = True
        print("舵机总线控制器成功连接")
        while True:
            servo_move(bus_client, bus_data['id'], bus_data['cmd'], bus_data['angel'], bus_data['time'])
            servo_pos(bus_client, [1, 2, 3, 4, 5, 6])
            print(bus_data_back['angel'])
            # servo_record(bus_client, 6)
            time.sleep(con_time / 1000)
    return


def servo_record(bus_client, servo_id):
    if client_status['bus']:
        with open(axis_x_address, "a") as f_x_axis:
            f_x_axis.write(str(time.time() - time_start))
            f_x_axis.write(" ")
        with open(axis_y_address, "a") as f_y_axis:
            servo_pos(bus_client, [1, 2, 3, 4, 5, 6])
            f_y_axis.write(str(bus_data_back['angel'][servo_id - 1]))
            f_y_axis.write(" ")
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
        except Exception:
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
print("服务器准备就绪,等待客户端上线..........")

if __name__ == '__main__':
    while True:
        s_client, addr = server.accept()  # 不阻塞
        gyro_app = threading.Thread(target=gyro_thread, args=(s_client, addr))
        gyro_app.start()
        servo_app = threading.Thread(target=bus_thread, args=(s_client, addr))
        servo_app.start()

import Gyro as gyro
import Control as control
import time
import struct
"""控制舵机参数"""
time_start = 0
con_time = 100  # ms
N = 1
"""总线舵机数据"""
bus_data = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500],
            'time': con_time, 'cmd': 3}
bus_data_back = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500]}
gravity = 0
"""绘图参数"""
gyro_address = r".\Data\Data_tmp"
servo_address = r".\Data\Data_tmp"


def control_algorithm():
    bus_data_s = [500, 500, 500, 500]
    global gravity

    if gyro.gyro_data['roll4'] - gyro.gyro_data_before['roll4'] > 0.1 and gravity == 0:
        servo_move(control.client_index['bus'], [1, 4], 3, [440, 440], 200)
        time.sleep(0.2)
        servo_move(control.client_index['bus'], [2, 3, 5, 6], 3, [500, 500, 500, 500], 500)  # 步距补偿
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
        servo_move(control.client_index['bus'], [2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(con_time / 1000)

        if gyro.gyro_data['roll4'] + 8 * gyro.gyro_data['roll1'] < 5:
            servo_move(control.client_index['bus'], [1, 4], 3, [500, 500], 200)
            time.sleep(0.2)
            gravity = 0

    if gyro.gyro_data['roll1'] - gyro.gyro_data_before['roll1'] > 0.1 and gravity == 0:
        servo_move(control.client_index['bus'], [1, 4], 3, [560, 560], 200)
        time.sleep(0.2)
        servo_move(control.client_index['bus'], [2, 3, 5, 6], 3, [500, 500, 500, 500], 500)
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
        servo_move(control.client_index['bus'], [2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(con_time / 1000)

        if gyro.gyro_data['roll1'] + 8 * gyro.gyro_data['roll4'] < 5:
            servo_move(control.client_index['bus'], [1, 4], 3, [500, 500], 200)
            time.sleep(0.2)
            gravity = 0
    return


def bus_thread(bus_client, bus_addr):
    global time_start
    if bus_addr[0] == '192.168.43.189':
        control.client_index['bus'] = bus_client
        control.client_status['bus'] = True
        print("舵机总线控制器成功连接")
        time.sleep(5)
        time_start = time.time()
        while True:
            control_algorithm()
            print("ID:4 ", int(gyro.gyro_data['roll4']), "ID:1", int(gyro.gyro_data['roll1']), "g:", gravity)
    return


def servo_record(bus_client):
    global time_start
    if control.client_status['bus']:
        servo_pos(bus_client, [3, 6])
        time.sleep(0.1)
        with open(servo_address + "/servo3.txt", "a") as f_servo3:
            f_servo3.write(str(bus_data_back['angel'][3 - 1]))
            f_servo3.write(" ")
        with open(servo_address + "/servo3_time.txt", "a") as f_servo3_time:
            f_servo3_time.write(str(time.time() - time_start))
            f_servo3_time.write(" ")

        with open(servo_address + "/servo6.txt", "a") as f_servo6:
            f_servo6.write(str(bus_data_back['angel'][6 - 1]))
            f_servo6.write(" ")
        with open(servo_address + "/servo6_time.txt", "a") as f_servo6_time:
            f_servo6_time.write(str(time.time() - time_start))
            f_servo6_time.write(" ")
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

import serial
import struct
import time
import matplotlib.pyplot as plt


def CMD_SERVO_MOVE(s_id, s_cmd, s_angle, s_time):
    servo_cmd = [b'\x55', b'\x55', struct.pack('B', len(s_id) * 3 + 5), struct.pack('B', s_cmd),
                 struct.pack('B', len(s_id)), struct.pack('H', s_time)]
    for i in range(len(s_id)):
        servo_cmd.append(struct.pack('B', s_id[i]))
        servo_cmd.append(struct.pack('H', s_angle[i]))
    servo_cmd = b''.join(servo_cmd)
    return servo_cmd


servo_data = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500], 'time': 500, 'cmd': 3}

if __name__ == "__main__":
    ser = serial.Serial("COM9", 115200, timeout=5)   # windows系统使用com1口连接串行口

    time_before = 0
    angel_change = 1
    move_status = 0
    w = 50  # w >1 就可以
    x_axis = []
    y_axis = []

    while 1:
        if (time.time() - time_before) > servo_data['time'] / 1000:
            time_before = time.time()

            ser.write(CMD_SERVO_MOVE(servo_data["id"], servo_data["cmd"],
                                     servo_data["angel"], servo_data["time"]))  # 向端口写数据

            if move_status == 0:
                servo_data["angel"][1] = servo_data["angel"][1] + angel_change
                servo_data["angel"][4] = servo_data["angel"][4] - angel_change
                servo_data['time']     = angel_change * w
            else:
                servo_data["angel"][1] = servo_data["angel"][1] - angel_change
                servo_data["angel"][4] = servo_data["angel"][4] + angel_change
                servo_data['time']     = angel_change * w

            if servo_data["angel"][1] > 700:
                move_status = 1
            if servo_data["angel"][1] < 300:
                move_status = 0
                plt.plot(x_axis, y_axis)
                plt.show()
                x_axis = []
                y_axis = []
            print(str(servo_data['angel'][1]) + " , " + str(servo_data['angel'][4]))
            print("时间是：", angel_change * w," 角度变化是：", angel_change)
            # angel_change = angel_change - 1
            x_axis.append(time.time())
            y_axis.append(servo_data["angel"][1])
    # ser.close()         # 关闭端口

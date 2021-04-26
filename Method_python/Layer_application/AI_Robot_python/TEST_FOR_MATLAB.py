import sys
import time
import math

servo_data = {'id': [1, 2, 3, 4, 5, 6], 'angel': [500, 500, 500, 500, 500, 500], 'time': 10, 'cmd': 3}


def TEST_FOR_MAT():
    while 1:
        print("1.冲激信号 2.阶跃信号 3.斜坡信号 4.正弦信号")
        print("请选择输出信号：")
        sys_status = sys.stdin.readline()
        if sys_status[0] == '1':
            for i in range(0, 1000):
                if i == 500:
                    servo_data['angel'][4] = 800
                else:
                    servo_data['angel'][4] = 500
                print(servo_data['angel'][4])
                time.sleep(0.01)

        if sys_status[0] == '2':
            for i in range(0, 1000):
                if i > 500:
                    servo_data['angel'][4] = 800
                else:
                    servo_data['angel'][4] = 500
                print(servo_data['angel'][4])
                time.sleep(0.01)

        if sys_status[0] == '3':
            for i in range(0, 1000):
                servo_data['angel'][4] = int(500 + i * 0.3)
                print(servo_data['angel'][4])
                time.sleep(0.01)

        if sys_status[0] == '4':
            for i in range(0, 1000):
                servo_data['angel'][4] = int(500 + 300 * math.sin(2*math.pi*i/1000))
                print(servo_data['angel'][4])
                time.sleep(0.01)
TEST_FOR_MAT()

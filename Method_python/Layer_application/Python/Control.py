import numpy as np
import os
import shutil
import keyboard
import socket
import pywifi
import threading
from Robot import *
from Gyro import *

# 保存包中写义的常量
from pywifi import const

"""预设的WIFI白名单"""
white_list = ['192.168.43.157', '192.168.43.52', '192.168.43.28', '192.168.43.38', "172.20.10.3"]

"""                  神经网络控制参数                 """
w1 = np.loadtxt("./Data/BP_net/Net6/w1.txt", delimiter=" ", dtype="float")
w2 = np.loadtxt("./Data/BP_net/Net6/w2.txt", delimiter=" ", dtype="float")
b1 = np.loadtxt("./Data/BP_net/Net6/b1.txt", delimiter=" ", dtype="float")
b2 = np.loadtxt("./Data/BP_net/Net6/b2.txt", delimiter=" ", dtype="float")
b1 = np.array([b1.tolist()]).T

"""                      控制参数                     """
con_time = 100  # ms
N = 1  # 控制采样频率相对指令的倍数
gravity = 0


def control_gyro():
    global gyro_1, gyro_2, gyro_3, gyro_4, server
    while 1:
        s_client, adder = server.accept()
        try:
            if adder[0] in white_list:
                raw_data = s_client.recv(11)
                s_id = raw_data[2]
                exec('gyro_{0}.client = s_client'.format(s_id))
                exec('gyro_{0}.adder = adder'.format(s_id))
                exec('gyro_{0}.name = s_id'.format(s_id))
                exec('Gyro.client_index[s_id - 1] = True')
                print('陀螺仪ID:', s_id, '成功连接')
        except Exception as e:
            print(e)

        if Gyro.client_index.count(0) == 2:
            break


def control_robot():
    if robot.status:
        print("ai_robot机器人成功连接")

    if 0 not in Gyro.client_index and robot.status:
        main_app = threading.Thread(target=control_main(), args=())
        main_app.start()


def control_main():
    global gravity, gyro_1, gyro_2, gyro_3, gyro_4, robot
    bus_data_s = [500, 500, 500, 500]
    if gyro_4.roll - gyro_4.roll_before > 0.1 and gravity == 0:
        robot.servo_move([1, 4], [440, 440], 200)
        time.sleep(0.2)
        robot.servo_move([2, 3, 5, 6], [500, 500, 500, 500], 500)  # 步距补偿
        time.sleep(0.5)
        gravity = 1

    if abs(gyro_4.roll + gyro_1.roll) > 1 and gravity == 1:
        bus_data_s[0] = \
            500 + gyro_4.roll / 270 * 1000
        bus_data_s[1] = \
            500 + gyro_4.roll / 270 * 1000
        bus_data_s[2] = \
            500 + gyro_4.roll / 270 * 1000
        bus_data_s[3] = \
            500 + gyro_4.roll / 270 * 1000
        robot.servo_move([2, 3, 5, 6], 3, bus_data_s, con_time)
        time.sleep(con_time / 1000)

        if gyro_4.roll + 8 * gyro_1.roll < 5:
            robot.servo_move([1, 4], [500, 500], 200)
            time.sleep(0.2)
            gravity = 0

    if gyro_1.roll - gyro_1.roll_before > 0.1 and gravity == 0:
        robot.servo_move([1, 4], [560, 560], 200)
        time.sleep(0.2)
        robot.servo_move([2, 3, 5, 6], [500, 500, 500, 500], 500)
        time.sleep(0.5)
        gravity = -1

    # TODO 待测试神经网络代码
    # data_set = [[gyro_1.ax, gyro_1.ay, gyro_1.az, gyro_4.ax,
    #             gyro_4.ay, gyro_4.az, gyro_1.roll, gyro_1.pitch,
    #             gyro_1.yaw, gyro_4.roll, gyro_4.pitch, gyro_4.yaw]]
    # data_set = np.array(data_set).T
    # if settle_down(data_set):
    #     robot.servo_move([1, 4], [500, 500], 200)
    #     time.sleep(0.2)
    #     gravity = 0

    if abs(gyro_4.roll + gyro_1.roll) > 1 and gravity == -1:
        bus_data_s[0] = \
            500 - gyro_1.roll / 270 * 1000
        bus_data_s[1] = \
            500 - gyro_1.roll / 270 * 1000
        bus_data_s[2] = \
            500 - gyro_1.roll / 270 * 1000
        bus_data_s[3] = \
            500 - gyro_1.roll / 270 * 1000
        robot.servo_move([2, 3, 5, 6], bus_data_s, con_time)
        time.sleep(con_time / 1000)

        if gyro_1.roll + 8 * gyro_4.roll < 5:
            robot.servo_move([1, 4], [500, 500], 200)
            time.sleep(0.2)
            gravity = 0
    return


def get_ip():
    while 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('www.baidu.com', 80))
            ip = s.getsockname()[0]
            break
        finally:
            s.close
    print("服务器IP为：", ip)
    return ip


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
    try:
        if keyboard.is_pressed('space'):
            print('记录落脚一次')
            flag = 1
    except BaseException:
        pass
    return flag


def connect_wifi(ssid, key):
    wifi = pywifi.PyWiFi()  # 创建一个wifi对象
    ifaces = wifi.interfaces()[0]  # 取第一个无限网卡
    # print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(3)  # 缓冲3秒

    profile = pywifi.Profile()  # 配置文件
    profile.ssid = ssid  # wifi名称
    profile.auth = const.AUTH_ALG_OPEN  # 需要密码
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    profile.key = key  # wifi密码

    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件

    ifaces.connect(tmp_profile)  # 连接
    time.sleep(5)  # 尝试10秒能否成功连接
    if ifaces.status() == const.IFACE_CONNECTED:
        print("连接WiFi:", ssid, "成功")
        return True
    else:
        print("连接WiFi:", ssid, "失败")
        return False


def server_init(port):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 不经过WAIT_TIME，直接关闭
    # server_s.setblocking(False)  # 设置非阻塞编程
    server_s.bind((get_ip(), port))  # 自动获取本机ip 并在8000端口创建服务器
    server_s.listen(5)
    print("服务器准备就绪,等待客户端上线..........\r\n\r\n")
    return server_s


while 1:
    """           建立一个服务端            """
    server = server_init(8000)
    """            成控制对象               """
    gyro_1 = Gyro(server)
    gyro_2 = Gyro(server)
    gyro_3 = Gyro(server)
    gyro_4 = Gyro(server)
    # robot = Robot()
    break

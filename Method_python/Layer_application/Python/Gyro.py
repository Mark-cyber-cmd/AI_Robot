import keyboard
import math
import struct
import time


class Gyro:
    """TODO 所有陀螺仪的基类"""

    """陀螺仪参数设置"""
    setup_open = b'\xFF\xAA\x69\x88\xB5'
    setup_zero = b'\xFF\xAA\x01\x08\x00'
    setup_close = b'\xFF\xAA\x00\x00\x00'
    setup_speed_100Hz = b'\xFF\xAA\x03\x09\x00'
    setup_data_angel = b'\xFF\xAA\x02\x08\x00'  # 设置只要角度
    setup_data_all = b'\xFF\xAA\x02\x0A\x00'  # 设置数据全部输出

    """数据存放路径"""
    gyro_address = r".\Data\Data_tmp"
    servo_address = r".\Data\Data_tmp"

    """预设的WIFI白名单"""
    white_list = ['192.168.43.157', '192.168.43.52', '192.168.43.28', '192.168.43.38']

    def __init__(self, client, addr):
        self.name = 0
        self.client = client
        self.addr = addr

        """陀螺仪数据"""
        self.temper = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.fps = 0
        self.time_angel = 0
        self.time_acc = 0
        self.time_start = 0

    def calibration(self, speed, data):
        self.addr.send(Gyro.setup_open)
        time.sleep(0.1)
        self.addr.send(Gyro.setup_zero)
        time.sleep(0.1)
        self.addr.send(speed)
        time.sleep(0.1)
        self.addr.send(data)
        time.sleep(0.1)
        self.addr.send(Gyro.setup_close)
        time.sleep(0.1)

    def refresh(self, raw_data):
        try:
            if raw_data[1] == 83:
                self.roll = struct.unpack('h', raw_data[2:4])[0] / 32768 * 180
                self.pitch = struct.unpack('h', raw_data[4:6])[0] / 32768 * 180
                self.yaw = struct.unpack('h', raw_data[6:8])[0] / 32768 * 180
                self.time_angel = time.time()
            if raw_data[1] == 81:
                self.ax = struct.unpack('h', raw_data[2:4])[0] / 32768 * 16 * 9.8
                self.ay = struct.unpack('h', raw_data[4:6])[0] / 32768 * 16 * 9.8
                self.az = struct.unpack('h', raw_data[6:8])[0] / 32768 * 16 * 9.8
                self.time_acc = time.time()
        except BaseException:
            pass

    def fps(self):
        if (time.time() - self.time_start) % 1 == 0:
            print('fps' + str(self.name) + ": ", self.fps)
            self.fps = 0
        else:
            self.fps += 1

    def record(self, raw_data):
        if raw_data[1] == 83:
            with open(Gyro.gyro_address + r"\gyro_roll" + str(self.name) + ".txt", "a") as f_gyro_roll:
                f_gyro_roll.write(str(self.roll))
                f_gyro_roll.write(" ")
            with open(Gyro.gyro_address + r"\gyro_pitch" + str(self.name) + ".txt", "a") as f_gyro_pitch:
                f_gyro_pitch.write(str(self.pitch))
                f_gyro_pitch.write(" ")
            with open(Gyro.gyro_address + r"\gyro_yaw" + str(self.name) + ".txt", "a") as f_gyro_yaw:
                f_gyro_yaw.write(str(self.yaw))
                f_gyro_yaw.write(" ")
            with open(Gyro.gyro_address + r"\gyro_angel_time" + str(self.name) + ".txt",
                      "a") as f_angel_time:
                f_angel_time.write(str(self.time_angel - self.time_start))
                f_angel_time.write(" ")

        if raw_data[1] == 81:
            with open(Gyro.gyro_address + r"\gyro_ax" + str(self.name) + ".txt", "a") as f_gyro_ax:
                f_gyro_ax.write(str(self.ax))
                f_gyro_ax.write(" ")
            with open(Gyro.gyro_address + r"\gyro_ay" + str(self.name) + ".txt", "a") as f_gyro_yx:
                f_gyro_yx.write(str(self.ay))
                f_gyro_yx.write(" ")
            with open(Gyro.gyro_address + r"\gyro_az" + str(self.name) + ".txt", "a") as f_gyro_zx:
                f_gyro_zx.write(str(self.az))
                f_gyro_zx.write(" ")
            with open(Gyro.gyro_address + r"\gyro_a_time" + str(self.name) + ".txt", "a") as f_a_time:
                f_a_time.write(str(self.time_acc - self.time_start))
                f_a_time.write(" ")

        # if self.name == 1:
        #     with open(gyro_address + r"\human_status.txt", "a") as f_hs:
        #         f_hs.write(str(gravity_flag))
        #         f_hs.write(" ")
        #         gravity_flag = 0

    def activate(self):
        if self.addr[0] in Gyro.white_list:
            raw_data = self.client.recv(11)
            self.name = raw_data[2]
            self.time_start = time.time()
            self.calibration(self.setup_speed_100Hz, self.setup_data_all)
            print("陀螺仪ID:", self.name, '成功连接并校准')
            while True:
                raw_data = self.client.recv(11)
                self.refresh(raw_data)
                self.record(raw_data)
                self.fps
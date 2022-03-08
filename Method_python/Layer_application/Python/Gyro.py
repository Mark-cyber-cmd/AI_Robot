import struct
import time


class Gyro:
    """所有陀螺仪的基类"""

    """陀螺仪参数设置"""
    setup_open = b'\xFF\xAA\x69\x88\xB5'
    setup_zero = b'\xFF\xAA\x01\x08\x00'
    setup_close = b'\xFF\xAA\x00\x00\x00'
    setup_speed_100Hz = b'\xFF\xAA\x03\x09\x00'
    setup_data_angel = b'\xFF\xAA\x02\x08\x00'  # 设置只要角度
    setup_data_all = b'\xFF\xAA\x02\x0A\x00'  # 设置数据全部输出

    """数据存放路径"""
    gyro_address = r".\Data\Data_tmp"
    """管理客户端在线情况"""
    client_index = []

    def __init__(self, server):
        self.server = server

        self.name = None
        self.client = None
        self.adder = None

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
        self.roll_before = 0

    def connect(self, s_id):
        while 1:
            s_client, adder = self.server.accept()
            self.client = s_client
            self.adder = adder
            try:
                raw_data = self.client.recv(11)
                if s_id == raw_data[2] and raw_data[1] == 1:
                    self.name = raw_data[2]
                    self.time_start = time.time()
                    print("陀螺仪ID:", self.name, '成功连接')
                    Gyro.client_index.append(s_id)
                    break
                else:
                    s_client.close()
                    break
            except Exception as e:
                print(e)

    def calibration(self, speed, data):
        self.client.send(Gyro.setup_open)
        time.sleep(0.1)
        self.client.send(Gyro.setup_zero)
        time.sleep(0.1)
        self.client.send(speed)
        time.sleep(0.1)
        self.client.send(data)
        time.sleep(0.1)
        self.client.send(Gyro.setup_close)
        time.sleep(0.1)

    def refresh(self, raw_data):
        try:
            self.roll_before = self.roll
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
        except Exception as e:
            print(e)

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

    def activate(self):
        self.calibration(self.setup_speed_100Hz, self.setup_data_all)
        self.time_start = time.time()
        counter = self.time_start
        while True:
            raw_data = self.client.recv(11)
            self.refresh(raw_data)
            self.record(raw_data)
            if (time.time() - counter) > 1:
                self.fps = 0
                counter = time.time()
            else:
                self.fps += 1

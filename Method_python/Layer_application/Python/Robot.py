import time
import struct

servo_address = r".\Data\Data_tmp"


class Robot:
    def __init__(self, server):
        self.server = server
        self.client = 0
        self.addr = 0
        self.status = 0

        self.move_cmd = 3
        self.back_data = []
        self.time_start = 0

    def connect(self):
        while 1:
            s_client, addr = self.server.accept()
            if addr[0] == '192.168.43.189':
                self.client = s_client
                self.addr = addr
                self.time_start = time.time()
                self.status = 1
                print("机器人成功连接:")
                break

    def servo_move(self, s_id, s_angle, s_time):
        servo_cmd = [b'\x55', b'\x55', struct.pack('B', len(s_id) * 3 + 5), struct.pack('B', self.move_cmd),
                     struct.pack('B', len(s_id)), struct.pack('H', s_time)]
        for i in range(len(s_id)):
            servo_cmd.append(struct.pack('B', s_id[i]))
            servo_cmd.append(struct.pack('H', int(s_angle[i])))
        servo_cmd = b''.join(servo_cmd)
        self.client.send(servo_cmd)
        return

    def servo_pos(self, s_id):
        for i in range(len(s_id)):
            servo_cmd = [b'\x55', b'\x55', struct.pack('B', 4), b'\x15', struct.pack('B', 1), struct.pack('B', s_id[i])]
            servo_cmd = b''.join(servo_cmd)
            self.client.send(servo_cmd)
            pos_data = self.client.recv(8)
            try:
                self.back_data[s_id[i] - 1] = struct.unpack('H', pos_data[6:8])[0]
            except BaseException:
                print("舵机数据回传错误")
        return

    def servo_record(self):
        if self.status:
            self.servo_pos([3, 6])
            time.sleep(0.1)
            with open(servo_address + "/servo3.txt", "a") as f_servo3:
                f_servo3.write(str(self.back_data[3 - 1]))
                f_servo3.write(" ")
            with open(servo_address + "/servo3_time.txt", "a") as f_servo3_time:
                f_servo3_time.write(str(time.time() - self.time_start))
                f_servo3_time.write(" ")

            with open(servo_address + "/servo6.txt", "a") as f_servo6:
                f_servo6.write(str(self.back_data[6 - 1]))
                f_servo6.write(" ")
            with open(servo_address + "/servo6_time.txt", "a") as f_servo6_time:
                f_servo6_time.write(str(time.time() - self.time_start))
                f_servo6_time.write(" ")
        return

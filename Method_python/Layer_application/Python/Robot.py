import time
import struct

servo_address = r".\Data\Data_tmp"


class Robot:

    def __init__(self, server):
        self.server = server

        self.client = None
        self.adder = None
        self.status = 0

        self.move_cmd = 3
        self.back_data = []
        self.time_start = 0

        self.position = [0, 500, 500, 500, 500, 500, 500]

    def connect(self):
        while 1:
            s_client, adder = self.server.accept()
            self.client = s_client
            self.adder = adder
            raw_data = self.client.recv(11)
            if raw_data[1] == 0:
                self.status = True
                print('机械腿成功连接')
                break
            else:
                s_client.close()

    def move(self, s_id, s_angle, s_time):
        servo_cmd = [b'\x55', b'\x55', struct.pack('B', len(s_id) * 3 + 5), struct.pack('B', self.move_cmd),
                     struct.pack('B', len(s_id)), struct.pack('H', s_time)]
        for i in range(len(s_id)):
            servo_cmd.append(struct.pack('B', s_id[i]))
            servo_cmd.append(struct.pack('H', int(s_angle[i])))
        servo_cmd = b''.join(servo_cmd)
        self.client.send(servo_cmd)

        for index, element in enumerate(s_id):
            self.position[element] = round(s_angle[index], 2)
        return

    def pos(self, s_id):
        for i in range(len(s_id)):
            servo_cmd = [b'\x55', b'\x55', struct.pack('B', 4), b'\x15', struct.pack('B', 1), struct.pack('B', s_id[i])]
            servo_cmd = b''.join(servo_cmd)
            self.client.send(servo_cmd)
            pos_data = self.client.send(8)
            try:
                self.back_data[s_id[i] - 1] = struct.unpack('H', pos_data[6:8])[0]
            except Exception as e:
                print(e)
        return

    def record(self):
        if self.status:
            self.pos([3, 6])
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

    def reset(self):
        self.move([1, 2, 3, 4, 5, 6], [500, 500, 500, 500, 500, 500], 500)

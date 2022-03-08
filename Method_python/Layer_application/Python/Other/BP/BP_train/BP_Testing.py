import numpy as np
import matplotlib.pyplot as plt

Data_address = r"./Data/Data_base/zzm/大腿数据_6/"
Label_name = r"human_status.txt"


# 创建激活函数sigmoid
def tansig(z):
    return 2 / (1 + np.exp(-2 * z)) - 1


def load_dataset(filename):
    fp = open(filename)  # （299，22）

    # 存放数据
    dataset = []

    for i in fp.readlines():  # 按照行来进行读取，每次读取一行，一行的数据作为一个元素存放在了类别中
        a = i.strip().split()  # 去掉每一行数据的空格以及按照默认的分隔符进行划分

        # 每个数据行的最后一个是标签
        dataset.append([float(j) for j in a[:len(a)]])  # 读取每一行中除最后一个元素的前面的元素，并且将其转换为浮点数
    return dataset


def standard_data(data_set):
    axis_x_vals = np.linspace(0, 1, 2319)
    axis_x = np.linspace(0, 1, len(data_set))
    data_set = np.interp(axis_x_vals, axis_x, data_set)
    # output = (data_set - min(data_set)) / (max(data_set) - min(data_set)) * 2 - 1
    return data_set.tolist()


gyro_ax2 = standard_data(load_dataset(Data_address + "gyro_ax1.txt")[0])
gyro_ax4 = standard_data(load_dataset(Data_address + "gyro_ax4.txt")[0])
gyro_ay2 = standard_data(load_dataset(Data_address + "gyro_ay1.txt")[0])
gyro_ay4 = standard_data(load_dataset(Data_address + "gyro_ay4.txt")[0])
gyro_az2 = standard_data(load_dataset(Data_address + "gyro_az1.txt")[0])
gyro_az4 = standard_data(load_dataset(Data_address + "gyro_az1.txt")[0])
gyro_pitch2 = standard_data(load_dataset(Data_address + "gyro_pitch1.txt")[0])
gyro_pitch4 = standard_data(load_dataset(Data_address + "gyro_pitch4.txt")[0])
gyro_roll2 = standard_data(load_dataset(Data_address + "gyro_roll1.txt")[0])
gyro_roll4 = standard_data(load_dataset(Data_address + "gyro_roll4.txt")[0])
gyro_yaw2 = standard_data(load_dataset(Data_address + "gyro_yaw1.txt")[0])
gyro_yaw4 = standard_data(load_dataset(Data_address + "gyro_yaw4.txt")[0])
Label_set = standard_data(load_dataset(Data_address + "human_status.txt")[0])
Data_set = [gyro_ax2, gyro_ay2, gyro_az2, gyro_ax4, gyro_ay4, gyro_az4, gyro_pitch2,
            gyro_roll2, gyro_yaw2, gyro_pitch4, gyro_roll4, gyro_yaw4]

Input = np.array(Data_set)


w1 = np.loadtxt("./BP_net/Net1/w1.txt", delimiter=" ", dtype="float")
w2 = np.loadtxt("./BP_net/Net1/w2.txt", delimiter=" ", dtype="float")
b1 = np.loadtxt("./BP_net/Net1/b1.txt", delimiter=" ", dtype="float")
b2 = np.loadtxt("./BP_net/Net1/b2.txt", delimiter=" ", dtype="float")

b1 = np.array([b1.tolist()]).T
step1 = np.dot(w1, Input)
step2 = tansig(step1 - b1)
step3 = np.dot(w2, step2)
step4 = tansig(step3 - b2)
print(step4)

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(1)
plt.plot(gyro_ax2, linewidth=0.5)
plt.plot(gyro_ay2, linewidth=0.5)
plt.plot(gyro_az2, linewidth=0.5)
plt.plot(np.heaviside((step4 - 0.5), 1), linewidth=0.5)
plt.title("1号加速度数据 落脚点输出")
plt.xlabel("N")
plt.ylabel("预测值")

plt.figure(2)
plt.plot(gyro_roll2, linewidth=0.5)
plt.plot(gyro_pitch2, linewidth=0.5)
plt.plot(gyro_yaw2, linewidth=0.5)
plt.plot(np.heaviside((step4 - 0.5), 1), linewidth=0.5)
plt.title("1号角度数据 落脚点输出")
plt.xlabel("N")
plt.ylabel("预测值")
plt.show()

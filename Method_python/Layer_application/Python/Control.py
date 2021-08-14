import numpy as np
"""神经网络控制参数"""
w1 = np.loadtxt("./Data/BP_net/Net6/w1.txt", delimiter=" ", dtype="float")
w2 = np.loadtxt("./Data/BP_net/Net6/w2.txt", delimiter=" ", dtype="float")
b1 = np.loadtxt("./Data/BP_net/Net6/b1.txt", delimiter=" ", dtype="float")
b2 = np.loadtxt("./Data/BP_net/Net6/b2.txt", delimiter=" ", dtype="float")
b1 = np.array([b1.tolist()]).T
"""TCP客户端连接管理"""
client_index = {'bus': 0, 'gyro_1': 0, 'gyro_2': 0, 'gyro_3': 0, 'gyro_4': 0}
client_status = {'bus': False, 'gyro_1': False, 'gyro_2': False, 'gyro_3': False, 'gyro_4': False}


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

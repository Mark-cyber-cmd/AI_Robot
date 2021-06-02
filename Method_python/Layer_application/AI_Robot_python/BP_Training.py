import numpy as np
import os
Data_address = r"./Data/Data_base/zzm/大腿数据_4/"


# 创建加载数据读取数据以及划分数据集的函数，返回数据特征集以及数据标签集
def loaddataset(Data_address, Data):
    dataset = []
    labelset = []
    for j in range(len(Data)):
        fp_dataset = open(Data_address + Data[j])
        for i in fp_dataset.readlines():
            a = i.strip().split()
            dataset.append([float(j) for j in a[:len(a)]])

    fp_labelset = open(Data_address + Data[0])
    for i in fp_labelset.readlines():
        a = i.strip().split()
        labelset.append([float(j) for j in a[:len(a)]])
    return dataset, labelset


def list_dir(file_dir):
    print('<><><><><><> listdir <><><><><><>')
    print("current dir : {0}".format(file_dir))
    file_name = []
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        # 获取文件的绝对路径
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path):  # 判断是否是文件还是目录需要用绝对路径
            print("{0} : is file!".format(cur_file))
            file_name.append(cur_file)
        if os.path.isdir(path):
            # print("{0} : is dir!".format(cur_file))
            # list_dir(path)  # 递归子目录
            pass
    print('<><><><><><> listdir <><><><><><>\n')
    return file_name


# x为输入层神经元个数，y为隐层神经元个数，z输出层神经元个数
# 创建的是参数初始化函数，参数有各层间的权重weight和阈值即偏置value就是b
# 本例的x,y=len(dataset[0])=22，z=1
def parameter_initialization(x, y, z):
    # 隐层阈值
    value1 = np.random.randint(-5, 5, (1, y)).astype(np.float64)  # 随机生成（-5，5）之间的整数组成（1，y）的数组，然后再将其转为浮点数显示

    # 输出层阈值
    value2 = np.random.randint(-5, 5, (1, z)).astype(np.float64)

    # 输入层与隐层的连接权重
    weight1 = np.random.randint(-5, 5, (x, y)).astype(np.float64)

    # 隐层与输出层的连接权重
    weight2 = np.random.randint(-5, 5, (y, z)).astype(np.float64)

    return weight1, weight2, value1, value2


# 创建激活函数sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 创建训练样本的函数，返回训练完成后的参数weight和value，这里的函数是经过一次迭代后的参数，即所有的样本经过一次训练后的参数
# 具体参数的值可以通过设置迭代次数和允许误差来进行确定
def trainning(dataset, labelset, weight1, weight2, value1, value2):
    # x为步长
    x = 0.01  # 学习率
    for i in range(len(dataset)):  # 依次读取数据特征集中的元素，一个元素即为一个样本所含有的所有特征数据
        # 输入数据
        # （1,21）
        inputset = np.mat(dataset[i]).astype(np.float64)  # 每次输入一个样本，将样本的特征转化为矩阵，以浮点数显示

        # 数据标签
        # （1，1）
        outputset = np.mat(labelset[i]).astype(np.float64)  # 输入样本所对应的标签

        # 隐层输入，隐层的输入是由输入层的权重决定的，wx
        # input1：（1，21）.（21，21）=（1，21）
        input1 = np.dot(inputset, weight1).astype(np.float64)

        # 隐层输出，由隐层的输入和阈值以及激活函数决定的，这里的阈值也可以放在输入进行计算
        # sigmoid（（1，21）-（1，21））=（1，21）
        output2 = sigmoid(input1 - value1).astype(np.float64)

        # 输出层输入，由隐层的输出
        # （1，21）.（21，1）=（1，1）
        input2 = np.dot(output2, weight2).astype(np.float64)

        # 输出层输出，由输出层的输入和阈值以及激活函数决定的，这里的阈值也可以放在输出层输入进行计算
        # （1，1）.（1，1）=（1，1）
        output3 = sigmoid(input2 - value2).astype(np.float64)

        # 更新公式由矩阵运算表示
        # a:(1,1)
        a = np.multiply(output3, 1 - output3)  # 输出层激活函数求导后的式子，multiply对应元素相乘，dot矩阵运算
        # g:(1,1)
        g = np.multiply(a, outputset - output3)  # outputset - output3：实际标签和预测标签差
        # weight2:(21,1),np.transpose(weight2):(1,21),b:(1,21)
        b = np.dot(g, np.transpose(weight2))
        # (1,21)
        c = np.multiply(output2, 1 - output2)  # 隐层输出激活函数求导后的式子，multiply对应元素相乘，dot矩阵运算
        # (1,21)
        e = np.multiply(b, c)

        value1_change = -x * e  # （1，21）
        value2_change = -x * g  # （1，1）
        weight1_change = x * np.dot(np.transpose(inputset), e)  # （21，21）
        weight2_change = x * np.dot(np.transpose(output2), g)  # （21，1）

        # 更新参数，权重与阈值的迭代公式
        value1 += value1_change
        value2 += value2_change
        weight1 += weight1_change
        weight2 += weight2_change
    return weight1, weight2, value1, value2


if __name__ == "__main__":
    Data = list_dir(Data_address)
    dataset, labelset = loaddataset(Data_address, Data)
    weight1, weight2, value1, value2 = parameter_initialization(len(dataset[0]), len(dataset[0]), 1)
    print(len(dataset))







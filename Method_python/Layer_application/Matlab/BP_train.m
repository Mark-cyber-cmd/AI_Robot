%% 此程序matlab编程实现的BP神经网络
% 清空环境变量
clear;
clc

Data_address = "./Data/Data_base/zzm/大腿数据_12/";

gyro_ax1 = importdata(Data_address + "gyro_ax1.txt");
gyro_ay1 = importdata(Data_address + "gyro_ay1.txt");
gyro_az1 = importdata(Data_address + "gyro_az1.txt");
gyro_ax4 = importdata(Data_address + "gyro_ax4.txt");
gyro_ay4 = importdata(Data_address + "gyro_ay4.txt");
gyro_az4 = importdata(Data_address + "gyro_az4.txt");
gyro_roll1 = importdata(Data_address + "gyro_roll1.txt");
gyro_pitch1 = importdata(Data_address + "gyro_pitch1.txt");
gyro_yaw1 = importdata(Data_address + "gyro_yaw1.txt");
gyro_roll4 = importdata(Data_address + "gyro_roll4.txt");
gyro_pitch4 = importdata(Data_address + "gyro_pitch4.txt");
gyro_yaw4 = importdata(Data_address + "gyro_yaw4.txt");
output = importdata(Data_address + "human_status.txt");

N = 2034;
input = zeros(12, N);
input(1,:) = interp1(0:1/(length(gyro_ax1)-1):1,gyro_ax1,0:1/(N-1):1,'linear'); %载入输入数据
input(2,:) = interp1(0:1/(length(gyro_ay1)-1):1,gyro_ay1,0:1/(N-1):1,'linear'); %载入输入数据
input(3,:) = interp1(0:1/(length(gyro_az1)-1):1,gyro_az1,0:1/(N-1):1,'linear'); %载入输入数据
input(4,:) = interp1(0:1/(length(gyro_ax4)-1):1,gyro_ax4,0:1/(N-1):1,'linear'); %载入输入数据
input(5,:) = interp1(0:1/(length(gyro_ay4)-1):1,gyro_ay4,0:1/(N-1):1,'linear'); %载入输入数据
input(6,:) = interp1(0:1/(length(gyro_az4)-1):1,gyro_az4,0:1/(N-1):1,'linear'); %载入输入数据
input(7,:) = interp1(0:1/(length(gyro_roll1)-1):1,gyro_roll1,0:1/(N-1):1,'linear'); %载入输入数据
input(8,:) = interp1(0:1/(length(gyro_pitch1)-1):1,gyro_pitch1,0:1/(N-1):1,'linear'); %载入输入数据
input(9,:) = interp1(0:1/(length(gyro_yaw1)-1):1,gyro_yaw1,0:1/(N-1):1,'linear'); %载入输入数据
input(10,:) = interp1(0:1/(length(gyro_roll4)-1):1,gyro_roll4,0:1/(N-1):1,'linear'); %载入输入数据
input(11,:) = interp1(0:1/(length(gyro_pitch4)-1):1,gyro_pitch4,0:1/(N-1):1,'linear'); %载入输入数据
input(12,:) = interp1(0:1/(length(gyro_yaw4)-1):1,gyro_yaw4,0:1/(N-1):1,'linear'); %载入输入数据
output = output';


%% 第二步 设置训练数据和预测数据
input_train = input(:,1:round(N*0.8));
output_train =output(1:round(N*0.8),:)';
input_test = input;
output_test =output';
%节点个数
inputnum=12;
hiddennum=5;%隐含层节点数量经验公式p=sqrt(m+n)+a ，故分别取2~13进行试验
outputnum=1;
%% 第三步 训练样本数据归一化
for i=1:length(input(:,1))
    [inputn(i,:), inputps] = mapminmax(input_train(i,:));
end
[outputn, outputps] = mapminmax(output_train);
%% 第四步 构建BP神经网络
net=newff(inputn,outputn,hiddennum,{'tansig','tansig'},'trainlm');% 建立模型，传递函数使用purelin，采用梯度下降法训练

W1= net. iw{1,1};%输入层到中间层的权值
B1 = net.b{1};%中间各层神经元阈值

W2 = net.lw{2,1};%中间层到输出层的权值
B2 = net. b{2};%输出层各神经元阈值

%% 第五步 网络参数配置（ 训练次数，学习速率，训练目标最小误差等）
net.trainParam.epochs=1000;         % 训练次数，这里设置为1000次
net.trainParam.lr=0.01;                   % 学习速率，这里设置为0.01
net.trainParam.goal=0.00000000000000001;                    % 训练目标最小误差，这里设置为0.00001

%% 第六步 BP神经网络训练
net=train(net,inputn,outputn);%开始训练，其中inputn,outputn分别为输入输出样本

%% 第七步 测试样本归一化
inputn_test=mapminmax('apply',input_test,inputps);% 对样本数据进行归一化

%% 第八步 BP神经网络预测
an=sim(net,inputn_test); %用训练好的模型进行仿真

%% 第九步 预测结果反归一化与误差计算     
test_simu=mapminmax('reverse',an,outputps); %把仿真得到的数据还原为原始的数量级
error=test_simu-output_test;      %预测值和真实值的误差

%%第十步 真实值与预测值误差比较
figure(1)
plot(output_test,'bo-')
hold on
plot(test_simu,'r*-')
% hold on
% plot(error,'square','MarkerFaceColor','b')
legend('期望值','预测值','误差')
xlabel('数据组数')
ylabel('值')
[c,l]=size(output_test);
MAE1=sum(abs(error))/l;
MSE1=error*error'/l;
RMSE1=MSE1^(1/2);
disp(['-----------------------误差计算--------------------------'])
disp(['隐含层节点数为',num2str(hiddennum),'时的误差结果如下：'])
disp(['平均绝对误差MAE为：',num2str(MAE1)])
disp(['均方误差MSE为：       ',num2str(MSE1)])
disp(['均方根误差RMSE为：  ',num2str(RMSE1)])
%% 导出数据
dlmwrite("./w1.txt",W1,'delimiter',' ','newline','pc');
dlmwrite("./w2.txt",W2,'delimiter',' ','newline','pc');
dlmwrite("./b1.txt",B1,'delimiter',' ','newline','pc');
dlmwrite("./b2.txt",B2,'delimiter',' ','newline','pc');
%% 此程序matlab编程实现的BP神经网络
% 清空环境变量
clear;
clc;

Data_address = "./Data/Data_base/zzm/大腿数据_1/";
%主程序
gyro_ax1 = importdata(Data_address + 'gyro_ax1.txt');
gyro_ay1 = importdata(Data_address + 'gyro_ay1.txt');
gyro_az1 = importdata(Data_address + 'gyro_az1.txt');
gyro_roll1 = importdata(Data_address + 'gyro_roll1.txt');
gyro_pitch1 = importdata(Data_address + 'gyro_pitch1.txt');
gyro_yaw1 = importdata(Data_address + 'gyro_yaw1.txt');
gyro_a_time1 = importdata(Data_address + 'gyro_a_time1.txt');
gyro_angel_time1 = importdata(Data_address + 'gyro_angel_time1.txt');
gyro_ax4 = importdata(Data_address + 'gyro_ax4.txt');
gyro_ay4 = importdata(Data_address + 'gyro_ay4.txt');
gyro_az4 = importdata(Data_address + 'gyro_az4.txt');
gyro_roll4 = importdata(Data_address + 'gyro_roll4.txt');
gyro_pitch4 = importdata(Data_address + 'gyro_pitch4.txt');
gyro_yaw4 = importdata(Data_address + 'gyro_yaw4.txt');
gyro_a_time4 = importdata(Data_address + 'gyro_a_time4.txt');
gyro_angel_time4 = importdata(Data_address + 'gyro_angel_time4.txt');
output = importdata(Data_address + "human_status.txt");
N = 1386; %自己手动输入吧
gyro_ax1 = interp1(0:1/(length(gyro_ax1)-1):1,gyro_ax1,0:1/(N-1):1,'linear');
gyro_ay1 = interp1(0:1/(length(gyro_ay1)-1):1,gyro_ay1,0:1/(N-1):1,'linear');
gyro_az1 = interp1(0:1/(length(gyro_az1)-1):1,gyro_az1,0:1/(N-1):1,'linear');
gyro_roll1 = interp1(0:1/(length(gyro_roll1)-1):1,gyro_roll1,0:1/(N-1):1,'linear');
gyro_pitch1 = interp1(0:1/(length(gyro_pitch1)-1):1,gyro_pitch1,0:1/(N-1):1,'linear');
gyro_yaw1 = interp1(0:1/(length(gyro_yaw1)-1):1,gyro_yaw1,0:1/(N-1):1,'linear');
gyro_a_time1 = interp1(0:1/(length(gyro_a_time1)-1):1,gyro_a_time1,0:1/(N-1):1,'linear');
gyro_angel_time1 = interp1(0:1/(length(gyro_angel_time1)-1):1,gyro_angel_time1,0:1/(N-1):1,'linear');
gyro_ax4 = interp1(0:1/(length(gyro_ax4)-1):1,gyro_ax4,0:1/(N-1):1,'linear');
gyro_ay4 = interp1(0:1/(length(gyro_ay4)-1):1,gyro_ay4,0:1/(N-1):1,'linear');
gyro_az4 = interp1(0:1/(length(gyro_az4)-1):1,gyro_az4,0:1/(N-1):1,'linear');
gyro_roll4 = interp1(0:1/(length(gyro_roll4)-1):1,gyro_roll4,0:1/(N-1):1,'linear');
gyro_pitch4 = interp1(0:1/(length(gyro_pitch4)-1):1,gyro_pitch4,0:1/(N-1):1,'linear');
gyro_yaw4 = interp1(0:1/(length(gyro_yaw4)-1):1,gyro_yaw4,0:1/(N-1):1,'linear');
gyro_a_time4 = interp1(0:1/(length(gyro_a_time4)-1):1,gyro_a_time4,0:1/(N-1):1,'linear');
gyro_angel_time4 = interp1(0:1/(length(gyro_angel_time4)-1):1,gyro_angel_time4,0:1/(N-1):1,'linear');

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


w1 = importdata("./BP_net/Net2/w1.txt");
w2 = importdata("./BP_net/Net2/w2.txt");
b1 = importdata("./BP_net/Net2/b1.txt");
b2 = importdata("./BP_net/Net2/b2.txt");



output = output';
input_test = input;
output_test =output;

[inputn,inputps]=mapminmax(input_test);%归一化到[-1,1]之间，inputps用来作下一次同样的归一化
[outputn,outputps]=mapminmax(output_test);

step1 = w1 * inputn;
step2 = tansig(step1 - b1);
step3 = w2 * step2;
step4 = tansig(step3 - b2)';
step5 = heaviside(step4 + 0.25);
outputn = heaviside(outputn - 0.5);
subplot(2,1,1);
plot(step5, "-r*");
title("测试组预测值");
hold on;
subplot(2,1,2);
plot(outputn,"-b*"); 
title("测试组期望值")




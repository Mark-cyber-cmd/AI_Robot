%% 此程序matlab编程实现的BP神经网络
% 清空环境变量
clear all；
clc

gyro_ax2 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_ax2.txt");
gyro_ay2 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_ay2.txt");
gyro_az2 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_az2.txt");
gyro_ax4 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_ax4.txt");
gyro_ay4 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_ay4.txt");
gyro_az4 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_az4.txt");
gyro_roll2 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_roll2.txt");
gyro_pitch2 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_pitch2.txt");
gyro_yaw2 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_yaw2.txt");
gyro_roll4 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_roll4.txt");
gyro_pitch4 = importdata("./Data/Data_base/zzm/大腿数据_5/gyro_pitch4.txt");
gyro_yaw4 = importdata("./Data/Data_base/zzm/大腿数据_4/gyro_yaw4.txt");
output = importdata("./Data/Data_base/zzm/大腿数据_4/human_status.txt");

w1 = importdata("./BP_net/Net2/w1.txt");
w2 = importdata("./BP_net/Net2/w2.txt");
b1 = importdata("./BP_net/Net2/b1.txt");
b2 = importdata("./BP_net/Net2/b2.txt");

N = 2319;
input = zeros(12, N);
input(1,:) = interp1(0:1/(length(gyro_ax2)-1):1,gyro_ax2,0:1/(N-1):1,'linear'); %载入输入数据
input(2,:) = interp1(0:1/(length(gyro_ay2)-1):1,gyro_ay2,0:1/(N-1):1,'linear'); %载入输入数据
input(3,:) = interp1(0:1/(length(gyro_az2)-1):1,gyro_az2,0:1/(N-1):1,'linear'); %载入输入数据
input(4,:) = interp1(0:1/(length(gyro_ax4)-1):1,gyro_ax4,0:1/(N-1):1,'linear'); %载入输入数据
input(5,:) = interp1(0:1/(length(gyro_ay4)-1):1,gyro_ay4,0:1/(N-1):1,'linear'); %载入输入数据
input(6,:) = interp1(0:1/(length(gyro_az4)-1):1,gyro_az4,0:1/(N-1):1,'linear'); %载入输入数据
input(7,:) = interp1(0:1/(length(gyro_roll2)-1):1,gyro_roll2,0:1/(N-1):1,'linear'); %载入输入数据
input(8,:) = interp1(0:1/(length(gyro_pitch2)-1):1,gyro_pitch2,0:1/(N-1):1,'linear'); %载入输入数据
input(9,:) = interp1(0:1/(length(gyro_yaw2)-1):1,gyro_yaw2,0:1/(N-1):1,'linear'); %载入输入数据
input(10,:) = interp1(0:1/(length(gyro_roll4)-1):1,gyro_roll4,0:1/(N-1):1,'linear'); %载入输入数据
input(11,:) = interp1(0:1/(length(gyro_pitch4)-1):1,gyro_pitch4,0:1/(N-1):1,'linear'); %载入输入数据
input(12,:) = interp1(0:1/(length(gyro_yaw4)-1):1,gyro_yaw4,0:1/(N-1):1,'linear'); %载入输入数据

output = output';
input_test = input;
output_test =output;

[inputn,inputps]=mapminmax(input_test);%归一化到[-1,1]之间，inputps用来作下一次同样的归一化
[outputn,outputps]=mapminmax(output_test);

step1 = w1 * inputn;
step2 = tansig(step1 - b1);
step3 = w2 * step2;
step4 = tansig(step3 - b2)';
step5 = heaviside(step4 - 0.5);
outputn = heaviside(outputn - 0.5);
subplot(2,1,1);
plot(step4, "-r*");
title("测试组预测值");
hold on;
subplot(2,1,2);
plot(outputn,"-b*"); 
title("测试组期望值")




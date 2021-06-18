clear;
clc;

Data_address = "./Data/Data_base/zzm/��������_6/";
%������
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

N = 1345; %�Լ��ֶ������
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
input(1,:) = interp1(0:1/(length(gyro_ax1)-1):1,gyro_ax1,0:1/(N-1):1,'linear'); %������������
input(2,:) = interp1(0:1/(length(gyro_ay1)-1):1,gyro_ay1,0:1/(N-1):1,'linear'); %������������
input(3,:) = interp1(0:1/(length(gyro_az1)-1):1,gyro_az1,0:1/(N-1):1,'linear'); %������������
input(4,:) = interp1(0:1/(length(gyro_ax4)-1):1,gyro_ax4,0:1/(N-1):1,'linear'); %������������
input(5,:) = interp1(0:1/(length(gyro_ay4)-1):1,gyro_ay4,0:1/(N-1):1,'linear'); %������������
input(6,:) = interp1(0:1/(length(gyro_az4)-1):1,gyro_az4,0:1/(N-1):1,'linear'); %������������
input(7,:) = interp1(0:1/(length(gyro_roll1)-1):1,gyro_roll1,0:1/(N-1):1,'linear'); %������������
input(8,:) = interp1(0:1/(length(gyro_pitch1)-1):1,gyro_pitch1,0:1/(N-1):1,'linear'); %������������
input(9,:) = interp1(0:1/(length(gyro_yaw1)-1):1,gyro_yaw1,0:1/(N-1):1,'linear'); %������������
input(10,:) = interp1(0:1/(length(gyro_roll4)-1):1,gyro_roll4,0:1/(N-1):1,'linear'); %������������
input(11,:) = interp1(0:1/(length(gyro_pitch4)-1):1,gyro_pitch4,0:1/(N-1):1,'linear'); %������������
input(12,:) = interp1(0:1/(length(gyro_yaw4)-1):1,gyro_yaw4,0:1/(N-1):1,'linear'); %������������



[inputn,inputps]=mapminmax(input);%��һ����[-1,1]֮�䣬inputps��������һ��ͬ���Ĺ�һ��

w1 = importdata("./BP_net/Net2/w1.txt");
w2 = importdata("./BP_net/Net2/w2.txt");
b1 = importdata("./BP_net/Net2/b1.txt");
b2 = importdata("./BP_net/Net2/b2.txt");

step1 = w1 * inputn;
step2 = tansig(step1 - b1);
step3 = w2 * step2;
step4 = tansig(step3 - b2)';
step5 = heaviside(step4 - 0.5);

figure(1);
plot(gyro_ax1);
hold on;
plot(gyro_ay1);
hold on;
plot(gyro_az1);
hold on;
plot(step5);
title("1�ż��ٶ����� ��ŵ����");
xlabel("ʱ��s");ylabel("���ٶ�m/s^2");
legend("ax1","ay1","az1","Ԥ����ŵ�");


figure(2);
plot(gyro_roll1);
hold on;
plot(gyro_pitch1);
hold on;
plot(gyro_yaw1);
hold on;
plot(step5');
title("1�ŽǶ����� ��ŵ����");
xlabel("ʱ��s");ylabel("�Ƕ�");
ylim([-90,90]);
legend("roll","pitch","yaw","Ԥ����ŵ�");










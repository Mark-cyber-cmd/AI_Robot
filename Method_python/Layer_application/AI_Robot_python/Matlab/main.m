clear;
clc;

%������
gyro_1 = importdata('../Data/Data_base/zzm/��������_1/gyro_data_1.txt');
gyro_2 = importdata('../Data/Data_base/zzm/��������_1/gyro_data_4.txt');

gyro_new_2 = interp1(0:714, gyro_2, 0:725);

num=726;%�ܹ�1000����
a=rand(1,num);
a(a>0.5)=1;
a(a<=0.5)=0;

figure(1);
subplot(2,1,1);
plot(gyro_2);

subplot(2,1,2);
plot(gyro_new_2);

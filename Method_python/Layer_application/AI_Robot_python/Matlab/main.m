clear;
clc;

%主程序
x_axis = importdata('x_axis.txt');
y_axis = importdata('y_axis.txt');
x_diff =  zeros(1,100);
x_length = (length(y_axis) - mod(length(y_axis),6)) / 6;
y_axis_1 = zeros(1,x_length);
y_axis_2 = zeros(1,x_length);
y_axis_3 = zeros(1,x_length);
y_axis_4 = zeros(1,x_length);
y_axis_5 = zeros(1,x_length);
y_axis_6 = zeros(1,x_length);
for i=1:(length(y_axis) - mod(length(y_axis),6)) / 6
    y_axis_1(i) = y_axis(6*i - 5);
    y_axis_2(i) = y_axis(6*i - 4);
    y_axis_3(i) = y_axis(6*i - 3);
    y_axis_4(i) = y_axis(6*i - 2);
    y_axis_5(i) = y_axis(6*i - 1);
    y_axis_6(i) = y_axis(6*i);
end

if length(x_axis) > x_length
    x_axis(:,[length(x_axis)]) = [];
end
if x_length > length(x_axis)
    y_axis(:,[x_length]) = [];
end 

%计算指令真实时间差
for i=1:length(x_axis)-1
    x_diff(i) = x_axis(i + 1) - x_axis(i);
end

subplot(6,1,1);
plot(y_axis_1,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo1','FontSize',12);

subplot(6,1,2);
plot(y_axis_2,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo2','FontSize',12);

subplot(6,1,3);
plot(y_axis_3,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo3','FontSize',12);

subplot(6,1,4);
plot(y_axis_4,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo4','FontSize',12);

subplot(6,1,5);
plot(y_axis_5,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo5','FontSize',12);

subplot(6,1,6);
plot(y_axis_6,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo6','FontSize',12);


% subplot(2,1,2);
% plot(x_diff,'r-*');
% xlabel("Time");
% ylabel("Time_diff");
% title('Plot of the time-diff','FontSize',12);

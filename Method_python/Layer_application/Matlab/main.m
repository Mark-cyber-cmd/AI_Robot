clear;
clc;

%Ö÷³ÌÐò
x_axis = importdata('x_axis.txt');
y_axis = importdata('y_axis.txt');
if length(x_axis) > length(y_axis)
    x_axis(:,[length(x_axis)]) = [];
end
if length(y_axis) > length(x_axis)
    y_axis(:,[length(y_axis)]) = [];
end   
subplot(1,1,1);
plot(x_axis,y_axis,'r-*');
xlabel("Time");
ylabel("Position");
title('Plot of the servo','FontSize',12);

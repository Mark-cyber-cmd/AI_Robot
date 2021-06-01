clear;
clc;

%Ö÷³ÌÐò
gyro_ax3 = importdata('.\Data_tmp\gyro_ax3.txt');
gyro_ay3 = importdata('.\Data_tmp\gyro_ay3.txt');
gyro_az3 = importdata('.\Data_tmp\gyro_az3.txt');
gyro_roll3 = importdata('.\Data_tmp\gyro_roll3.txt');
gyro_pitch3 = importdata('.\Data_tmp\gyro_pitch3.txt');
gyro_yaw3 = importdata('.\Data_tmp\gyro_yaw3.txt');
gyro_a_time3 = importdata('.\Data_tmp\gyro_a_time3.txt');
gyro_angel_time3 = importdata('.\Data_tmp\gyro_angel_time3.txt');
figure(1);
plot(gyro_a_time3 , gyro_ax3,"-r*");
hold on;
plot(gyro_angel_time3 , gyro_roll3,"-b*");
title("AX3");

figure(2);
plot(gyro_a_time3 , gyro_ay3,"-r*");
hold on;
plot(gyro_angel_time3 , gyro_roll3,"-b*");
title("AY3");

figure(3);
plot(gyro_a_time3 , gyro_az3,"-r*");
hold on;
plot(gyro_angel_time3 , gyro_roll3,"-b*");
title("AZ3");

figure(4);
plot(gyro_angel_time3 , gyro_roll3,"-r*");
title("ROLL3");

figure(5);
plot(gyro_angel_time3 , gyro_pitch3,"-r*");
title("PITCH3");

figure(6);
plot(gyro_angel_time3 , gyro_yaw3,"-r*");
title("YAW3");



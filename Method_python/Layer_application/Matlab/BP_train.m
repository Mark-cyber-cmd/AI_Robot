%% �˳���matlab���ʵ�ֵ�BP������
% ��ջ�������
clear;
clc

Data_address = "./Data/Data_base/zzm/��������_12/";

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
output = output';


%% �ڶ��� ����ѵ�����ݺ�Ԥ������
input_train = input(:,1:round(N*0.8));
output_train =output(1:round(N*0.8),:)';
input_test = input;
output_test =output';
%�ڵ����
inputnum=12;
hiddennum=5;%������ڵ��������鹫ʽp=sqrt(m+n)+a ���ʷֱ�ȡ2~13��������
outputnum=1;
%% ������ ѵ���������ݹ�һ��
for i=1:length(input(:,1))
    [inputn(i,:), inputps] = mapminmax(input_train(i,:));
end
[outputn, outputps] = mapminmax(output_train);
%% ���Ĳ� ����BP������
net=newff(inputn,outputn,hiddennum,{'tansig','tansig'},'trainlm');% ����ģ�ͣ����ݺ���ʹ��purelin�������ݶ��½���ѵ��

W1= net. iw{1,1};%����㵽�м���Ȩֵ
B1 = net.b{1};%�м������Ԫ��ֵ

W2 = net.lw{2,1};%�м�㵽������Ȩֵ
B2 = net. b{2};%��������Ԫ��ֵ

%% ���岽 ����������ã� ѵ��������ѧϰ���ʣ�ѵ��Ŀ����С���ȣ�
net.trainParam.epochs=1000;         % ѵ����������������Ϊ1000��
net.trainParam.lr=0.01;                   % ѧϰ���ʣ���������Ϊ0.01
net.trainParam.goal=0.00000000000000001;                    % ѵ��Ŀ����С����������Ϊ0.00001

%% ������ BP������ѵ��
net=train(net,inputn,outputn);%��ʼѵ��������inputn,outputn�ֱ�Ϊ�����������

%% ���߲� ����������һ��
inputn_test=mapminmax('apply',input_test,inputps);% ���������ݽ��й�һ��

%% �ڰ˲� BP������Ԥ��
an=sim(net,inputn_test); %��ѵ���õ�ģ�ͽ��з���

%% �ھŲ� Ԥ��������һ����������     
test_simu=mapminmax('reverse',an,outputps); %�ѷ���õ������ݻ�ԭΪԭʼ��������
error=test_simu-output_test;      %Ԥ��ֵ����ʵֵ�����

%%��ʮ�� ��ʵֵ��Ԥ��ֵ���Ƚ�
figure(1)
plot(output_test,'bo-')
hold on
plot(test_simu,'r*-')
% hold on
% plot(error,'square','MarkerFaceColor','b')
legend('����ֵ','Ԥ��ֵ','���')
xlabel('��������')
ylabel('ֵ')
[c,l]=size(output_test);
MAE1=sum(abs(error))/l;
MSE1=error*error'/l;
RMSE1=MSE1^(1/2);
disp(['-----------------------������--------------------------'])
disp(['������ڵ���Ϊ',num2str(hiddennum),'ʱ����������£�'])
disp(['ƽ���������MAEΪ��',num2str(MAE1)])
disp(['�������MSEΪ��       ',num2str(MSE1)])
disp(['���������RMSEΪ��  ',num2str(RMSE1)])
%% ��������
dlmwrite("./w1.txt",W1,'delimiter',' ','newline','pc');
dlmwrite("./w2.txt",W2,'delimiter',' ','newline','pc');
dlmwrite("./b1.txt",B1,'delimiter',' ','newline','pc');
dlmwrite("./b2.txt",B2,'delimiter',' ','newline','pc');
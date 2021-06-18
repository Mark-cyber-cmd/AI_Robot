%% �˳���matlab���ʵ�ֵ�BP������
% ��ջ�������
clear all��
clc

gyro_ax2 = importdata("./Data/Data_base/zzm/��������_4/gyro_ax2.txt");
gyro_ay2 = importdata("./Data/Data_base/zzm/��������_4/gyro_ay2.txt");
gyro_az2 = importdata("./Data/Data_base/zzm/��������_4/gyro_az2.txt");
gyro_ax4 = importdata("./Data/Data_base/zzm/��������_4/gyro_ax4.txt");
gyro_ay4 = importdata("./Data/Data_base/zzm/��������_4/gyro_ay4.txt");
gyro_az4 = importdata("./Data/Data_base/zzm/��������_4/gyro_az4.txt");
gyro_roll2 = importdata("./Data/Data_base/zzm/��������_4/gyro_roll2.txt");
gyro_pitch2 = importdata("./Data/Data_base/zzm/��������_4/gyro_pitch2.txt");
gyro_yaw2 = importdata("./Data/Data_base/zzm/��������_4/gyro_yaw2.txt");
gyro_roll4 = importdata("./Data/Data_base/zzm/��������_4/gyro_roll4.txt");
gyro_pitch4 = importdata("./Data/Data_base/zzm/��������_4/gyro_pitch4.txt");
gyro_yaw4 = importdata("./Data/Data_base/zzm/��������_4/gyro_yaw4.txt");
output = importdata("./Data/Data_base/zzm/��������_4/human_status.txt");

N = 2319;
input = zeros(12, N);
input(1,:) = interp1(0:1/(length(gyro_ax2)-1):1,gyro_ax2,0:1/(N-1):1,'linear'); %������������
input(2,:) = interp1(0:1/(length(gyro_ay2)-1):1,gyro_ay2,0:1/(N-1):1,'linear'); %������������
input(3,:) = interp1(0:1/(length(gyro_az2)-1):1,gyro_az2,0:1/(N-1):1,'linear'); %������������
input(4,:) = interp1(0:1/(length(gyro_ax4)-1):1,gyro_ax4,0:1/(N-1):1,'linear'); %������������
input(5,:) = interp1(0:1/(length(gyro_ay4)-1):1,gyro_ay4,0:1/(N-1):1,'linear'); %������������
input(6,:) = interp1(0:1/(length(gyro_az4)-1):1,gyro_az4,0:1/(N-1):1,'linear'); %������������
input(7,:) = interp1(0:1/(length(gyro_roll2)-1):1,gyro_roll2,0:1/(N-1):1,'linear'); %������������
input(8,:) = interp1(0:1/(length(gyro_pitch2)-1):1,gyro_pitch2,0:1/(N-1):1,'linear'); %������������
input(9,:) = interp1(0:1/(length(gyro_yaw2)-1):1,gyro_yaw2,0:1/(N-1):1,'linear'); %������������
input(10,:) = interp1(0:1/(length(gyro_roll4)-1):1,gyro_roll4,0:1/(N-1):1,'linear'); %������������
input(11,:) = interp1(0:1/(length(gyro_pitch4)-1):1,gyro_pitch4,0:1/(N-1):1,'linear'); %������������
input(12,:) = interp1(0:1/(length(gyro_yaw4)-1):1,gyro_yaw4,0:1/(N-1):1,'linear'); %������������
output = output';
%%��һ�� ��ȡ����
% input=randi([1 20],2,200);  %������������
% output=input(1,:)'+input(2,:)';  %�����������

%% �ڶ��� ����ѵ�����ݺ�Ԥ������
input_train = input(:,1:2000);
output_train =output(1:2000,:)';
input_test = input(:,2000:2319);
output_test =output(2000:2319,:)';
%�ڵ����
inputnum=12;
hiddennum=5;%������ڵ��������鹫ʽp=sqrt(m+n)+a ���ʷֱ�ȡ2~13��������
outputnum=1;
%% ������ ѵ���������ݹ�һ��
[inputn,inputps]=mapminmax(input_train);%��һ����[-1,1]֮�䣬inputps��������һ��ͬ���Ĺ�һ��
[outputn,outputps]=mapminmax(output_train);
%% ���Ĳ� ����BP������
net=newff(inputn,outputn,hiddennum,{'tansig','tansig'},'trainlm');% ����ģ�ͣ����ݺ���ʹ��purelin�������ݶ��½���ѵ��

W1= net. iw{1,1};%����㵽�м���Ȩֵ
B1 = net.b{1};%�м������Ԫ��ֵ

W2 = net.lw{2,1};%�м�㵽������Ȩֵ
B2 = net. b{2};%��������Ԫ��ֵ

%% ���岽 ����������ã� ѵ��������ѧϰ���ʣ�ѵ��Ŀ����С���ȣ�
net.trainParam.epochs=1000;         % ѵ����������������Ϊ1000��
net.trainParam.lr=0.0001;                   % ѧϰ���ʣ���������Ϊ0.01
net.trainParam.goal=0.000000000000001;                    % ѵ��Ŀ����С����������Ϊ0.00001

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
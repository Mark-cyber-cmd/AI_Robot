using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;

namespace clicent
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }
       
        Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
       


        void showMsg1(string msg)
        {
            messageshow.AppendText(msg + "\r\n");
        }//在状态栏显示 msg 中的信息

        void disconnect(int number)
        {
            if (number == 1)
            {
                this.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    sensor1.Text = ("已掉线，请重连");

                });
            }
            if (number == 2)
            {
                this.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    sensor2.Text = ("已掉线，请重连");

                });
            }
            if (number == 3)
            {
                this.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    sensor3.Text = ("已掉线，请重连");

                });
            }
            if (number == 4)
            {
                this.Dispatcher.BeginInvoke((Action)delegate ()
                {
                    sensor4.Text = ("已掉线，请重连");

                });
            }

        }//根据 number 来显示第几个传感器掉线

        private void ReceiveMsg()//在接受数据后在指定位置显示
        {
            byte[] result = new Byte[11];
            byte[] msg = new Byte[11];
            int number = 0;
            clientSocket.ReceiveTimeout = 5000;
            while (true)
            {
                //通过clientSocket接收数据。Receive表示接受服务器的数据。


                try
                {
                    number++;
                    clientSocket.Receive(result);
                    string message1 = BitConverter.ToString(result);
                    Int16 Z = BitConverter.ToInt16(result, 0);
                    if (number == 4) number = 0;
                    if (Z == 21333 && number == 1)
                    {
                        //计算角度

                        Int16 angle = BitConverter.ToInt16(result, 2);
                        string anglexx = Convert.ToString(angle * 180 / 32768.0);
                        anglexx = Convert.ToDecimal(anglexx).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglex1.Text = anglexx;
                        });

                        angle = BitConverter.ToInt16(result, 4);
                        string angleyy = Convert.ToString(angle * 180 / 32768.0);
                        angleyy = Convert.ToDecimal(angleyy).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            angley1.Text = angleyy;
                        });

                        angle = BitConverter.ToInt16(result, 6);
                        string anglezz = Convert.ToString(angle * 180 / 32768.0);
                        anglezz = Convert.ToDecimal(anglezz).ToString("0.00");


                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglez1.Text = anglezz;
                        });

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            sensor1.Text = "成功上线";
                        });
                    }//显示第一个传感器的角度信息
                    if (Z == 21333 && number == 2)
                    {
                        //计算角度

                        Int16 angle = BitConverter.ToInt16(result, 2);
                        string anglexx = Convert.ToString(angle * 180 / 32768.0);
                        anglexx = Convert.ToDecimal(anglexx).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglex2.Text = anglexx;
                        });

                        angle = BitConverter.ToInt16(result, 4);
                        string angleyy = Convert.ToString(angle * 180 / 32768.0);
                        angleyy = Convert.ToDecimal(angleyy).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            angley2.Text = angleyy;
                        });

                        angle = BitConverter.ToInt16(result, 6);
                        string anglezz = Convert.ToString(angle * 180 / 32768.0);
                        anglezz = Convert.ToDecimal(anglezz).ToString("0.00");


                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglez2.Text = anglezz;
                        });
                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            sensor2.Text = "成功上线";
                        });
                    }
                    if (Z == 21333 && number == 3)
                    {
                        //计算角度

                        Int16 angle = BitConverter.ToInt16(result, 2);
                        string anglexx = Convert.ToString(angle * 180 / 32768.0);
                        anglexx = Convert.ToDecimal(anglexx).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglex3.Text = anglexx;
                        });

                        angle = BitConverter.ToInt16(result, 4);
                        string angleyy = Convert.ToString(angle * 180 / 32768.0);
                        angleyy = Convert.ToDecimal(angleyy).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            angley3.Text = angleyy;
                        });

                        angle = BitConverter.ToInt16(result, 6);
                        string anglezz = Convert.ToString(angle * 180 / 32768.0);
                        anglezz = Convert.ToDecimal(anglezz).ToString("0.00");


                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglez3.Text = anglezz;
                        });

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            sensor3.Text = "成功上线";
                        });
                    }
                    if (Z == 21333 && number == 4)
                    {
                        //计算角度

                        Int16 angle = BitConverter.ToInt16(result, 2);
                        string anglexx = Convert.ToString(angle * 180 / 32768.0);
                        anglexx = Convert.ToDecimal(anglexx).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglex4.Text = anglexx;
                        });

                        angle = BitConverter.ToInt16(result, 4);
                        string angleyy = Convert.ToString(angle * 180 / 32768.0);
                        angleyy = Convert.ToDecimal(angleyy).ToString("0.00");

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            angley4.Text = angleyy;
                        });

                        angle = BitConverter.ToInt16(result, 6);
                        string anglezz = Convert.ToString(angle * 180 / 32768.0);
                        anglezz = Convert.ToDecimal(anglezz).ToString("0.00");


                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            anglez4.Text = anglezz;
                        });

                        this.Dispatcher.BeginInvoke((Action)delegate ()
                        {
                            sensor4.Text = "成功上线";
                        });
                    }
                }
                catch (Exception)
                {
                    disconnect(number);
                }



            }
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            IPAddress ip = IPAddress.Parse(this.ipaddress.Text.Trim());
            
            try
            {

                //Connect表示客户端向服务器发起连接请求。而在服务端，用Accept()响应该请求。
                clientSocket.Connect(new IPEndPoint(ip, Convert .ToInt32 (this .duankouaddress.Text .Trim ())));
                showMsg1("连接成功");
                byte[] message = new byte[] { 0x55, 0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                clientSocket.Send(message);
                showMsg1("成功发送编号");
                byte[] message1 = new byte[] { 0x55, 0xFF, 0xAA, 0x69, 0x88, 0xB5, 0x00, 0x00, 0x00, 0x00, 0x00 };
                clientSocket.Send(message1);
                System.Threading.Thread.Sleep(500);
                byte[] message2 = new byte[] { 0x55, 0xFF, 0xAA, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                clientSocket.Send(message2);
                showMsg1("成功发送调零指令");
                byte[] message3 = new byte[] { 0x55, 0xFF, 0xAA, 0x69, 0x88, 0xB5, 0x00, 0x00, 0x00, 0x00, 0x00 };
                clientSocket.Send(message3);
                System.Threading.Thread.Sleep(500);
                byte[] message4 = new byte[] { 0x55, 0xFF, 0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
                clientSocket.Send(message4);
                showMsg1("成功发送退出设置指令");

                var th = new Thread(ReceiveMsg);
                th.Start();
                
               
            }
            catch
            {
                showMsg1("连接服务器失败,请按回车键退出");
                return;
            }
            
        }

        private void tiaoling_Click(object sender, RoutedEventArgs e)
        {
            byte[] tl = new byte[] { 0x55, 0xFF, 0xAA, 0x69, 0x88, 0xB5, 0x00, 0x00, 0x00, 0x00, 0x00 };
            clientSocket.Send(tl);
            System.Threading.Thread.Sleep(500);
            byte[] tiaoling = new byte[] { 0x55, 0xFF, 0xAA, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
            clientSocket.Send(tiaoling);
            this.Dispatcher.BeginInvoke((Action)delegate ()
            {
                showMsg1("调零指令已发送");

            });
            System.Threading.Thread.Sleep(500);
            byte[] message3 = new byte[] { 0x55, 0xFF, 0xAA, 0x69, 0x88, 0xB5, 0x00, 0x00, 0x00, 0x00, 0x00 };
            clientSocket.Send(message3);
            System.Threading.Thread.Sleep(500);
            byte[] message4 = new byte[] { 0x55, 0xFF, 0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
            clientSocket.Send(message4);
            this.Dispatcher.BeginInvoke((Action)delegate ()
            {
                showMsg1("退出指令已发送");

            });
        }

       
    }
}


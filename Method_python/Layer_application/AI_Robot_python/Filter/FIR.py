import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']   # 显示中文
mpl.rcParams['axes.unicode_minus'] = False       # 显示负号
N = 726    # 采样点的个数
x = np.arange(0, 2*np.pi, 2*np.pi/N)
# 产生频率为120、500、10hz的信号进行模拟
y = 7 * np.sin(120*x) + 5 * np.sin(500 * x) + 9 * np.sin(10 * x)

w = np.arange(0, N, 1)  # 频域轴

b = signal.firwin(N,  2*10/N, window='hamming')   # 哈明窗，截至频率100Hz
print(b)
w, h = signal.freqz(b)    # 求频响
plt.figure(1)
plt.subplot(2, 1, 1)
plt.title("幅频响应")
plt.plot(w/2/np.pi*N, 20*np.log10(np.abs(h)+0.01))
plt.subplot(2, 1, 2)
plt.title("相频响应")
plt.plot(w/2/np.pi*N, np.angle(h))
plt.xlim(0, 100)
plt.show()

t = np.arange(0, 2, 1/N)
sweep = signal.chirp(t, f0=0, t1=2, f1=20.0)
out = signal.lfilter(b, [1.], sweep)
plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(t, sweep)
plt.subplot(2, 1, 2)
plt.plot(t, out)
plt.show()



# 设计模拟滤波器并绘制其频率响应，显示关键点：
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


t = np.arange(0, 2, 1/800.0)
sweep = signal.chirp(t, f0=0, t1=2, f1=30.0)
sos = signal.butter(10, np.pi / 1284, 'lp', output='sos')
filtered = signal.sosfilt(sos, sweep)
fig, (ax2) = plt.subplots(1, 1, sharex=True)
ax2.plot(t, filtered, color='green')
ax2.set_title('After 15 Hz high-pass filter')
ax2.axis([0, 2, -2, 2])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()




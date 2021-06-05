# -*-coding:utf-8 -*-
import numpy as np
from scipy import interpolate
import pylab as pl

x = np.linspace(0, 2 * np.pi, 715)
x_new = np.linspace(0, 2*np.pi, 726)

y = np.sin(x)
pl.plot(x, y, "ro")

f = interpolate.interp1d(x, y, kind="slinear")
ynew = f(x_new)
pl.plot(x_new, ynew,  "bo", label=str("slinear"))
pl.legend(loc="lower right")
pl.show()
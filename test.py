import time

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

for _ in range(100):
    x = np.random.rand(10)
    plt.plot(x)
    plt.ylim(0, 1)
    plt.draw()
    plt.pause(0.005)
    fig.clear()

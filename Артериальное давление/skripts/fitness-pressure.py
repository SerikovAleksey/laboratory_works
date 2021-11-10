import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from textwrap import wrap
k = 11.4
with open('fitness.txt', 'r') as fit:
    tmpfit = fit.read().split("\n")
    tmpfit_x = []
    tmpfit_y = []
    time = []
    time1 = []
    count = []
    for i in range(7, len(tmpfit) - 1, 1):
        tmpfit_y.append(int(tmpfit[i]) / k)
    time1 = tmpfit[3].split(" ")
    time = time1[4].split(".")
    count = tmpfit[6].split(" ")
    tmpfit_x = np.linspace(0, int(time[0]), int(count[4]))


fig, ax = plt.subplots(figsize=(16, 10), dpi=250)
#plt.title('Артериальное давление после физической нагрузки', fontsize=7, color='black')
title = 'Артериальное давление после физической нагрузки'
ax.set_title("\n".join(wrap(title, 100)))
ax.plot(tmpfit_x, tmpfit_y, color='b', linewidth=0.6)
plt.axis([0, int(time[0]) + 5, 60, 190])
plt.ylabel('Давление [мм рт. ст.]', fontsize=7)
plt.xlabel('Время [с]', fontsize=7)
ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.tick_params(which='major', length=5, labelsize=5)
ax.tick_params(which='minor', length=3)
ax.grid(which='major', color='black', linewidth=0.2)
ax.minorticks_on()
ax.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)
graph = mlines.Line2D([], [], color='blue', markersize=20, label='P = N * k')
plt.legend(handles=[graph])
plt.show()
fig.savefig("Pressure-fitness.png")
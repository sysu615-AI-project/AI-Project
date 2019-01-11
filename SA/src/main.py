import matplotlib.pyplot as plt
import re
import random
import math

filename = "../tc/ch130.tsp"

def main():
    x = []
    y = []
    with open(filename) as file:
        for line in file.readlines()[6:-1]:
            k = re.split('[ ]+', line.strip())
            x.append(float(k[1]))
            y.append(float(k[2]))
    plt.ion()
    ax = plt.subplot(111)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.plot(x, y, '-ro')
    plt.pause(0.001)
    path = []
    dis = []
    length = 0
    for i in range(0, len(x)):
        temp = []
        for j in range(0, len(x)):
            temp.append(int(((x[i] - x[j])**2 + (y[i] - y[j])**2) ** 0.5 + 0.5))
        dis.append(temp)
        path.append(i)
    path.append(0)
    for i in range(0, len(path) - 1):
        length = length + dis[path[i]][path[i + 1]]
    t, a, MapkobChainLength= 1000.0, 0.98, int(len(x) * len(x) / 2)
    dE, count, lastLength = 0, 0, 0
    if MapkobChainLength > 10000:
        MapkobChainLength = 10000
    while t > 0.01 and count < 20:
        for k in range(MapkobChainLength):
            i = random.randint(1, len(x) - 2)
            j = random.randint(i + 1, len(x) - 1)
            dE = dis[path[i - 1]][path[j]] + dis[path[i]][path[j + 1]] -\
                 dis[path[i - 1]][path[i]] - dis[path[j]][path[j + 1]]
            if dE <= 0 or random.random() < math.exp(-dE / t):
                path[i:j+1] = path[j:i-1:-1]
                length = length + dE
        if length == lastLength:
            count = count + 1
        else :
            lastLength = length
            count = 0
        ax.cla()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for n in range(len(path) - 1):
            ax.plot([x[path[n]], x[path[n + 1]]], [y[path[n]], y[path[n + 1]]], '-ro')
        plt.pause(0.001)
        t = a * t
    ax.cla()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for n in range(len(path) - 1):
        ax.plot([x[path[n]], x[path[n + 1]]], [y[path[n]], y[path[n + 1]]], '-ro')
    plt.ioff()
    print(length)
    print(path)
    plt.show()

if __name__ == "__main__":
    main()
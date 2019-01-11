import matplotlib.pyplot as plt
import re
import random
import math

filename = "../tc/ch130.tsp"

def disturbance(path):
    size = len(path)
    ran = random.randint(2, size - 1)
    path[1:size - ran], path[size - ran:size - 1] = path[ran:size - 1], path[1:ran]

def localSearch(dis, path, count):
    disturbance(path)
    size = len(path) - 1
    length = 0
    for i in range(size):
        length = length + dis[path[i]][path[i + 1]]
    for i in range(1, size - 1):
        for j in range(i + 1, size):
            tempDE = dis[path[i - 1]][path[j]] + dis[path[i]][path[j + 1]] -\
                     dis[path[i - 1]][path[i]] - dis[path[j]][path[j + 1]]
            if tempDE < 0:
                length = length + tempDE
                path[i:j+1] = path[j:i-1:-1]
            k = int((i + j) / 2 + 0.5)
            tempDE = dis[path[i - 1]][path[k]] + dis[path[k]][path[i + 1]] +\
                     dis[path[i]][path[k + 1]] + dis[path[k - 1]][path[i]] -\
                     dis[path[i - 1]][path[i]] - dis[path[i]][path[i + 1]] -\
                     dis[path[k - 1]][path[k]] - dis[path[k]][path[k + 1]] +\
                     (k == i + 1) * 2 * dis[path[i]][path[k]]
            if tempDE < 0:
                length = length + tempDE
                path[i], path[k] = path[k], path[i]
    return length

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
    for i in range(0, len(x)):
        length = length + dis[path[i]][path[i + 1]]
    max_iterations, count = 50, 0
    pathSize = len(path)
    bestPath = path[:]
    bestPathLength = length
    while count < max_iterations:
        length = localSearch(dis, path, count)
        if length < bestPathLength:
            bestPathLength = length
            bestPath = path[:]
        ax.cla()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for n in range(pathSize - 1):
            ax.plot([x[path[n]], x[path[n + 1]]], [y[path[n]], y[path[n + 1]]], '-ro')
        plt.pause(0.001)
        count = count + 1
    ax.cla()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    for n in range(pathSize - 1):
        ax.plot([x[bestPath[n]], x[bestPath[n + 1]]], [y[bestPath[n]], y[bestPath[n + 1]]], '-ro')
    plt.ioff()
    print(bestPathLength)
    print(bestPath)
    plt.show()

if __name__ == "__main__":
    main()
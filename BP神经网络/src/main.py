import struct
import matplotlib.pyplot as plt
import random
import numpy as np

# 训练集文件
train_images_idx3_ubyte_file = '../tc/train-images.idx3-ubyte'
# 训练集标签文件
train_labels_idx1_ubyte_file = '../tc/train-labels.idx1-ubyte'

# 测试集文件
test_images_idx3_ubyte_file = '../tc/t10k-images.idx3-ubyte'
# 测试集标签文件
test_labels_idx1_ubyte_file = '../tc/t10k-labels.idx1-ubyte'

class BPNet:
    def __init__(self):
        self.expect_num = [0.01, 0.99]
        self.weightIH, self.weightHO = [], []

    def calculationOffset(self, rowsNum, columnsNum, index):
        return rowsNum * columnsNum * index + 16

    def weightGenerator(self, weight, row, column):
        temp = 4.8 / row
        for i in range(row):
            for j in range(column):
                weight[i].append((random.random() - 0.5) * temp)

    def f(self, a, b):
        return 1/(1+np.exp(-1 * a @ b))

    def d(self, i):
        a = np.array([self.expect_num[0]] * 10)
        a[i] = 0.99
        return a

    def train(self):
        labels = []
        with open(train_labels_idx1_ubyte_file, "rb") as file:
            magicNumber, labelsSize = struct.unpack('>ii', file.read(8))
            if magicNumber == 2049:
                print("label")
            else :
                print("Can't recognized")
                return 0
            labels = file.read()
        with open(train_images_idx3_ubyte_file, "rb") as file:
            magicNumber, numOfImages, rowsNum, columnsNum = struct.unpack('>iiii', file.read(16))
            if magicNumber == 2051:
                print("image")
            else :
                print("Can't recognized")
                return 0
            # 神经元节点
            # 输入层, 隐层, 输出层
            inputLayerNodeNum, hideLayerNodeNum, outputLayerNodeNum = rowsNum * columnsNum, 38, 10
            # 权值
            self.weightIH, self.weightHO = [[] for i in range(inputLayerNodeNum)], [[] for i in range(hideLayerNodeNum)]
            self.weightGenerator(self.weightIH, inputLayerNodeNum, hideLayerNodeNum)
            self.weightIH = np.array(self.weightIH)
            self.weightGenerator(self.weightHO, hideLayerNodeNum, outputLayerNodeNum)
            self.weightHO = np.array(self.weightHO)
            count, formatStr, yita = 0, '>' + str(inputLayerNodeNum) + 'B', 0.1
            while count < numOfImages:
                pixes = np.array([struct.unpack(formatStr, file.read(inputLayerNodeNum))])
                Ioutput = 1 / (1 + np.exp(-1 * pixes))
                Houtput = self.f(Ioutput, self.weightIH)
                Ooutput = self.f(Houtput, self.weightHO)
                EO = Ooutput * (1 - Ooutput) * (self.d(labels[count]) - Ooutput)
                EH = Houtput * (1 - Houtput) * (self.weightHO @ EO.T).T
                self.weightHO = self.weightHO + yita * Houtput.T @ EO
                self.weightIH = self.weightIH + yita * Ioutput.T @ EH
                count = count + 1
                if np.mod(count, 1000) == 0:
                    print("已训练 " + str(count) + " 张图片")
            self.test()

    def test(self):
        labels = []
        with open(test_labels_idx1_ubyte_file, "rb") as file:
            magicNumber, labelsSize = struct.unpack('>ii', file.read(8))
            if magicNumber == 2049:
                print("label")
            else :
                print("Can't recognized")
                return 0
            labels = file.read()
        with open(test_images_idx3_ubyte_file, "rb") as file:
            magicNumber, numOfImages, rowsNum, columnsNum = struct.unpack('>iiii', file.read(16))
            if magicNumber == 2051:
                print("image")
            else :
                print("Can't recognized")
                return 0
            inputNode = rowsNum * columnsNum
            count, formatStr = 0, '>' + str(inputNode) + 'B'
            countTrue = 0
            while count < numOfImages:
                pixes = np.array([struct.unpack(formatStr, file.read(inputNode))])
                Ioutput = 1 / (1 + np.exp(-1 * pixes))
                Houtput = self.f(Ioutput, self.weightIH)
                Ooutput = self.f(Houtput, self.weightHO)
                if labels[count] == np.argmax(Ooutput):
                    countTrue = countTrue + 1
                count = count + 1
            print(countTrue)
            print("正确率为: " + str(countTrue * 100.0 / numOfImages) + "%")

if __name__ == "__main__":
    bp = BPNet()
    bp.train()
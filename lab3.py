
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D


def writefile():
    x=np.random.randint(-100,100,100)
    y=np.random.randint(-100,100,100)
    z=np.random.randint(-100,100,100)
    tmp=np.zeros((100,3),dtype=int)
    for i in range(100):
        tmp[i][0]=x[i]
        tmp[i][1]=y[i]
        tmp[i][2]=z[i]
    np.savetxt('data3.txt',tmp)


def readfile(filepath):
    data=np.loadtxt(filepath,skiprows=1)
    with open(filepath) as file:
        numbers=file.readline()
        file.close()
    numbers=(int)(numbers)
    return numbers,data


def draw(data,y_hat):
    x=data[:,0]
    y=data[:,1]
    z=data[:,2]
    fig = plt.figure(figsize=(12, 8))
    ax = Axes3D(fig,  elev=30, azim=20)
    ax.scatter(x,y,z,c=y_hat)
    plt.show()


def kmeans(data):
    K=int(input("输入聚类个数\n"))
    y_hat= KMeans(n_clusters=K, random_state=9,max_iter=100).fit_predict(data)
    print(y_hat)
    draw(data,y_hat)


if __name__=='__main__':
    filepath='data3.txt'
    numbers,data=readfile(filepath)
    kmeans(data)

















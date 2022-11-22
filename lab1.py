
'''
Descripttion: Do not Edit
version: Do not Edit
Author: czjoyit@qq.com
Date: 2022-11-17 12:03:48
LastEditors: Capzlime czjoyit@qq.com
LastEditTime: 2022-11-22 15:01:19
'''

import numpy as np
import math
import pandas as pd


def read(filepath):
    data=np.loadtxt(filepth,dtype=int,delimiter=',')
    data.sort()
    return data


def resize(depth,data):
    data=data.reshape(int(data.size/depth),depth)
    x=data.shape[0]
    y=data.shape[1]
    return data,x,y


def init_box(x,y):
    return np.zeros([x,y])


# 均值深箱 
def mean(x,y,mean_data):
    for i in range(x):
        for j in range(y):
            mean_data[i][j]=int(data[i].mean())


# 中值深箱
def medin_mean(x,y,medin_mean_data):
    med=int(y/2)
    for i in range(x):
        tmp=data[i][med]
        for j in range(y):
            medin_mean_data[i][j]=tmp


# 边界值深箱
def edge_mean(x,y,edge_mean_data):
    for i in range(x):
        left_edge=data[i][0]
        right_edge=data[i][-1]
        for j in range(y):
            if(j==0):
                edge_mean_data[i][j]=left_edge
            elif(j==y):
                edge_mean_data[i][j]=right_edge
            else:
                if(abs(left_edge-data[i][j])<=abs(right_edge-data[i][j])):
                    edge_mean_data[i][j]=left_edge
                else:
                    edge_mean_data[i][j]=right_edge


def quan(filepth):
    data=read(filepth)
    df=pd.Series(data)
    q1,q3=df.quantile([0.25,0.75])
    iqr=q3-q1
    outlier = df[(df> q3 + iqr * 1.5) | (df< q1 - iqr * 1.5)]
    print("lqr is :",iqr)
    print("outlier is :",outlier)


if __name__=='__main__':
    filepth="data1.txt"
    data=read(filepth)
    depth=3
    data,x,y=resize(depth,data)

    mean_data=init_box(x,y)
    medin_mean_data=init_box(x,y)
    edge_mean_data=init_box(x,y)
    quan(filepth)

    mean(x,y,mean_data)
    medin_mean(x,y,medin_mean_data)
    edge_mean(x,y,edge_mean_data)
    print(data)
    print(mean_data)
    print(medin_mean_data)
    print(edge_mean_data)




















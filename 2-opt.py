import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import math
source=''
sequence=[]
bag=[]
city_number=51
midu=[]
n=1
R=1
#cost coefficient
r=9.72
#Backpack capacity
weight_sum=4452
city_weight=np.load("city_weightByiss.npy")
city_value=np.load("city_valueByiss.npy")
with open(source, "r") as lines:
    lines = lines.readlines()
    lines = lines[10:61]
    for line in lines:
        xy = line.split()
        sequence.append([float(xy[1]), float(xy[2])])
    with open(source, "r") as lines:
        lines = lines.readlines()
        lines = lines[62:113+(city_number-1)*(n-1)-1]
        for line in lines:
            xy = line.split()
            bag.append([float(xy[1]), float(xy[2])])
sequence=np.array(sequence)
def cal_dis(city_condition):
    Distance = np.zeros((51, 51))
    for i in range(51):
        for j in range(51):
            if i != j:
                Distance[i][j] = math.sqrt(
                    (city_condition[i][0] - city_condition[j][0]) ** 2 + (
                            city_condition[i][1] - city_condition[j][1]) ** 2)
            else:
                Distance[i][j] = 100000
    return Distance
def cal_z(route,distance):
    w=0
    v=0
    time=0
    for i in range(city_number):
        w=w+city_weight[int(route[i])]
        v=v+city_value[int(route[i])]
        s = (-0.9 / weight_sum) * w + 1
        time=time+distance[int(route[i])][int(route[i+1])]/s
    z=v-r*time
    return z
def cal_z_bit(route,distance,itemchosed):
    w=0
    v=0
    time=0
    for i in range(city_number):
        if itemchosed[int(route[i])]==1:
            w=w+bag[int(route[i])-1][1]
            v=v+bag[int(route[i])-1][0]
        s = (-0.9 / weight_sum) * w + 1
        time = time + distance[int(route[i])][int(route[i + 1])] / s
    z = v - r * time
    return z

def reverse(route, i , k):
    while i <k:
        temp=route[i]
        route[i]=route[k]
        route[k]=temp
        i=i+1
        k=k-1
    return route
def two_opt(route,distance):
    z = cal_z(route, distance)
    z_1=0
    for i in range(1,city_number-2):
        for k in range(i+1,city_number-1):
            route_1=route.copy()
            route=reverse(route,i,k)
            z_1=cal_z(route,distance)
            if z_1>z:
                route_1=route
                z=z_1
            else:
                route=route_1
    return route,z
def loop_two_opt(route,z):
    route_2, z_1 = two_opt(route, Distance)
    while z_1>z:
        z=z_1
        route=route_2.copy()
        route_2, z_1 = two_opt(route, Distance)
    return route_2,z
def cal_weight_value(itemchosed):
    item_weight=0
    item_value=0
    for i in range(city_number):
        if itemchosed[i]==1:
            item_weight=item_weight+bag[i-1][1]
            item_value=item_value+bag[i-1][0]
    return item_value,item_weight
def bitflip(route, city_weight,city_value):
    item_chose=np.zeros(city_number)
    z_pre=cal_z(route,Distance)

    for i in range(city_number):
        if city_weight[i]==0:
            item_chose[i]=0
        else:
            item_chose[i]=1
    _, item_weight = cal_weight_value(item_chose)
    for j in range(1,city_number):
        if item_chose[j]==0:
            item_chose[j]=1
            _,item_weight=cal_weight_value(item_chose)

            if item_weight>weight_sum*R:
                item_chose[j]=0
            else:
               z_bit = cal_z_bit(route, Distance, item_chose)
               if z_bit>z_pre:
                    z_pre=z_bit
        else:
            item_chose[j] = 0
            z_bit = cal_z_bit(route, Distance, item_chose)
            if z_bit > z_pre:
                item_value, item_weight = cal_weight_value(item_chose)
                z_pre = z_bit
            else:
                item_chose[j]=1

if __name__ == '__main__':
    route = np.load("GACOpath.npy")
    route=route[0]
    weight=city_weight.sum()
    Distance=cal_dis(sequence)
    z=cal_z(route,Distance)
    route_2,z_1=loop_two_opt(route,z)
    np.save("route_2opt",route_2)
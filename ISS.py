import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['font.sans-serif'] = ['KaiTi']
#Backpack capacity
weight_sum=18270
#Dataset Path
source=''

city_condition=[]
n=1
#Classification coefficient
r=0.4

R=1
#Number of cities
city_number=51
bag=[]
with open(source,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    lines = lines[10:61]
    for line in lines:
        line = line.split()
        city_condition.append([float(line[1]), float(line[2])])
city_condition = np.array(city_condition)
with open(source, "r") as lines:
    lines = lines.readlines()
    lines = lines[62:113]
    for line in lines:
        xy = line.split()
        bag.append([float(xy[1]), float(xy[2])])
bag=np.array(bag)
midu=bag[:,0]/bag[:,1]
city_condition=np.array(city_condition)
def first(weight_sum,midu,bag):
    city=[]
    w=0
    v=0
    midu=midu.tolist()
    while w<weight_sum*r:
        index=midu.index(max(midu))
        w=w+bag[index][1]
        v = v + bag[index][0]
        midu[index]=0
        city.append(index)
    return city,w
def draw_city(city_condition,city):
    fig = plt.figure()
    city_pass=[]
    x=np.zeros(city_number)
    for i in city:
        city_pass.append(i+1)
    for i in city_pass:
        x[i]=x[i]+1
    for j in range(city_number):
        if (j in city_pass) and x[j]==1:
             plt.plot(city_condition[j][0] ,city_condition[j][1], 'v-r')
        elif (j in city_pass) and x[j]==2:
            plt.plot(city_condition[j][0], city_condition[j][1], 's-g')
        elif  (j in city_pass) and x[j] == 3:
            plt.plot(city_condition[j][0], city_condition[j][1], 'D-y')
        else:
            plt.plot(city_condition[j][0], city_condition[j][1], 'o-b')
    plt.title("item")
    plt.show()
    return x
def max_citycondition(city_condition):
    max_x=0
    max_y=0
    min_x=10000
    min_y=10000
    edge=[]
    for i in range(city_number):
        if city_condition[i][0]>max_x:
            max_x=city_condition[i][0]
        if city_condition[i][1]>max_y:
            max_y=city_condition[i][1]
        if city_condition[i][0] < min_x:
            min_x = city_condition[i][0]
        if city_condition[i][1] < min_y:
            min_y = city_condition[i][1]
    edge.append(min_x)
    edge.append(min_y)
    edge.append(max_x)
    edge.append(max_y)
    return edge
def judgesearch(x,city_condition,edge):
    x_dis=edge[2]-edge[0]
    y_dis=edge[3]-edge[1]
    edge_length=max((x_dis,y_dis))/3
    x_ini=edge[0]+edge_length
    y_ini=edge[1]+edge_length
    path=edge_length/10
    count_max1=0
    x_max=[]
    while x_ini<=edge[2]:
        while y_ini<=edge[3]:
            count_max=0
            for i in range(0,city_number):
                if city_condition[i][0]<=x_ini and city_condition[i][0]>=x_ini-edge_length and city_condition[i][1]<=y_ini and city_condition[i][1]>=y_ini-edge_length:
                    if (i-1 )  in x:
                       count_max=count_max+bag[i-1][1]
                    if (i-1)+city_number-1 in x:
                        count_max = count_max + bag[(i-1)+city_number-1 ][1]
                    if (i-1)+(city_number-1)*2 in x:
                        count_max = count_max + bag[(i - 1) + (city_number - 1)*2][1]
            if count_max>count_max1:
                count_max1=count_max
                x_max.append(x_ini)
                x_max.append(y_ini)
            y_ini=y_ini+path
        x_ini=x_ini+path
        y_ini=edge[1]+edge_length
    return count_max1,x_max,edge_length
def add_two(judge, citycondition, city_first, w, midu):
    w_now=0
    city_second=[]
    v=0
    midu=midu.tolist()
    for i in range(len(midu)):
        if i in city_first:
            midu[i]=0
    j=0
    while w_now+w<weight_sum*R and j<len(midu):
        x=0
        index = midu.index(max(midu))
        midu[index]=0
        j=j+1
        if index>49 and index <=99:
            x=index-city_number+1
        elif index>99:
            x=index-(city_number-1)*2
        else:
            x=index
        if citycondition[x+1][0]<=judge[0] and citycondition[x+1][0]>=judge[0]-edge_length and citycondition[x+1][1]<=judge[1] and citycondition[x+1][1]>=judge[1]-edge_length:
            w_now = w_now + bag[index][1]
            if w_now+w <weight_sum*R:
                v = v + bag[index][0]
                city_second.append(index)
            else:
                w_now=w_now-bag[index][1]
    return city_second
def cal_v_w(city):
    w=0
    v=0
    for i  in range(len(bag)):
        if i in city:
           w=w+bag[i][1]
           v=v+bag[i][0]
    print("weight:"+str(w)+"value："+str(v))
    return w
def cal_max(x,y,z,a,b,c):
    sum=0
    minz=min(x,y,z)
    if x!=minz:
        sum=sum+a
    if y != minz:
        sum=sum+b
    if z != minz:
        sum=sum+c
    return  sum
def cal_max_one(x,y,z,a,b,c):
    sum=0
    maxz=max(x,y,z)
    if x==maxz:
        sum=sum+a
    if y == maxz:
        sum = sum + b
    if z == maxz:
        sum = sum + c
    return sum
def cal_everycoty_weight(city):
    city_weight=np.zeros(city_number)
    city_value=np.zeros(city_number)
    for i in range(city_number):
        if city[i]==1:
            city_weight[i]=bag[i-1][1]
            city_value[i]=bag[i-1][0]
        if city[i]==0:
            city_weight[i]=0
            city_value[i]=0
    return city_weight,city_value





if __name__ == '__main__':
    city,w=first(weight_sum,midu,bag)
    draw_city(city_condition,city)
    x=draw_city(city_condition,city)
    edge=max_citycondition(city_condition)
    _,judge,edge_length=judgesearch(city,city_condition,edge)
    city_second=add_two(judge[-2:],city_condition,city,w,midu)
    for i in  range(len(city_second)):
        city.append(city_second[i])
    w_sum=cal_v_w(city)
    i = 2
    while w_sum<weight_sum*R and i<=2:
        city_third = add_two(judge[-(i+2):-(i)], city_condition, city, w_sum, midu)
        for j in  range(len(city_third)):
             city.append(city_third[j])
        w_sum = cal_v_w(city)
        i=i+2
    city=list(set(city))
    x=draw_city(city_condition,city)
    city_weight,city_value=np.array(cal_everycoty_weight(x))
    np.save("city_weightByiss.npy", city_weight)
    np.save("city_valueByiss.npy", city_value)


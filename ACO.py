
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import random
from tqdm import tqdm
matplotlib.rcParams['font.family'] = 'STSong'
np.set_printoptions(threshold=np.inf)
city_name = []
city_condition = []

#Dataset Path
source=''
#Backpack capacity
weight_sum=19270
#cost coefficient
r=14.47
bag=[]
city_number=51
city_weight=np.load("city_weightByiss.npy")
city_value=np.load("city_valueByiss.npy")
with open(source,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    lines = lines[10:61]
    for line in lines:
        line = line.split()
        city_name.append(line[0])
        city_condition.append([float(line[1]), float(line[2])])
city_condition = np.array(city_condition)
with open(source, "r") as lines:
    lines = lines.readlines()
    lines = lines[62:113]
    for line in lines:
        xy = line.split()
        bag.append([float(xy[1]), float(xy[2])])
city_count = len(city_name)
Distance = np.zeros((city_count, city_count))
for i in range(city_count):
    for j in range(city_count):
        if i != j:
            Distance[i][j] = math.sqrt((city_condition[i][0] - city_condition[j][0]) ** 2 + (city_condition[i][1] - city_condition[j][1]) ** 2)
        else:
            Distance[i][j] = 100000
def cal_z(route,distance):
    z=[]
    for j in range(AntCount):
        w = 0
        v = 0
        time = 0
        for i in range(city_number):
            if int(route[j][i]) in item:
                w=w+city_weight[int(route[j][i])]
                v=v+city_value[int(route[j][i])]
            s = (-0.9 / weight_sum) * w + 1
            time=time+distance[int(route[j][i])][int(route[j][i+1])]/s
        z.append(v-r*time)
    return z
def min_max(ant_z):
    ant_z_min=ant_z.copy()
    for i in range(AntCount):
        ant_z[i]=(ant_z_min[i]-np.min(ant_z_min))/10000
    return ant_z
AntCount = 50
city_count = len(city_name)
# 信息素
alpha = 1
beta = 5
rho = 0.9
iter = 0
MAX_iter = 300
Q = 1
pheromonetable = np.ones((city_count, city_count))
candidate = np.zeros((AntCount, city_count)).astype(int)

path_best = np.zeros((MAX_iter, city_count))

distance_best = np.zeros( MAX_iter)
etable = 1.0 / Distance
etable2=np.ones([city_count,city_count])
item=[]
city_2=[]
length=0
for p in range(city_number):
    if city_weight[p]!=0:
        item.append(p)
        length=length+1
k=0
print(item)
city_weight_temp=city_weight.copy()
while k <len(item):
    index=np.where(city_weight_temp==np.max(city_weight_temp))
    city_2.append(index[0][0])
    city_weight_temp[index]=0
    k=k+1
max=-10000
city_1=item.copy()
for i in city_1:
    etable2[:,i]=1
for i in city_2:
        etable2[:, i] = 0.1
for iter in tqdm(range(MAX_iter)):
    if AntCount <= city_count:
        candidate[:, 0] = 0
    else:
        m =AntCount -city_count
        n =2
        candidate[:city_count, 0] = np.random.permutation(range(1))[:]
        while m >city_count:
            candidate[city_count*(n -1):city_count*n, 0] = np.random.permutation(range(1))[:]
            m = m -city_count
            n = n + 1
        candidate[city_count*(n-1):AntCount,0] = np.random.permutation(range(1))[:m]
    length = np.zeros(AntCount)

    for i in range(AntCount):
        unvisit = list(range(city_count))
        visit = candidate[i, 0]
        unvisit.remove(visit)
        for j in range(1, city_count):
            protrans = np.zeros(len(unvisit))
            for k in range(len(unvisit)):
                protrans[k] = np.power(pheromonetable[visit][unvisit[k]], alpha) * np.power(
                    etable[visit][unvisit[k]], beta)*np.power(etable2[visit][unvisit[k]], beta)

            cumsumprobtrans = (protrans / sum(protrans)).cumsum()
            cumsumprobtrans -= np.random.rand()
            try:
                k = unvisit[list(cumsumprobtrans > 0).index(True)]
            except:
                print(protrans)
            candidate[i, j] = k
            unvisit.remove(k)
            length[i] += Distance[visit][k]
            visit = k 
        length[i] += Distance[visit][candidate[i, 0]]
    if iter == 0:
        distance_best[iter] = length.min()
        path_best[iter] = candidate[length.argmin()].copy()
    else:
        if length.min() > distance_best[iter - 1]:
            distance_best[iter] = distance_best[iter - 1]
            path_best[iter] = path_best[iter - 1].copy()
        else:
            distance_best[iter] = length.min()
            path_best[iter] = candidate[length.argmin()].copy()
    changepheromonetable = np.zeros((city_count, city_count))
    x = np.zeros([AntCount, 1])
    route=np.concatenate((candidate,x),1)
    ant_z=cal_z(route,Distance)
    ant_z_pre=ant_z.copy()
    if np.max(ant_z_pre)>max:
        max=np.max(ant_z_pre)
        index=np.where(ant_z_pre==max)
        print(max)
        print(route[index])
        np.save("GACOpath.npy", route[index])
    for i in range(AntCount):
        for j in range(city_count - 1):
            changepheromonetable[candidate[i, j]][candidate[i][j + 1]] += 1/length[i]
        changepheromonetable[candidate[i, j + 1]][candidate[i, 0]] += 1/length[i]
    pheromonetable = (1 - rho) * pheromonetable + changepheromonetable
    iter += 1
print(max)
print("best",path_best[-1])
np.save("path_only-51.npy", path_best[-1])
path=np.array(path_best[-1]+1)
print("after", MAX_iter,"best",distance_best[-1])

fig = plt.figure()
plt.title("Best roadmap")
x = []
y = []
path = []
for i in range(len(path_best[-1])):
    x.append(city_condition[int(path_best[-1][i])][0])
    y.append(city_condition[int(path_best[-1][i])][1])
    path.append(int(path_best[-1][i])+1)
x.append(x[0])
y.append(y[0])
path.append(path[0])
for i in range(len(x)):
    plt.annotate(path[i], xy=(x[i], y[i]), xytext=(x[i] + 0.3, y[i] + 0.3))

plt.plot(x, y,'o-b')
fig = plt.figure()
plt.title("Distance iteration graph")
plt.plot(range(1, len(distance_best) + 1), distance_best)
plt.xlabel("Number of iterations")
plt.ylabel("Distance value")
plt.show()

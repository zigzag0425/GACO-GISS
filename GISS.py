# coding=utf-8
import random
import numpy as np
import math
import pandas as pd
from tqdm import tqdm
#Dataset Path
source=''
city_number=51
n=1
R=1
bag=[]
city_condition=[]
#Backpack capacity
weight_sum=18270
#cost coefficient
r=14.47


M=20
max_inter=1000
pc = 0.65
pm = 0.2
route_2=np.load("route_2opt.npy")
route_2=route_2.tolist()
for i in range(city_number+1):
    route_2[i]=int(route_2[i])
route=route_2
with open(source,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    lines = lines[10:61]
    for line in lines:
        line = line.split()
        city_condition.append([float(line[1]), float(line[2])])
city_condition = np.array(city_condition)
with open(source, "r") as lines:
    lines = lines.readlines()
    lines = lines[62:113+(city_number-1)*(n-1)-1]
    for line in lines:
        xy = line.split()
        bag.append([float(xy[1]), float(xy[2])])
bag=np.array(bag)
city_count = city_number
Distance = np.zeros((city_count, city_count))
for i in range(city_count):
    for j in range(city_count):
        if i != j:
            Distance[i][j] = math.sqrt((city_condition[i][0] - city_condition[j][0]) ** 2 + (city_condition[i][1] - city_condition[j][1]) ** 2)
        else:
            Distance[i][j] = 100000
def init():
    pop=np.zeros([M,city_number-1])
    for i in range(M):
        weight_now=0
        item_chose=np.zeros([city_number-1,n])
        flag=True
        while weight_now<weight_sum and flag:
            city=random.randint(0,city_number-2)
            pop[i][city]=1
            weight_now=weight_now+bag[city][1]
            if weight_now>weight_sum:
                pop[i][city]=0
                flag=False


    return pop

def cal_weight_value(pop):
    weight=np.zeros([pop.shape[0],city_number])
    value=np.zeros([pop.shape[0],city_number])
    for k  in range(pop.shape[0]):
        for i in range(city_number-1):
            if pop[k][i]==1:
              weight[k][i+1]=weight[k][i+1]+bag[i][1]
              value[k][i+1]=value[k][i+1]+bag[i][0]
            else:
               weight[k][i+1]=0
               value[k][i+1]=0
    return weight,value
def cal_fitness(route,weight,value):
    fitness=[]
    for i  in range(weight.shape[0]):
        time=0
        w=0
        v=0
        for j in range(city_number):
            w=w+weight[i][route[j]]
            v=v+value[i][route[j]]
            s = (-0.9 / weight_sum) * w + 1
            time = time + Distance[route[j]][route[j+1]] / s
        z=v-r*time
        fitness.append(z)
    return fitness
def choose(pop,fitness):
    pop_chosed=np.zeros([pop.shape[0],city_number-1])
    for i in range(pop.shape[0]):
        x=random.randint(0,M-1)
        y=random.randint(0,M-1)
        if x==y:
            x = random.randint(0, M-1)
            y = random.randint(0, M-1)
        if fitness[x]>=fitness[y]:
            pop_chosed[i]=pop[x]
        else:
            pop_chosed[i]=pop[y]

    return pop_chosed
def croseeover(pop_1,pop_2):
    pop_child=np.zeros([M,city_number-1])
    for i in range(M):
        parent_1=pop_1[i]
        parent_2=pop_2[i]
        child = np.zeros([city_number-1])
        if random.random() >= pc:
            child = parent_1.copy()
        else:
            start_pos = random.randint(0, parent_1.shape[0] - 1)
            end_pos = random.randint(0, parent_1.shape[0] - 1)
            if start_pos > end_pos:
                tem_pop = start_pos
                start_pos = end_pos
                end_pos = tem_pop
            child[start_pos:end_pos + 1][:] = parent_1[start_pos:end_pos + 1][:].copy()
            child[0:start_pos][:]=parent_2[0:start_pos][:]
            child[end_pos+1:city_number-1][:]= parent_2[end_pos+1:city_number-1][:]
            child_weight=np.expand_dims(child,0)
            weight_dim,_=cal_weight_value(child_weight)
            weight_dim=np.array(weight_dim)
            if np.sum(weight_dim)>weight_sum:
                child=parent_1.copy()
        pop_child[i]=child
    return pop_child

def mutate(pops):
    pops_mutate=np.zeros([M,city_number-1])
    for i in range(len(pops)):
        pop=pops[i].copy()
        t = random.randint(1, 5)
        count = 0
        while count < t:
            pop_temp=pop.copy()
            if random.random() < pm:
                mut_pos1 = random.randint(0, pop.shape[0] - 1)
                mut_pos2 = random.randint(0, pop.shape[0] - 1)
                if mut_pos1 != mut_pos2:
                    tem = pop[mut_pos1]
                    pop[mut_pos1] = pop[mut_pos2]
                    pop[mut_pos2] = tem
            pop_cal=np.expand_dims(pop,0)
            weight_pop,_=cal_weight_value(pop_cal)
            if np.sum(weight_pop)>weight_sum:
                     pop=pop_temp
            count += 1
        pops_mutate[i] = pop
    return  pops_mutate






x=[]
if __name__ == '__main__':
   pop=init()
   i=0
   global_max=-10000
   global_item=pop[0]
   for i in tqdm(range(max_inter)):
       weight,value=cal_weight_value(pop)
       fitness=cal_fitness(route,weight,value)
       max=np.max(fitness)
       if(i%50==0):
           x.append(np.max(fitness))
       index=np.where(fitness==max)
       if max >global_max:
           global_item=pop[index]
           print(max)
           np.save("../city_weight-kp.npy", weight[index])
           np.save("../city_value-kp.npy", value[index])
           global_max=max
       fitness=cal_fitness(route,weight,value)
       pop_1=choose(pop,fitness)
       pop_2 = choose(pop, fitness)
       pop_child=croseeover(pop_1,pop_2)
       pop_mutate=mutate(pop_child)
       weight_new, value_new = cal_weight_value(pop_mutate)
       fitness_new = cal_fitness(route, weight_new, value_new)
       for j in range(M):
           if fitness_new[j]>=fitness[j] :
               pop[j]=pop_mutate[j]
   x=np.array(x)



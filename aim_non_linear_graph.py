#!/usr/bin/env python
# coding: utf-8

# In[4]:

import numpy as np
import random
import time
import pandas as pd
import csv

np.random.seed(0)

#...
# ?????????
#...

list_temps = [];
list_probs = [];

def del_cycle_(p1,t1,p2,t2): #p2 и t2 параметры петли     
    return [p1/(1-p2),t1 + ((t2 * p2)/(1-p2))] #[new_prob,new_temp]

def del_node_(p1,t1,p2, t2):
    return [p1*p2, t1+t2] 

def parallel_temps(l=0): # рекурсивная функция, t2,p2 
    #print(l,list_temps)
    t1 = list_temps[l]
    p1 = list_probs[l]
    
    if l+1 == len(list_probs)-1: 
        t2 = list_temps[l+1]
        p2 = list_probs[l+1] 
     
        return [p1+p2,((t1*p1) + (t2 * p2))/(p1 + p2)] #Если дошли до конца, завершаем рекурсию и возвращаем результат.
    else:
        p2,t2 = parallel_temps(l+1)

        return [p1+p2,((t1*p1) + (t2 * p2))/(p1 + p2)] #возвращаем результат вызывающей функции для ее соотв. t2
    
def del_parallel_edges_(x,y):
    global list_temps 
    global list_probs 
    
    list_temps = curr_temp_matrix[x][y]
    list_probs = curr_prob_matrix[x][y]
    
    return parallel_temps()
    
#...
# ?????????
#...


# In[15]:
#Функция пробегается по диагонали и проверяет о наличии петлей.
#При их наличии, петли должны удаляться; 

def check_for_cycles_():
    for i in range(0,len(curr_prob_matrix)-1): 
        if curr_prob_matrix[i][i] == 1.0:
            continue

        ind = None
        
        #Удаляем петлю
        for l in range(len(ind)):
            curr_prob_matrix[i][ind[l]],curr_temp_matrix[i][ind[l]] = del_cycle_(
                curr_prob_matrix[i][ind[l]],
                curr_temp_matrix[i][ind[l]],
                curr_prob_matrix[i][i],
                curr_temp_matrix[i][i]) 
        
        curr_prob_matrix[i][i] = 0.0  
        curr_temp_matrix[i][i] = 0    


#...
# ?????????
#...

matrix_prob = [ #0   #1   #2    #3   #4   #5   #6   #7   #8   #9   #10   
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #0
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #1
                [0.0, 0.0, 0.0, 0.95, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0],#2
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #3
                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], #4
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], #5
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], #6
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], #7
                [0.0, 0.15, 0.0, 0.85, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #8
                [0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95], #9
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], #10
              ]

temp_matrix = [ #0 #1 #2 #3 #4 #5 #6 #7 #8 #9 #10
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
                [0, 0, 3.4902, 0, 0, 0, 0, 0, 0, 0, 0], #1
                [0, 0, 0, 1.339, 0, 0, 1.275, 0, 0, 0, 0], #2
                [0, 0, 0, 0, 3.08, 0, 0, 0, 0, 0, 0], #3
                [0, 0, 0, 0, 0, 2.93, 0, 0, 0, 0, 0], #4
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2.72, 0], #5
                [0, 0, 0, 0, 0, 0, 0, 6.88, 0, 0, 0], #6
                [0, 0, 0, 0, 0, 0, 0, 0, 4.73, 0, 0], #7
                [0, 1.47, 0, 2.298, 0, 0, 0, 0, 0, 0, 0], #8
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], #9
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #10
              ]



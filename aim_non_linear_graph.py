
# Программное обеспечение для оценки статистических характеристик временного профиля линейных и нелинейных планов 
# действий интеллектуальных сервис-ориентированных систем

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


def solve_matrix():
    check_for_cycles_()

    cycles_ = []
    par_edges = []

    while len(curr_prob_matrix) > 2:    

        i = np.random.randint(1,len(curr_prob_matrix)-1) #выбираем вершину для удаления

        for j in range(len(curr_prob_matrix[i])):

            if curr_prob_matrix[i][j] <= 0.0: #пропускаем цикл, поскольку наличие нуля означает 
                continue                      #отсутствие какого либо перехода

            for k in range(len(curr_prob_matrix[i])): # K индексы по столбцу, J индексы по строке
                if (k == i) or (j == i): #k - это строки, по столбцу i (i также является строкой. Мы удаляем элементы [i,i])
                    continue

                if (isinstance(curr_prob_matrix[k][j], float) 
                    and curr_prob_matrix[k][i] > 0.0 
                    and curr_prob_matrix[i][j] > 0.0): #Надо проверять, что перемножаемые значения больше 0.0
                                                       #из-за этого вылетала ошибка

                    prob_ki_ij = curr_prob_matrix[k][i] * curr_prob_matrix[i][j] #сокращаем последовательность вероятностей
                    temp_ki_ij = curr_temp_matrix[k][i] + curr_temp_matrix[i][j] #сокращаем временную последовательность

                    if curr_prob_matrix[k][j] == 0.0: #если элемент равен нулю, то просто присваиваем ему новое значение
                        #print(f"k={k} и j={j} если k-j = 0.0 \n")

                        curr_prob_matrix[k][j],curr_temp_matrix[k][j] = [ #в python не переносить переменные на след. строку
                            prob_ki_ij,temp_ki_ij                         #при присвоении им значения... !!!
                        ]
                    elif curr_prob_matrix[k][j] > 0.0: #если элемент больше нуля, то создаем массив
                        curr_prob_matrix[k][j],curr_temp_matrix[k][j] = [
                            [curr_prob_matrix[k][j],prob_ki_ij],
                            [curr_temp_matrix[k][j],temp_ki_ij]
                        ]

                elif isinstance(curr_prob_matrix[k][j], list): #если объект - список... 
                    #print("Прибавляет новые значения в список... \n")
                    curr_prob_matrix[k][j].append(curr_prob_matrix[k][i] * curr_prob_matrix[i][j])  
                    curr_temp_matrix[k][j].append(curr_temp_matrix[k][i] + curr_temp_matrix[i][j])

                #x,y = define_coords(k,j,i) #определяем координаты

                if k == j:
                    x,y = define_coords(k,j,i)
                    cycles_.append(x) #координаты петель
                elif k != j and isinstance(curr_prob_matrix[k][j], list): 
                    par_edges.append(define_coords(k,j,i)) #координаты параллельных (сразу вызываем функцию)
                    #print(f"Параллельные дуги {par_edges}\n")

        #Удаляем сначала столбец...

        #print("\n--------->")
        #print(f"Is deleted the state {i}")

        for l in range(len(curr_prob_matrix)):
            curr_prob_matrix[l].pop(i)
            curr_temp_matrix[l].pop(i)

        #...затем строку
        curr_prob_matrix.pop(i)
        curr_temp_matrix.pop(i)

        #print("До сюда дошло...")

        #Удаляем параллельные дуги...
        if len(par_edges) > 0:
            for l in range(len(par_edges)):
                new_p,new_t = del_parallel_edges_(par_edges[l][0],par_edges[l][1]) 
                curr_prob_matrix[par_edges[l][0]][par_edges[l][1]] = new_p
                curr_temp_matrix[par_edges[l][0]][par_edges[l][1]] = new_t

        par_edges = []

        #Проверяем о наличии петель... 
        check_for_cycles_() #удаляем все петли

        #show_matrix() # показываем упрощенный вариант матрицы n степени.

        
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

curr_prob_matrix = matrix_prob
curr_temp_matrix = temp_matrix

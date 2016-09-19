
# coding: utf-8

# In[135]:

import numpy as np 
from itertools import combinations
import random
import os.path
import collections
# In[136]:

sudoku = [8,3,4,1,7,5,9,2,6,1,6,2,3,9,4,7,8,5,7,9,5,6,2,8,4,3,1,2,7,6,5,4,9,8,1,3,3,1,8,7,6,2,5,4,9,4,5,9,8,1,3,2,6,7,5,4,1,9,8,6,3,7,2,6,8,3,2,5,7,1,9,4,9,2,7,4,3,1,6,5,8] 


# In[137]:

sudoku1 = map(int,list("123456789578139624496872153952381467641297835387564291719623548864915372235748916"))


# In[138]:

#reading sudoku from file
def readSudokus(filename):
    with open(filename) as f:
        content = f.readlines()
    f.close()
    # print type(content)
    Sudoku = []
    for i in content:
#         try:
        Sudoku.append(map(int,list(i[:-1])))
#         except ValueError:
#             pass
#             print i
    return Sudoku


# In[139]:
k=0
def verify(cage_list):
    com_list = []
    for cage in cage_list:
#         print cage.choice,cage.size(),cage.sum(),cage.cells
        com_list += cage.cells
#     print len(com_list),len(Scells)
    if set(com_list) != set(Scells):
#         print False
        k += 1
#     print com_list
#     print [item for item, count in collections.Counter(com_list).items() if count > 1]


# In[148]:

def get_neighbours(a,values_list):
    cell = a
#     print cell
    neighbours = []
    if (cell[0],cell[1]+1) in not_included:
        if cells[(cell[0],cell[1]+1)] in values_list:
            neighbours.append((cell[0],cell[1]+1))
    if (cell[0],cell[1]-1) in not_included:
        if cells[(cell[0],cell[1]-1)] in values_list:
            neighbours.append((cell[0],cell[1]-1))
    if (cell[0]+1,cell[1]) in not_included:
        if cells[(cell[0]+1,cell[1])] in values_list:
            neighbours.append((cell[0]+1,cell[1]))
    if (cell[0]-1,cell[1]) in not_included:
        if cells[(cell[0]-1,cell[1])] in values_list:
            neighbours.append((cell[0]-1,cell[1]))
    if neighbours == []:
        return "no neighbours" #TODO: None
    return neighbours


def create_cage(a,cage_choice,cage_list,max_cage_choice):
    req_cage = cage_list[-1]
    values_list = [i for i in range(1,10)]
    for i in range(cage_choice-1):
        neighbours = get_neighbours(a,values_list)
        if neighbours == "no neighbours": #TODO: None
#             print "Steps to prevent stil to do",a #then merge or split the adjacent cage
            if req_cage.size()==1:
                for i in cage_list[:-1]:
    #                 print i.cells
                    n = [(a[0],a[1]-1),(a[0],a[1]+1),(a[0]+1,a[1]),(a[0]-1,a[1])]
                    random.shuffle(n)
                    for j in n:
                        if j in i.cells:
                            if cells[j] in values_list and i.size()<max_cage_choice:
#                                 print j
#                                 not_included.remove(cells[a])
                                i.join(a)
                                cage_list.remove(req_cage)
                                return "done"
                                #TODO
            else:
                return "size reduced"
#         elif neighbours == "done":
            
#             return True #to be figured out
        else:
            choosen_neighbour = random.choice(neighbours)
#             print choosen_neighbour, values_list
            values_list.remove(cells[choosen_neighbour])
            not_included.remove(choosen_neighbour)
            req_cage.join(choosen_neighbour)
            a=choosen_neighbour


# In[149]:

class cage:
    def __init__(self,choice,cell):
        self.choice = choice
        self.cells = [cell]
        self.values = []
    def join(self,cell):
        self.cells.append(cell)
    def size(self):
        return len(self.cells)
    def sum(self):
        return sum([cells[i] for i  in self.cells])
    
def generateKillerSudoku(sudoku,index,max_cage_choice):
    Scells = []
    for i in range(9):
        for j in range(9):
                Scells.append((i,j))

    cells = dict((Scells[i], sudoku[i]) for i in range(len(Scells)))
    cage_list = []
    not_included = Scells[:]
    random.shuffle(not_included)
    i = 0 
    c_index=0
    # cells = dict((key, [key,]) for key in Scells)
    # print not_included
    while not_included != []:
    #     print "once"
        for a in not_included:
    #         print "a=",a
            not_included.remove(a)
            if c_index<5:    # reduce  c_index if you want less unit cages
                x = cage(max_cage_choice,a)
                cage_list.append(x)
                create_cage(a,max_cage_choice,cage_list,max_cage_choice)
                c_index += 1
                continue
            cage_choice = random.choice(range(2,max_cage_choice+1))
            x = cage(cage_choice,a)
            cage_list.append(x)
            create_cage(a,cage_choice,cage_list,max_cage_choice)
        random.shuffle(not_included)
    verify(cage_list)
#     print not_included
    save_path = "F:/UvA/KRProject_1/"+ str(max_cage_choice)+str('/') 
#     save_path = ''
    out = str(index)+".killer"
    output_filename = os.path.join(save_path,out)
    f1 = open(output_filename,'w')
    for cage1 in cage_list:
            outputString = ''
            outputString = str(cage1.sum())+"="
            listString =''
            for item in cage1.cells:
                listString += str(item)+'+'
            outputString += listString[:-1]+'\n'
#             print outputString
            f1.write(outputString)
    f1.close()

def outputKillerSudoku(filename,max_cage_choice):
    Sudokus = readSudokus(filename)
    killerSudokus = []
    index = 0
    for s in Sudokus:
        generateKillerSudoku(s,index,max_cage_choice)
        index += 1

# save_path = 'F:\UvA\KRProject_1'
for i in [2,3,4,5,6,7,8,9]:
    outputKillerSudoku("Sudokus.txt",i)
# generateKillerSudoku(sudoku,1,3)
# outputKillerSudoku("Sudokus.txt",2)


# In[126]:

# import collections
# com_list = []
# for cage in cage_list:
# #     print [item for item, count in collections.Counter(cage.cells).items() if count > 1]
#     print cage.choice,cage.size(),cage.sum(),cage.cells
# #     if cage.size()>1:
# #         com_list += cage.cells
# # if set(com_list) == set(Scells):
# #      print True
# # print len(com_list),len(Scells)
# # print com_list
# # print [item for item, count in collections.Counter(com_list).items() if count > 1]


# In[27]:

# print not_included,len(not_included)


# In[17]:

# j=0
# temp = []
# for i in sudoku:
#     j+=1
#     temp.append(i)
#     if j == 9:
#         print temp
#         temp=[]
#         j=0


# In[81]:

# range(2,6)


# In[147]:

# print k


# In[ ]:




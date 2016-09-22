#Robert White 
#Supervisor Dr. Konstantin Korovin
#http://pythonsudoku.sourceforge.net/
#Oct 2013
import os, sys
import pyparsing as pp
import numpy
import time
import pycosat
from itertools import combinations, ifilter, chain

# some global values:
seed = 10000
indexBoard = []

countCNF_ari = 0
countCNF_all = 0

def getNewIndex():
    global seed
    seed = seed + 1
    return seed


# note that the k is a number from 1 to 9
def getIndex(i,j,k):
    return (i * 81 + j * 9 + k)

# note that the k is a number from 1 to 9
def deIndex (index):
    i = (index-1) / 81
    j = ((index -1)/ 9) % 9
    k = (index-1) % 9 +1 
    return (i, j, k)  # k is 1 - 9


def decode_to_matrix(result_list):
    out_matrix = numpy.zeros(shape = (9,9))
    for l in result_list:
        if l > 0 and l < 10000:
            #print l ,'means', (l-1)/81,((l-1)/9)%9,' is ', (l-1)%9 +1 
            (i,j,k) = deIndex(l)
            out_matrix[i][j] = k
        # elif l > 10000:
            # print l

    return out_matrix
            
def print_matrix(matrix):
    line = 1
    for row in matrix:
        for ele in row:
            print int(ele), 
        line = line + 1
        print '\n'
       

            
def write_to_cnf_file(cnf, name): # out is the writting channel
    out = open(name, 'w+')
    
    for clause in cnf:
        for literal in clause:
            out.write(str(literal)+' ')
    out.write('\n')
    out.close() 


def remove_cell_values(i, j, v):
    if v in cellPossibleValues[i][j]:
        cellPossibleValues[i][j].remove (v)

def add_cell_values(i, j, v):
    if not (v in cellPossibleValues[i][j]):
            cellPossibleValues[i][j].append(v)

def exactly_one(literals):
    # print 'exactly one of ', literals
    new = []
    cnf = []
    previous= None
    if len(literals) == 1:
        cnf.append([literals[0]])
    elif len(literals) == 2:
        # cnf.append([literals[0], literals[1]])
        cnf.append([literals[0] * -1, literals[1] * -1])
    else:
        for x in literals[:-2]:
            # print 'x is ', x
            y = getNewIndex()
            # print 'y is ', y
            # cnf.append([x, y])
            cnf.append([-1*x, -1*y])
            # print 'x only one y'
            if len(new) != 0:
                # print 'link to the previous x and y'
                cnf.append([x * -1, new[-1]])
                # print [x * -1, new[-1]]
                cnf.append([y * -1, new[-1]])
                # print [y * -1, new[-1]]
            new.append(y)
            previous = x
        # cnf.append([literals[-1], literals[-2]])
        cnf.append([-1*literals[-1], -1*literals[-2]])
        cnf.append([-1*literals[-1], new[-1]])
        cnf.append([-1*literals[-2], new[-1]])
    cnf.append(literals)
    return cnf


def encode_to_cnf(killerRules): #encode a problem (stored in matrix) as cnf
    global indexBoard
    global countCNF_all
    global countCNF_ari
    for i in range (0, 9):
        tmp = []
        for j in range (0, 9):
            tmp2 = []
            for num in range (1, 10): # here, it represent num of 1 to 9
                tmp2.append(getIndex(i, j, num))
            tmp.append(tmp2)
        indexBoard.append(tmp)

    cnf = []
    
    # find all possible combination of each cell
    for k in killerRules:
        cageSum = k[0]
        cageSize = len(k[1])
        cageCells = k[1]
        cb = combinations([1,2,3,4,5,6,7,8,9], cageSize)
        f = lambda x : sum(x) == cageSum
        comb = ifilter(f, cb) # all valid combinations
        allPossible = list(chain(comb))
        # print '\nall possible: ', allPossible
        common = []
        for i in range (1,10):
            flag = True # means it is a common one
            for j in allPossible:
                # print 'test on', list(j)
                if not(i in list(j)):
                    # print i, ' is not in ', list(j) 
                    flag = False
            if flag == True:
                # print '************this is a common one: ', i
                common.append(i)

        different = []
        for p in allPossible:
            pl = list(p)
            for r in common:
                if r in pl:
                    pl.remove(r)
            if (pl != []):
                different.append(pl)

        # print 'In this iteration, we have the sum of cage: ', cageSum, '; the size of cage', cageSize
        # print 'these cells are: ', cageCells
        # print 'possible combinations are: ', allPossible
        # print 'common values, ' , common
        # print 'different values', different

        # next we start to encode. 

        # encode the common values first. 
        # for every common value, [1,2] for example, introduce a new index representing the existence of the value
        # among the cells of the cage. 

        dic = {}
        for num in range(1, 10): 
            dic[num] = getNewIndex()
            tmp =[]
            for cc in cageCells:
                cnf.append([indexBoard[cc[0]][cc[1]][num-1] * -1,  dic[num]]) # right arrow
                tmp.append(indexBoard[cc[0]][cc[1]][num-1])                # left arrow
            tmp.append(dic[num] * -1)
            cnf.append(tmp)
        for num in common:
            # print num, '  is a common number'
            cnf.append([dic[num]])

        # next, we encode the differnt ones 
        # we need to introduce new values as above
        # we need to obtain all the numbers possibly in the different cases
        # lst = reduce ((lambda x, y: x + y), different)
        # lst = list(set(lst)) # remove duplicated elements

        x_list = []
        for dif in different: # for example, [[3,4,8], [3,5,7], [4,5,6]
            # for cc in cageCells:
            # we need to convert from DNF to CNF
            # first, we need to convert that x1 = 3 /\ 4 /\ 8
            # again, we need to introduce our x1, for 348, x2 for 357 , etc
            x = getNewIndex()
            # x -> 3 4 8
            for d in dif:
                cnf.append([-1* x , dic[d]])
                # print ' for ', d, ' -- ', dic[d]
            # ~(3, 4, 8) \/ x
            # i.e. -3 \/ -4 \/ -8 \/ x
            tmp = map ((lambda x : -1 * dic[x]), dif)
            tmp.append(x)  
            # print ' == ', tmp 
            cnf.append(tmp)
            x_list.append(x)
        if x_list != []:
            # print '***************', x_list
            cnf.append(x_list)
    # END of killer sudoku ------------------------
    countCNF_ari = len(cnf)

    # Exactly one in each cell
    for i in range(9): #column
        for j in range(9): #row
            # print 'for cell ', i ,' and ', j, '\n'
            #at least one of k should be true
            temp =[]
            for k in range(1,10):
                temp.append(getIndex(i,j,k))
            cnf = cnf + exactly_one(temp)
            
    #exactly once in each row     
    for k in range(1,10): #each number
        # appear exactly once in each row
        for j in range(9):
            #appear at least once
            #print 'In row ', j, ' \n'
            temp = []
            for i in range(9):
                temp.append(getIndex(i,j,k))
            cnf = cnf + exactly_one(temp)
            
        #exactly once in each coloumn
        for i in range(9):
            temp = []
            for j in range(9):
                temp.append(getIndex(i,j,k))
            cnf = cnf + exactly_one(temp)
        #exactly once in each block
        for block_i in range(3):
            for block_j in range(3):
                #print 'for block', block_i, ' and ', block_j, '::::\n'
                #at least once
                temp  = []
                for i in range(block_i*3, block_i*3 + 3):
                    for j in range(block_j*3, block_j*3 + 3):
                        temp.append(getIndex(i,j,k))
                cnf = cnf + exactly_one(temp)
    countCNF_all = len(cnf)
    return cnf

                
def readSudoku(filename):
    # print 'the constraints from file ', filename, ' are:'
    file_reader = open(filename, 'r')
    lines = file_reader.readlines()
    killerRules = []
    f = lambda x: [int(x[1]), int(x[4])] 

    for l in lines:
        # print l
        (s, t) = l.split('=')
        tl = t.split('+')
        lst = map(f, tl)
        killerRules.append((int(s), lst))
    return killerRules

def verify_killer_sudoku(killerRules, result_matrix):
    # print 'start checking the answer!'
    for r in killerRules:
        ans = r[0]
        cage = r[1]
        cageSum = 0
        for c in cage:
            cageSum = cageSum + result_matrix[c[0]][c[1]]
        if cageSum != ans:
            # print 'the rule is not validated: ', r
            return False
    return True


def main ():


    killerRules = readSudoku(sys.argv[1])
    
    cnf =  encode_to_cnf(killerRules)       
    # #solve the encoded CNF     
    start = time.time()
    result_list = pycosat.solve(cnf)
    end = time.time()
    #output the result
    # print result_list
    if result_list == 'UNSAT':
        print 'UNSAT'
    elif result_list !=[]:
        # print '\n\nFor a this killer sudoku, ',
        # print_matrix(matrix)
        result_matrix = decode_to_matrix(result_list)
        # uncomment these two lines if you want to print the sudoku 
        # print 'one of the solutions found is\n'
        # print_matrix(result_matrix)

        if (verify_killer_sudoku(killerRules, result_matrix)):
            # print 'yes, it is a valid answer!'
            print 'CORRECT %04.5f %d %d'% ((end-start), countCNF_ari, countCNF_all)
        else:
            print 'ERROR'
            # print 'no, it is not a valid answer'
    else:
        print 'SYSTEM ERROR'
              
if __name__ == '__main__':
    main()
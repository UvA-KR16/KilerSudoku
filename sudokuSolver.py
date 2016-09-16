#Robert White 
#Supervisor Dr. Konstantin Korovin
#http://pythonsudoku.sourceforge.net/
#Oct 2013
import os, sys
import pyparsing as pp
import numpy
import pycosat


def code(i,j,k):
    return (i * 81 + j * 9 + k +1)

def decode_to_matrix(result_list):
    out_matrix = numpy.zeros(shape = (9,9))
    for l in result_list:
        if l > 0:
            #print l ,'means', (l-1)/81,((l-1)/9)%9,' is ', (l-1)%9 +1 
            out_matrix[(l-1)/81][((l-1)/9)%9] = (l-1)%9 +1
            
    return out_matrix
            
def print_matrix(matrix):
    line = 1
    for row in matrix:
        for ele in row:
            print int(ele), 
        line = line + 1
        print '\n'
       
'''
def count_matrix(m):
    count = 0
    for i in range(9):
        for j in range(9):
            if m[i][j] != 0:
                count = count +1
    return count
'''
            
def write_to_cnf_file(cnf, name): # out is the writting channel
    out = open(name + '.cnf' , 'w+')
    out.write("c created by Robert for iLogic course and final year project. \nc Supervisor: Dr. Konstantin Korovin")
    #out.write() we can forget about the number of clauses and number of variables although it is good to know.
    #print "data is", repr(cnf)
    
    for clause in cnf:
        #print 'A Clause is: ', clause
        for literal in clause:
            #print literal
            out.write(str(literal)+' ')
    out.write('\n')
    out.close() 

def read_as_matrix(name):
    input = open(name, "r")
    lines = input.readlines()
    #matrix =  numpy.zeros(shape = (9,9))
    matrix = []
    word = pp.Word(pp.alphanums)
    rest = pp.OneOrMore(word)
    for l in lines:
        nums = map(int, rest.parseString(l))
        matrix.append(nums)
           
    #print count_matrix(matrix) # use this matrix to produce CNF file
    input.close()
    return matrix

def encode_to_cnf(matrix): #encode a problem (stored in matrix) as cnf
    cnf = []
    # Exactly one in each cell
    for i in range(9): #column
        for j in range(9): #row
            # print 'for cell ', i ,' and ', j, '\n'
            #at least one of k should be true
            temp =[]
            for k in range(9):
                temp.append(code(i,j,k))
                #output.write(str(code(i,j,k)) + ' ') 
            cnf.append(temp)
            #print 'not two numbers at the same time \n'
            #no more than one will be true
            for k in range(9):
                for k2 in range (k+1, 9):
                    cnf.append([-1*code(i,j,k), -1*code(i,j,k2)])
                    #output.write('-'+str(code(i,j,k))+' -'+str(code(i,j, k2)) + ' 0\n') 
                    #print '\t (', k , ' and ', k2, 'are not the true at the same time for ', i, j , '\n'
            
    #exactly once in each row     
    for k in range(9): #each number
        # appear exactly once in each row
        for j in range(9):
            #appear at least once
            #print 'In row ', j, ' \n'
            temp = []
            for i in range(9):
                temp.append(code(i,j,k))
                #output.write(str(code(i,j,k)) + ' ')
            #output.write('0\n')
            cnf.append(temp)
            #no more than once
            for i in range(9):
                for i2 in range(i+1, 9):
                    cnf.append([-1*code(i,j,k), -1*code(i2,j,k)])
                    #output.write('-'+ str(code(i,j,k)) + ' -'+ str(code(i2,j,k)) + ' 0\n')
                    #print '\t for a number, row', i , ' and ', i2 ,' can not be true at the same time'      
            
        #exactly once in each coloumn
        for i in range(9):
            temp = []
            for j in range(9):
                temp.append(code(i,j,k))
                #output.write(str(code(i,j,k)) + ' ')
            #output.write('0\n')
            cnf.append(temp)
            #no more than once
            for j in range(9):
                for j2 in range( j +1, 9):
                    #output.write('-'+ str(code(i,j,k)) + ' -'+ str(code(i,j2,k)) + ' 0\n')
                    cnf.append([-1*code(i,j,k), -1*code(i,j2,k)])
                    
        #exactly once in each block
        for block_i in range(3):
            for block_j in range(3):
                #print 'for block', block_i, ' and ', block_j, '::::\n'
                #at least onece
                temp  = []
                for i in range(block_i*3, block_i*3 + 3):
                    for j in range(block_j*3, block_j*3 + 3):
                        temp.append(code(i,j,k))
                        #output.write(str(code(i,j,k)) + ' ')
                #output.write('0\n')
                cnf.append(temp)
                #no more than once
                for index1 in range(0,9):
                    for index2 in range(index1+1, 9):
                        #output.write('-'+str(code(index1%3+(block_i*3), index1/3+(block_j*3),k))+' -'
                        #             + str(code(index2%3+(block_i*3), index2/3+(block_j*3),k))+' 0\n')
                        cnf.append([-1*(code(index1%3+(block_i*3), index1/3+(block_j*3),k)), 
                                    -1*code(index2%3+(block_i*3), index2/3+(block_j*3),k)])#
                
    '''               
    #some numbers are prefilled
    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                #print i, j, matrix[i][j], code(i,j, matrix[i][j])
                #output.write(str(code(i,j, matrix[i][j])) + ' 0\n')
                cnf.append([code(i,j,matrix[i][j])])
    '''
    return cnf


                
def main ():
    
    #encode the Sudoku problem to a CNF
    matrix = read_as_matrix(sys.argv[1])
    
    cnf =  encode_to_cnf(matrix)             
    write_to_cnf_file(cnf, sys.argv[1]+'.cnf')
    
    #solve the encoded CNF     
    result_list = pycosat.solve(cnf)
    
    #output the result
    #print result_list
    
    if result_list !=[]:
        
        print 'For a Sudoku problem like this:\n'
        print_matrix(matrix)
        
        result_matrix = decode_to_matrix(result_list)
        print 'One of the solution is\n'
        print_matrix(result_matrix)
    else:
        print 'There is no solution for such a Sudoku'
              
if __name__ == '__main__':
    main()
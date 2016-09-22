#!/usr/bin/env python

import os
import subprocess
import time
import sys
# import subprocess
import commands


def basename(filename):
  return os.path.splitext(os.path.basename(filename))[0]

solver = sys.argv[1]
sudokuDir = sys.argv[2]
amount = int(sys.argv[3])

print 'the solver is: ', sys.argv[0]
# print '1 ', sys.argv[1]
# print '2 ', sys.argv[2]
# print '3 ', sys.argv[3]

# Maximum width of the names to display
# width = max(map(len, map(basename, files))) 
# files.sort(key=basename)
for folder in range(2, 10):
  print 'evaluating ', folder
  ptime = 0
  fsize = 0
  solvingTime = 0
  countAri = 0
  countAll = 0
  ct = 0
  for file in range(amount):
    # ct = ct + 1
    # name = basename(filename)
    # size = os.path.getsize(filename)
    # fsize = fsize + size
    start = time.time()
    filename = './' + sudokuDir + '/'+ str(folder) + '/' + str(file) + '.killer'
    # code = subprocess.call(["bash", "-c", "python %s %s" % (solver, filename)])
    com = 'python '+ solver +' '+ filename
    # print com
    (code, result) = commands.getstatusoutput(com)
    end = time.time()
    ptime = ptime + (end - start)
    if code != 0:
      # print("%-*s  %10d  %04.2f" % (width, name, size, end - start))
    # else:
      print result
      print 'fail'
    elif result[0:7] != 'CORRECT':
      print 'error'
      print result 
      # print("%-*s  %10d  FAIL" % (width, name, size))
    else: 
      # print result 
      r = result.split(' ')
      solvingTime = solvingTime + float(r[1])
      countAri = countAri + int(r[2])
      countAll = countAll + int(r[3])
    
  print "total time for cage size %d is = %04.4f, among which, the solving time is %04.4f" % (folder, ptime/amount, solvingTime/amount)
  print 'they have an avg. no. arith clauses of ', countAri/amount, '  and a total of ', countAll/amount
  # print("total art file size = %10d" % (fsize))
  # print("in total %10d files" % ct);
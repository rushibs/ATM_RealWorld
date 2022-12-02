#! usr/bin/python2

import csv


myfilepath = '/home/ai4ce/instructions.csv'

f1 = open(myfilepath, "r")
last_line = f1.readlines()[-1]
print(last_line)

f1.close()
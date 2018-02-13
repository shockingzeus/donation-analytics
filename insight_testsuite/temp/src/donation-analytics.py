#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:29:05 2017

@author: Xiaoqing
"""

import sys
import time
import math
import bisect
import contextlib
import pytest 

# Workflow
# 0. Initialize by create empty donor list and recipient dictionary.
# 1. Load the data in RAM, parse each line to get the relevant data. O(N).
# 2. Determine if the data from the current line is valid.
# 3. Checking if the current donor (Name@Zip) is in our donor list. Yes means repeat donor.
#    If not, add it to the list for future use. O(N).
# 4. If yes in #3, check if its correpondent recipient+year+Zip combination is a "key"
#    in our recipient dictionary. If not, assign a python list of "Transaction_AMT" as its value. O(N).
#    If yes,use the bisect module to sorted-insert the "Transaction_AMT" to the list. O(logN)
# 5. Calculate the length, total amount and percentile of the "Transaction_AMT" list. 
# 6. Output.
#        
        
def isID(CMTD, Other):
    return CMTD!="" and Other==""

def isdate(date):
    if len(date) == 8:
        try:
            year = int(date[4:])
            return year<2019 and year>2014
        except:
            return False
    else:
        return False
       
def iszip(zipcode):
#check if zipcode is valid. Here we simply check whether the first 5 digits is a integer.
#We could build a database and see if the zipcode really exist - probably overkill here.
    if len(zipcode)>=5:
        try:
            int(zipcode[:5])
            return True
        except:
            return False
    else:
        return False
    
def isname(name):
#check if the name is valid. A valid name should have first name and lastname
#separated by ",", and consists of only alphabets.
    if name:        
        try:
            lastname, firstname = name.rsplit(',')
            lastname = lastname.replace(" ","")
            firstname = firstname.replace(" ","")
        except:
            return False
        
        return lastname.isalpha() and firstname.isalpha()
    else:
        return False
    
def isAMT(AMT):
     try:
         float(AMT)
         return True
     except:
         return False
     
def percentile(N, P):
# Nearest rank method for percentile calculation.
    n = max(int(math.ceil(P * len(N))), 1)
    return N[n-1]

def readpercf(percentf):
# read the percentile number from file.
    with open(percentf, "r") as f:
        return int(f.readline().rstrip('\n'))/100


@contextlib.contextmanager            
def timer(msg):
# A timer generator to test the speed of each function. "with timer():..."
    start = time.time()
    yield
    end = time.time()
    print("%s: %.02fms" % (msg, (end-start)*1000))

def main(inputf, percentf, outputf):
    
    donorlist = set()
    recipientDict = {}
    output = ""
    percent = readpercf(percentf)
    
    with open(inputf, "r") as data:        
        for line in data:
            data = line.rstrip('\n').rsplit('|')
            CMTD = data[0]
            Other = data[15]
            Date = data[13]
            Name = data[7].rstrip()
            Zip = data[10]
            AMT = data[14]
            if all([isID(CMTD, Other), isdate(Date), iszip(Zip), isname(Name), isAMT(AMT)]):
                donorID = Name+"@"+Zip[:5]
                recID = "|".join([CMTD, Zip[:5], Date[4:]])
                AMT = math.floor(float(AMT)+0.5)
                    
                if donorID in donorlist:
                    try:   
                        bisect.insort(recipientDict[recID],AMT)                            
                    except:    
                        recipientDict[recID] = [AMT]
                    number = str(len(recipientDict[recID]))
                    total = str(sum(recipientDict[recID]))
                    perc = str(percentile(recipientDict[recID],percent))
                    output+= "|".join([recID, perc, total, number])+"\n"
                else:
                    donorlist.add(donorID)
    with open(outputf, "w") as f:
        f.write(output)
        
if __name__=="__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Xiaoqing
"""

import sys
import time
import math
import contextlib
import datetime        

@contextlib.contextmanager            
def timer(msg):
# A timer generator to test the speed of each function. 
    start = time.time()
    yield
    end = time.time()
    print("%s: %.02fms" % (msg, (end-start)*1000))    

def getdata(line):
# read all data from a line. If there's any error, return None 
    try:
        data = line.rstrip('\n').rsplit('|')
        Other = data[15]
        CMTE = data[0].rstrip()
        if Other != "" or CMTE == "":
            CMTE = None
        year = getyear(data[13].rstrip())
        name = getname(data[7].rstrip())
        zipcode = getzip(data[10].rstrip())
        AMT = getAMT(data[14])
        return CMTE, year, name, zipcode, AMT
    except:
        return None, None, None, None, None

def getyear(date):
#Get the year from date string.
    if len(date) == 8:
        try:
#            time.strptime(date, "%m%d%Y")
            month = date[:2]
            day = date[2:4]
            year = date[4:]
            datetime.datetime(int(year), int(month), int(day))
            return year
        except:
            return None
  
def getzip(zipcode):
# check if zipcode is valid. Here we simply check whether the first 5 digits is a integer.
    if len(zipcode)>=5:
        try:
            int(zipcode[:5])
            return zipcode[:5]
        except:
            return None

    
def getname(name):
# check if the name is valid. This can be very tricky, as there are so many edge cases.
# I kid you not, I know a Chinese Mongolian who writes his name as "A, A".
# Anyway, here we define a valid name string as: has at least a first and a last name separated by a ","
# which consist of only alphabets except for whitespaces and "." (for possible middle name). 
    try:
        name = name.replace(" ","")
        name = name.replace(".","")
        firstname, lastname = name.rsplit(",")
        if firstname.isalpha() and lastname.isalpha():
            return name
    except:
        return None

    
def getAMT(AMTstr):
     try:
         AMT = math.floor(float(AMTstr)+0.5)
         return AMT
     except:
         return None
     
def percentile(N, P):
# Nearest rank method for percentile calculation.
    n = max(int(math.ceil(P * len(N))), 1)
    return N[n-1]

def main(testdata):
    count = 0
    with open(testdata,"r") as f:        
        with timer("parsing data "+testdata):
            for line in f:
                line.rstrip('\n').rsplit('|')
                count+=1
        print("The file has "+str(count)+" lines.\n")
        
    with open(testdata,"r") as f:      
        Dates = [line.rstrip('\n').rsplit('|')[13] for line in f]
        with timer("getyear() "+str(count)+" times"):
            for date in Dates:
                getyear(date)
                
    with open(testdata,"r") as f:      
        Zips = [line.rstrip('\n').rsplit('|')[10] for line in f]
        with timer("getzip() "+str(count)+" times"):
            for zipcode in Zips:
                getzip(zipcode)        
        
    with open(testdata,"r") as f:      
        Names = [line.rstrip('\n').rsplit('|')[7] for line in f]
        with timer("getname() "+str(count)+" times"):
            for name in Names:
                getname(name)   
                
                
    with open(testdata,"r") as f:      
        AMTs =  [line.rstrip('\n').rsplit('|')[14] for line in f]
        with timer("getAMT() "+str(count)+" times"):
            for AMT in AMTs:
                getAMT(AMT)       
            
    with open(testdata,"r") as f:
        with timer("Total time of getdata() on "+testdata):
            for line in f:
                CMTE, year, name, zipcode, AMT = getdata(line)        
        
        

if __name__=="__main__":
    main(str(sys.argv[1]))
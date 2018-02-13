#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Xiaoqing
"""

import sys
import math
import bisect
import datetime

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
# Nearest rank method for percentile calculation. Verified with the examples in Wikipedia.
    n = max(int(math.ceil(P * len(N))), 1)
    return N[n-1]

def readpercf(percentf):
# read the percentile number from file.
    with open(percentf, "r") as f:
        return int(f.readline().rstrip('\n'))/100
            
def main(inputf, percentf, outputf):
    
    donorlist = set()
    recipientDict = {}
    output = ""
    percent = readpercf(percentf)
    
    with open(inputf, "r") as f:        
        for line in f:

            CMTE, year, name, zipcode, AMT = getdata(line)          
            if None in [CMTE, year, name, zipcode, AMT]:
                continue
            
            donorID = name+zipcode
            recID = "|".join([CMTE, zipcode, year])
                    
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
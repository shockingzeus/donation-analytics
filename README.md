# Find Political Donors

A Python 3 script that take a file listing individual campaign contributions for multiple years, determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, `repeat_donors.txt`.

For each recipient, zip code and calendar year, it calculates these three values for contributions coming from repeat donors:

* total dollars received
* total number of contributions received 
* donation amount in a given percentile

## Requires

Python 3
Bisect ,Time, math and Sys Module

## Input and Output

We have two inputs:

1. `percentile.txt`, holds a single value -- the percentile value (1-100) that your program will be asked to calculate.

2. `itcont.txt`, has a line for each campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. The data conform to the data dictionary [as described by the FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

We need to update an output with: 

## Data structure and work flow 

As we supposedly has streaming data, we use a python set to hold the list of donors, uniquely defined by the combination of "name" and "zip code". 

Recipients are uniquely defined by the combination of "CMTE_ID", "year" and "zip code", and we are interested in their correspondent donation amounts from repeat donors. We use a python dictionary, with the keys the recipients, and the values sorted python lists of correspondent donation amounts.  
 
Work flow:

0. Initialize by create empty donor set and recipient dictionary.
1. Load the data in RAM, parse each line to get the relevant data. O(N).
2. Determine if the data from the current line is valid.
3. Checking if the current donor (name and zip code) is in our donor set. Yes means repeat donor. If not, add it to the list for future use. 
4. If yes in #3, check if its correspondent recipient+year+Zip combination is a key in our recipient dictionary. If not, assign a python list with single element "Transaction_AMT" as its value.  If yes,use the bisect module to sorted-insert the "Transaction_AMT" to the list. It therefore maintains a sorted python list.
5. Calculate the length, total amount and percentile of the "Transaction_AMT" list. 
6. Write to the output file.

## Usage

run.sh

## Performance

We use the "Contributions by Individuals" data from 2017-2018 in

https://classic.fec.gov/finance/disclosure/ftpdet.shtml

to run the test.

It currently processes about one million lines in 10 seconds on my Macbook Pro (early 2015): 2.7 GHz Intel Core i5 CPU, 16 GB 1867 MHz DDR3. 

## Note

1. The python default round() function is weird: it round .5 into 0 instead of 1. We have to use math.floor(x+0.5) instead.

2. We have to compromise between accuracy and speed. Addressing all edge cases uses a lot of resource and slows the program down. For instance, to check if the "date" is valid, we can either use the default time.strptime() method or simply see if the last 4 digits of the "date" string can be converted to an integer between 2015 and 2018. The former is certainly more robust but significantly slower for large data set.

I think it is ultimately depends on what people care about more. For this challenge, the majority of edge cases probably arises from typos or missing information, so stringent validation could be overkill. On the other hand, political analysts probably don't care about running time difference in the seconds scale.....

3. For this particular challenge, the number of donations for a recipient is generally not very large. If it is, we should consider replacing the sorted list of donation amounts by something else as python list is slow. Right now it is not necessary.

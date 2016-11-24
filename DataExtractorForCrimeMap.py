# title: data extractor for crime map #
# starting...                         #
# go!                                 #
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pprint import pprint
from collections import defaultdict
import sys
import re
import json

req = Request('https://www.hk01.com/section/%E6%B8%AF%E8%81%9E',
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()

soup = BeautifulSoup(page, 'lxml')

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

print(soup.prettify())

sys.stdout = orig_stdout
f.close()

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listcrime.txt', 'r+') as fc:
    crimelines = [line[:-1] for line in fc]  # for escaping the newline next to the location string

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listlocation.txt', 'r+') as fl:
    localines = [line[:-1] for line in fl]  # for escaping the newline next to the location string

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# //---->loop through the crimelines list, until there's a match

# loop then check the news title and news contents, to see if  A is in B #

s = localines[9]  # get crime from text file.
t = "西環"  # get crime from web
print("s=" + s)  # for debugging
print("t=" + t)  # for debugging
if s == t:  # string matching
    print("s = t")  # if find a match, then find the corresponding location
else:
    print("s != t")  # if s, t don't match at this round, then check the next crime name in the list.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ==
# //---->substring containing:
# ================
# s = "This be a string"
# if s.find("is") == -1:
#     print "No 'is' here!"
# else:
#     print "Found 'is' in the string."
# ================

# //---->inspiration for storing data pairs into database
# ================
# list1 = [1, 2, 3, 4, 5]
# list2 = [10, 20, 30, 40, 50]
# list3 = [100, 200, 300, 400, 500]
# for i, (l1, l2, l3) in enumerate(zip(list1, list2, list3)):
#     print(i, l1, l2, l3)
# ================

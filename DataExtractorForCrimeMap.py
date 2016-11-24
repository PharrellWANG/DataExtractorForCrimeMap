# title: data extractor for crime map #
# starting...                         #
# go!                                 #

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listcrime.txt', 'r+') as fc:
    crimelines = [line[:-1] for line in fc]  # for escaping the newline next to the location string

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listlocation.txt', 'r+') as fl:
    localines = [line[:-1] for line in fl]  # for escaping the newline next to the location string

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# //---->loop through the crimelines list, until there's a match
s = localines[9]  # get crime from text file.
t = "西環"  # get crime from web
print("s=" + s)  # for debugging
print("t=" + t)  # for debugging
if s == t:  # string matching
    print("s = t")  # if find a match, then find the corresponding location
else:
    print("s != t")  # if s, t don't match at this round, then check the next crime name in the list.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

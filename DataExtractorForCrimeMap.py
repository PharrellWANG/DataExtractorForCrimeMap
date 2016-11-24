# data extractor for crime map #

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listcrime.txt', 'r+') as fc:
    crimelines = [line[:-1] for line in fc]
print(type(crimelines))

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listlocation.txt', 'r+') as fl:
    localines = [line[:-1] for line in fl]
print(type(localines))

print(localines[8])
print(localines[5])
print(localines[8] + localines[5])
print(crimelines[50])
print(crimelines[23])
print(crimelines[50] + crimelines[23])
s = localines[9]
print(s)
t="西環"
if s == t:
    print ("equal")
else:
    print ("not equal")
# inspiration for storing data pairs into database
# list1 = [1, 2, 3, 4, 5]
# list2 = [10, 20, 30, 40, 50]
# list3 = [100, 200, 300, 400, 500]
# for i, (l1, l2, l3) in enumerate(zip(list1, list2, list3)):
#     print(i, l1, l2, l3)

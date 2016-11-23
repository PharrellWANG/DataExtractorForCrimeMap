# data extractor for crime map #

f = open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listcrime.txt','r')

for line in f:
    crimelist = f.readlines()

for i, singlecrime in enumerate(crimelist):
    print( i, singlecrime )

# inspiration for storing data pairs into database
list1 = [1, 2, 3, 4, 5]
list2 = [10, 20, 30, 40, 50]
list3 = [100, 200, 300, 400, 500]
for i, (l1, l2, l3) in enumerate(zip(list1, list2, list3)):
    print(i, l1, l2, l3)

f.close()
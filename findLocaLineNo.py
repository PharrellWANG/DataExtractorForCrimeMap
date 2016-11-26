with open('/Users/Pharrell_WANG/PycharmProjects/DataExtractorForCrimeMap/Lib2_ListOfLocation.txt', 'r+') as fl:
    localines = [line[:-1] for line in fl]  # for escaping the newline next to the location string

count = 1
for loc in localines:
    count += 1
    if loc == "山道":
        print("got it: " + str(count))
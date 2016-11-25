# title: data extractor for crime map #
# starting...                         #
# go!                                 #
from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import sys
import geocoder

from datetime import datetime

start = datetime.now()
print("=============================")
print("$----> data extractor starting... #####")

with open('/Users/Pharrell_WANG/PycharmProjects/DataExtractorForCrimeMap/Lib1_ListOfCrime.txt', 'r+') as fc:
    crimelines = [line[:-1] for line in fc]  # for escaping the newline next to the location string
with open('/Users/Pharrell_WANG/PycharmProjects/DataExtractorForCrimeMap/Lib2_ListOfLocation.txt', 'r+') as fl:
    localines = [line[:-1] for line in fl]  # for escaping the newline next to the location string

req = Request('https://www.hk01.com/section/%E6%B8%AF%E8%81%9E',
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()

soup = BeautifulSoup(page, 'lxml')

collection = soup.find_all("div", class_="blog_listing__item")
print()
print("     #1. Number of news found: " + str(len(collection)))

orig_stdout = sys.stdout
f1 = open('dele_TitleUrlPairs.txt', 'w')
sys.stdout = f1

for member in collection:
    title = member.find("h3")
    title = title.string
    ref = member.find('a').get('href')
    # for reading url containing Traditional Chinese words
    refpart2 = ref[20:]
    s = refpart2
    s = urllib.parse.quote(s)
    url = 'http://www.hk01.com/01%s' % (s)

    req2 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page2 = urlopen(req2).read()
    soup2 = BeautifulSoup(page2, 'lxml')  # single page
    # contents = soup2.find_all('p')
    # print(contents)

    for crime in crimelines:
        if crime not in title:
            continue
        else:
            if 3 == 2:  # todo---->  loop the titles in DB, compare to the current title, if duplicated, "continue";else go go go.
                continue
            else:
                for location in localines:
                    if location not in title:
                        contents = soup2.find_all('p')
                        contents = str(contents)
                        if location not in contents:
                            continue
                        else:
                            g = geocoder.google(location)
                            lat = g.latlng[0]
                            lng = g.latlng[1]
                            time_twins = soup2.find_all("div", class_="date")
                            for tag in time_twins:
                                issue_time = tag.text.strip()[34:]
                                break
                            with open("dele_CrimeLocationPairs.txt", "a") as pairs:
                                pairs.write('crime      :' + crime)
                                pairs.write("\n")
                                pairs.write('location   :' + location)
                                pairs.write("\n")
                                pairs.write('issue time :' + issue_time)
                                pairs.write("\n")
                                pairs.write('crime cato :')# + crimecat)
                                pairs.write("\n")
                                pairs.write('latitude   :' + str(lat))
                                pairs.write("\n")
                                pairs.write('longitude  :' + str(lng))
                                pairs.write("\n")
                                pairs.write('title      :' + title)
                                pairs.write("\n")
                                pairs.write('URL        :' + url)
                                pairs.write("\n")
                                pairs.write("\n")
                                pairs.write("\n")
                                pairs.close()
                        break

                    else:  # location in title
                        g = geocoder.google(location)
                        lat = g.latlng[0]
                        lng = g.latlng[1]
                        time_twins = soup2.find_all("div", class_="date")
                        for tag in time_twins:
                            issue_time = tag.text.strip()[34:]
                            break

                        with open("dele_CrimeLocationPairs.txt", "a") as pairs:
                            pairs.write('crime      :' + crime)
                            pairs.write("\n")
                            pairs.write('location   :' + location)
                            pairs.write("\n")
                            pairs.write('issue time :' + issue_time)
                            pairs.write("\n")
                            pairs.write('crime cato :')# + crimecat)
                            pairs.write("\n")
                            pairs.write('latitude   :' + str(lat))
                            pairs.write("\n")
                            pairs.write('longitude  :' + str(lng))
                            pairs.write("\n")
                            pairs.write('title      :' + title)
                            pairs.write("\n")
                            pairs.write('URL        :' + url)
                            pairs.write("\n")
                            pairs.write("\n")
                            pairs.write("\n")
                            pairs.close()
                    break
        break
    print(title)
    print(url)
    print()
sys.stdout = orig_stdout
f1.close()

print("     #2. Time lapsed: " + str(datetime.now() - start))
print()
print("$----> data extractor ending... #####")
print("=============================")

# //--->redirection completed


# ============
# ============
# ============
# ============
# ============
# ============
# ============
# ============
# ============
# ============
# ============
# ============
#
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # //---->loop through the crimelines list, until there's a match
#
# # loop then check the news title and news contents, to see if  A is in B #
#
# s = localines[9]  # get crime from text file.
# t = "西環"  # get crime from web
# print("s=" + s)  # for debugging
# print("t=" + t)  # for debugging
# if s == t:  # string matching
#     print("s = t")  # if find a match, then find the corresponding location
# else:
#     print("s != t")  # if s, t don't match at this round, then check the next crime name in the list.
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # =
# # //---->substring containing:
# # ================
# # s = "This be a string"
# # if s.find("is") == -1:
# #     print "No 'is' here!"
# # else:
# #     print "Found 'is' in the string."
# # ================
#
# # //---->inspiration for storing data pairs into database
# # ================
# # list1 = [1, 2, 3, 4, 5]
# # list2 = [10, 20, 30, 40, 50]
# # list3 = [100, 200, 300, 400, 500]
# # for i, (l1, l2, l3) in enumerate(zip(list1, list2, list3)):
# #     print(i, l1, l2, l3)
# # ================

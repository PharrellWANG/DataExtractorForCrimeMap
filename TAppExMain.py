#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title: data extractor for crime map #
# starting...                         #
# go!                                 #
from __future__ import print_function
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen, Request
import sys
import geocoder
from datetime import datetime
import mysql.connector

# =========== connecting to mysql
config = {
    'user': 'root',
    'password': 'bitnami',
    'host': '127.0.0.1',
    'database': 'crimemap',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
add_rec = ("INSERT INTO crimemaprec "
           "(issuetime, location, crime, crimecat, latitude, longitude, title, URL) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
# =========== connecting to mysql

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

member = collection[1]
data_rec = ()
title = member.find("h3")
title = title.string
ref = member.find('a').get('href')
# for reading url containing Traditional Chinese words
refpart2 = ref[20:]
s = refpart2
s = urllib.parse.quote(s)
url = 'http://www.hk01.com/01%s' % s
print(url)

print()
print("     #1. Number of news found: " + str(len(collection)))
atitle = []

orig_stdout = sys.stdout
f1 = open('ZTitleUrlPairs.txt', 'w')
sys.stdout = f1

for member in collection:
    data_rec = ()
    title = member.find("h3")
    title = title.string
    ref = member.find('a').get('href')
    # for reading url containing Traditional Chinese words
    refpart2 = ref[20:]
    s = refpart2
    s = urllib.parse.quote(s)
    url = 'http://www.hk01.com/01%s' % s

    req2 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page2 = urlopen(req2).read()
    soup2 = BeautifulSoup(page2, 'lxml')  # single page

    for crime in crimelines:
        if crime not in title:
            continue
        else:  # crime in the title
            if "爆竊" == crime:
                crimecat = "burglary"
            elif "攻擊" == crime or "持械攻擊" == crime:
                crimecat = "violent crime"
            elif "兇殺" == crime or "謀殺" == crime or "殺人" == crime:
                crimecat = "homicide"
            elif "搶劫" == crime or "搶掠" == crime or "行搶" == crime or "劫" == crime or "劫案" == crime:
                crimecat = "robbery"
            elif "襲警" == crime or "偷拍" == crime or "傷人" == crime or "家暴" == crime or "家庭暴力" == crime or "酒後駕車" == crime or "酒駕" == crime or "毆打" == crime or "騷亂" == crime or "暴力" == crime or "縱火" == crime:
                crimecat = "wounding and serious assault"
            elif "毒駕" == crime or "毒品" == crime or "毒品買賣" == crime or "買賣毒品" == crime or "毒品走私" == crime or "走私毒品" == crime or "吸食毒品" == crime:
                crimecat = "serious drug offenses"
            elif "恐嚇" == crime:
                crimecat = "criminal intimidation"
            elif "強暴" == crime or "賣淫" == crime or "性交易" == crime or "強姦" == crime or "非禮" == crime or "騷擾" == crime or "性暴力" == crime:
                crimecat = "rape"
            elif "偷竊" == crime or "盜竊" == crime or "闖空門" == crime:
                crimecat = "all thefts"
            elif "扒竊" == crime or "打荷包" == crime:
                crimecat = "pickpocketing"
            elif "失車" == crime or "劫車" == crime:
                crimecat = "motor vehicles reported missing"
            elif "勒索" == crime or "詐騙" == crime or "行騙" == crime or "物業騙案" == crime or "圍標案" == crime or "侵權" == crime:
                crimecat = "deception"
            if 3 == 2:
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
                            with open("ZPairs_allRecords_with_dup_indicated.txt", "a") as pairs:
                                data_rec = list(data_rec)
                                pairs.write('issue time :' + issue_time)
                                data_rec.insert(0, str(issue_time))
                                pairs.write("\n")
                                pairs.write('location   :' + location)
                                data_rec.insert(1, str(location))
                                pairs.write("\n")
                                pairs.write('crime      :' + crime)
                                data_rec.insert(2, str(crime))
                                pairs.write("\n")
                                pairs.write('crime cato :' + crimecat)
                                data_rec.insert(3, str(crimecat))
                                pairs.write("\n")
                                pairs.write('latitude   :' + str(lat))
                                data_rec.insert(4, str(lat))
                                pairs.write("\n")
                                pairs.write('longitude  :' + str(lng))
                                data_rec.insert(5, str(lng))
                                pairs.write("\n")
                                pairs.write('title      :' + title)
                                data_rec.insert(6, str(title))
                                pairs.write("\n")
                                pairs.write('URL        :' + url)
                                data_rec.insert(7, str(url))
                                pairs.write("\n")
                                data_rec = tuple(data_rec)
                                try:
                                    cursor.execute(add_rec, data_rec)
                                    cnx.commit()
                                except mysql.connector.errors.IntegrityError:
                                    pairs.write("Duplicated entry detected, I won't add it twice.")
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
                        with open("ZPairs_allRecords_with_dup_indicated.txt", "a") as pairs:
                            data_rec = list(data_rec)
                            pairs.write('issue time :' + issue_time)
                            data_rec.insert(0, str(issue_time))
                            pairs.write("\n")
                            pairs.write('location   :' + location)
                            data_rec.insert(1, str(location))
                            pairs.write("\n")
                            pairs.write('crime      :' + crime)
                            data_rec.insert(2, str(crime))
                            pairs.write("\n")
                            pairs.write('crime cato :' + crimecat)
                            data_rec.insert(3, str(crimecat))
                            pairs.write("\n")
                            pairs.write('latitude   :' + str(lat))
                            data_rec.insert(4, str(lat))
                            pairs.write("\n")
                            pairs.write('longitude  :' + str(lng))
                            data_rec.insert(5, str(lng))
                            pairs.write("\n")
                            pairs.write('title      :' + title)
                            data_rec.insert(6, str(title))
                            pairs.write("\n")
                            pairs.write('URL        :' + url)
                            data_rec.insert(7, str(url))
                            pairs.write("\n")
                            data_rec = tuple(data_rec)
                            try:
                                cursor.execute(add_rec, data_rec)
                                cnx.commit()
                            except mysql.connector.errors.IntegrityError:
                                pairs.write("Duplicated entry detected, I won't add it twice.")
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

cursor.close()
cnx.close()

print("     #2. Time lapsed: " + str(datetime.now() - start))
print()
print("$----> data extractor ending... #####")
print("=============================")

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

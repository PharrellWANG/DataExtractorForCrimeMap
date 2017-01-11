# !/usr/bin/env python
# -*- coding: utf-8 -*-

""" title: data extractor for crime map """

from __future__ import print_function

import os
import sys
import time
import urllib
from datetime import datetime
from urllib.request import Request, urlopen

import geocoder
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup

# import subprocess

interval = 20


def tick():
    """I JUST ADD THIS SENTENCE FOR ELIMINATE A GREY WAVE LINE."""
    # =========== connecting to mysql
    print()
    print()
    print()
    print()
    print(">>>Database connecting on progress...")
    print(">>>.....................")

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
    print(">>>Database connection is successful.")
    # =========== connecting to mysql
    start = datetime.now()
    print("=============================")
    print('$>>>>> Starting time:    %s' % datetime.now())
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
    f1 = open('ZTitleUrlPairs.txt', 'w')
    sys.stdout = f1

    for member in collection:
        data_rec = ()
        title = member.find("h3")
        title = title.string
        ref = member.find('a').get('href')
        # for reading url containing Traditional Chinese words
        refpart2 = ref[21:]
        s = refpart2
        s = urllib.parse.quote(s)
        url = 'https://www.hk01.com/%s' % s

        req2 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page2 = urlopen(req2).read()
        soup2 = BeautifulSoup(page2, 'lxml')  # single page

        for crime in crimelines:
            if crime not in title:
                continue
            else:  # crime in the title
                if "爆竊" == crime:
                    crimecat = "burglary"
                elif "攻擊" == crime or "持械攻擊" == crime or "持械大混戰" == crime or "刑毀" == crime or "射爆" == crime:
                    crimecat = "violent crime"
                elif "兇殺" == crime or "謀殺" == crime or "殺人" == crime:
                    crimecat = "homicide"
                elif "搶劫" == crime or "搶掠" == crime or "行搶" == crime \
                        or "劫" == crime or "劫案" == crime:
                    crimecat = "robbery"
                elif "襲警" == crime or "偷拍" == crime or "傷人" == crime \
                        or "家暴" == crime or "家庭暴力" == crime or "酒後駕車" == crime \
                        or "酒駕" == crime or "毆打" == crime or "騷亂" == crime \
                        or "暴力" == crime or "縱火" == crime:
                    crimecat = "wounding and serious assault"
                elif "毒駕" == crime or "毒品" == crime or "毒品買賣" == crime \
                        or "買賣毒品" == crime or "毒品走私" == crime or "走私毒品" == crime or "吸食毒品" == crime:
                    crimecat = "serious drug offenses"
                elif "恐嚇" == crime:
                    crimecat = "criminal intimidation"
                elif "強暴" == crime or "賣淫" == crime or "性交易" == crime \
                        or "強姦" == crime or "非禮" == crime or "騷擾" == crime or "性暴力" == crime:
                    crimecat = "rape"
                elif "偷竊" == crime or "盜竊" == crime or "闖空門" == crime:
                    crimecat = "all thefts"
                elif "扒竊" == crime or "打荷包" == crime:
                    crimecat = "pickpocketing"
                elif "失車" == crime or "劫車" == crime:
                    crimecat = "motor vehicles reported missing"
                elif "勒索" == crime or "詐騙" == crime or "行騙" == crime \
                        or "物業騙案" == crime or "圍標案" == crime or "侵權" == crime:
                    crimecat = "deception"
                if 3 == 2:
                    # tod---->  loop the titles in DB,
                    # compare to the current title,
                    # if duplicated, "continue";else go go go.
                    continue
                else:
                    for location in localines:
                        if location not in title:
                            contents = member.find(class_="blog_listing__item__content__caption")
                            contents = str(contents)
                            if location not in contents:
                                continue
                            else:
                                g = geocoder.google(location)
                                try:
                                    lat = g.latlng[0]
                                    lng = g.latlng[1]
                                except IndexError:
                                    break
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
    print("     #2. Time lapsed: " + str(datetime.now() - start))
    print()
    print("$----> data extractor ending... #####")
    print('$>>>>> Ending time:  %s' % datetime.now())
    print("\n")

    print(">>>Database is shutting down...")
    print(">>>.....................")
    cursor.close()
    cnx.close()
    print(">>>Database is successfully shut down.")

print()
print()
print('Crawler execution interval(s): %s' % interval)
tick()

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=interval)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

# title: data extractor for crime map #
# starting...                         #
# go!                                 #
from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import sys

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listcrime.txt', 'r+') as fc:
    crimelines = [line[:-1] for line in fc]  # for escaping the newline next to the location string

with open('/Users/Pharrell_WANG/Documents/CrimeMapProject/Z-inputFilesForCrimeMap/listlocation.txt', 'r+') as fl:
    localines = [line[:-1] for line in fl]  # for escaping the newline next to the location string

req = Request('https://www.hk01.com/section/%E6%B8%AF%E8%81%9E',
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()

soup = BeautifulSoup(page, 'lxml')

# //--->for redirecting the web contents to text file  for the purpose of debugging??
orig_stdout = sys.stdout
f = open('output_of_inspect.txt', 'w')
sys.stdout = f

print(soup.prettify())

sys.stdout = orig_stdout
f.close()
# //--->redirection completed

collection = soup.find_all("div", class_="blog_listing__item")

# //--->for redirecting the web contents to text file  for the purpose of debugging??
orig_stdout = sys.stdout
f = open('collection.html', 'w')
sys.stdout = f

print(collection)

sys.stdout = orig_stdout
f.close()
# //--->redirection completed

# //--->for redirecting the web contents to text file  for the purpose of debugging??
orig_stdout = sys.stdout
f1 = open('extracted_title_link_pairs.txt', 'w')
sys.stdout = f1

for member in collection:
    title = member.find("h3")
    title = title.string
    ref = member.find('a').get('href')
# for reading url containing Traditional Chinese words
    refpart2 = ref[20:]
    s = refpart2
    s = urllib.parse.quote(s)
    url = 'http://www.hk01.com/01%s' % (
        s)
    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()

    soup = BeautifulSoup(page, 'lxml')

    # //--->for redirecting the web contents to text file  for the purpose of debugging??
    orig_stdout = sys.stdout
    f = open('page_of_single_news.html', 'w')
    sys.stdout = f
    print(soup.prettify())
    sys.stdout = orig_stdout
    f.close()
    # //--->redirection completed

    # for crime in crimelines:
    #     if crime not in title:
    #         continue
    #     else:
    #         for location in localines:
    #             if location not in title: # go check contents first
    #                 req = Request(ref, headers={'User-Agent': 'Mozilla/5.0'})
    #                 page = urlopen(req).read()
    #                 soup = BeautifulSoup(page, 'lxml')
    #                 # //--->for redirecting the web contents to text file  for the purpose of debugging??
    #                 orig_stdout = sys.stdout
    #                 f = open('output_of_inspect_single_news.txt', 'w')
    #                 sys.stdout = f
    #                 print(soup.prettify())
    #                 sys.stdout = orig_stdout
    #                 f.close()
    #                 # //--->redirection completed

    print(title)
    print(ref)
    print(url)
    print()

sys.stdout = orig_stdout
f.close()
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

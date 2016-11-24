# title: data extractor for crime map #
# starting...                         #
# go!                                 #
from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import sys

s = '博評-政經社'
s = urllib.parse.quote(s)
url = 'http://www.hk01.com/01%s'%(s)
url = url + '/56139/%E9%A6%99%E6%B8%AF%E6%88%AA%E7%8D%B2%E6%98%9F%E6%B4%B2%E8%A3%9D%E7%94%B2%E8%BB%8A-%E5%8F%B0%E6%96%B0%E8%BB%8D%E4%BA%8B%E5%90%88%E4%BD%9C%E5%8F%AF%E5%8F%97%E5%BD%B1%E9%9F%BF-'

print(url)
req = Request(url,
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()

soup = BeautifulSoup(page, 'lxml')

# //--->for redirecting the web contents to text file  for the purpose of debugging??
orig_stdout = sys.stdout
f = open('test.txt', 'w')
sys.stdout = f

print(soup.prettify())

sys.stdout = orig_stdout
f.close()
# //--->redirection completed

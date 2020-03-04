import urllib.request
from bs4 import beautifulSoup


url = 'https://wuhanvirus.kr/'
html = urllib.request.urlopen(url).read()
soup = beautifulSoup(html,'html.parser')

print(soup)

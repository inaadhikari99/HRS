import requests
from bs4 import BeautifulSoup
from csv import writer
import urllib.request

url = "https://www.booking.com/"
# get the html
r = requests.get(url)
htmlcontent = r.content
print(htmlcontent)
# pasrse the html
soup = BeautifulSoup(htmlcontent, 'html.parser')
print(soup.prettify())
# html tree traversal
print(soup.find_all("img"))
# images = soup.find_all("img", class_="rg_i Q4LuWd")
# print(images)
# number = 0
# for image in images:
#     image_src = image["src"]
# print(image_src)
# urllib.request.urlretrieve(image_src, str(number))
# number += 1

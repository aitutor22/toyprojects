#the following code scrapes the transcripts of obama's speeches
#and stores it in an ouput text file

from bs4 import BeautifulSoup
import requests

f = open("output.txt", "a", encoding="utf-8")

#get the links from the front page
url = "http://obamaspeeches.com/"
content = requests.get(url).text
soup = BeautifulSoup(content, "lxml")

for l in soup.table.table.find_all("a"):
    print(l.get("href"))

#get links to obama's speeches
links = [(url + l.get("href")) for l in soup.table.table.find_all("a")]

#loops through all the links and scrapes the speech contents
for link in links:
    content = requests.get(link).text
    soup = BeautifulSoup(content, "lxml")
    speech_contents = soup.table.find_all("table")[1].text

    f.write(speech_contents)

f.close()

print(len(links))
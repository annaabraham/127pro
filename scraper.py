from selenium import webdriver 
from bs4 import BeautifulSoup
import requests
import time 
import csv

starturl="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(starturl)
time.sleep(10)

def scrape():
headers=["NAME","LIGHT-YEARS FROM EARTH","PLANET MASS","STELLAR MAGNITUDE","DISCOVERY DATE","HYPER-LINK","PLANET TYPE","PLANET RADIUS","ORBITAL RADIUS","ORBITAL PERIOD","ECCENTRICITY"]
planetdata=[]
newplanetdata=[]
    for i in range(0,198):
        
     soup=BeautifulSoup(browser.page_source,"html.parser")
     for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
         litags=ultag.find_all("li")
         templist=[]
         for index,litag in enumerate(litags):
             if index==0:
                 templist.append(litag.find_all("a")[0].contents[0])
             else:
                 try:
                     templist.append(litag.contents[0])
                 except:
                     templist.append("")
        Hyperlinklitag=litags[0]
        templist.append("https://exoplanets.nasa.gov/"+Hyperlinklitag.find_all("a",href=True)[0]["href"])
         planetdata.append(templist)
     browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a')
    

def scrapemoredata(HYPERLINK):
    page=requests.get(HYPERLINK)
    soup=BeautifulSoup(page.content,"html.parser")
    for trtag in soup.find_all("tr",attrs={"class,exoplanet"}):
        tdtags=trtag.find_all("td")
        templist=[]
        for tdtag in tdtags:
            try:
                templist.append(tdtag.find_all("divtag",attrs={"class,exoplanet"})[0].contents[0])
            except:
                templist.append("")
        newplanetdata.append(templist)



scrape()
for data in planetdata:
    scrapemoredata(data[5])
finalplanetdata=[]
for index,data enumerate(planetdata):
    newplanetdataelement=newplanetdata[index]
    newplanetdataelement=[elem.replace("/n","")for elem in newplanetdataelement]
    newplanetdataelement=newplanetdataelement[:7]
    finalplanetdata.append(data+newplanetdataelement)

 with open("scraper2.csv","w")as f:
         csvwriter=csv.writer(f)
         csvwriter.writerow(headers)
         csvwriter.writerow(planetdata)
       
import sys
import csv
import os
import configparser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import time
from multiprocessing import Process

myset=set()

def getName(element):
    print(element.get_attribute('innerHTML'))
    try:
        t=element.find_element("xpath", ".//div").text
    except:
        t=element.find_element("xpath", ".//*[@class='biGQs _P fiohW fOtGX']").text


    return t

with open('rest_source.csv', 'a',newline='') as the_file:
    the_file.write('')

with open('location_source.csv', 'a',newline='') as the_file:
    the_file.write('')

with open('hotel_source.csv', 'a',newline='') as the_file:
    the_file.write('')

configParser=configparser.RawConfigParser()
configParser.read("../scrapper.cfg")

url_restaraunt = configParser.get("config-data","rest_url")
url_location = configParser.get("config-data","loc_url")
url_hotel = configParser.get("config-data","hotel_url")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url_restaraunt)


csvFile = open('rest_source.csv', 'a', encoding="utf-8",newline="")
csvWriter = csv.writer(csvFile)

for i in range(0, 1000):
    print("Page " + str(i))
    time.sleep(5)

    q = driver.find_element("xpath", "//div[@class='YtrWs']")
    q = q.find_elements("xpath", ".//div[1]/div[2]/div[1]/div/span/a[@target='_blank']")
    for location in q:
        _href_location = location.get_attribute("href")
        if _href_location not in myset:
            myset.add(_href_location)
            csvWriter.writerow(
                [_href_location,"Рестораны"])
    try:
        driver.find_element("xpath",
                            "//a[@class='nav next rndBtn ui_button primary taLnk']").click()
    except:
        print("Sorry!")
        break

driver.quit()

csvFile.close()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url_location)

csvFile = open('location_source.csv', 'a', encoding="utf-8",newline="")
csvWriter = csv.writer(csvFile)

#####
time.sleep(3)

elements = driver.find_elements("xpath",'//main/span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[1]/div[1]/div[2]/div/div[1]/div/span/div/div[2]/div/div/div[1]/div')
length=len(elements)
counter = 1
hasSecondNext=False
for i in range(1,100):
    time.sleep(4)
    try:
        e=driver.find_element("xpath", "//button[@class='UikNM _G B- _S _T c G_ P0 wSSLS TXrCr']") #Показать больше строка
        if ("больше" in e.text):
            e.click()
    except:
        print("CANT CLICK")
    time.sleep(3)

    try:

        element=driver.find_element("xpath","//div[3]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[1]/div["+str(i)+"]/a") #Вывод категорий?
    except:
        break
    elem_name=element.find_element("xpath",".//div").text
    time.sleep(3)
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()
    #element.click()
    time.sleep(3)
    while(True):

        q = driver.find_elements("xpath", "//div[@class='alPVI eNNhq PgLKC tnGGX']/a[1]")
        for location in q:
            _href_location = location.get_attribute("href")
            if _href_location not in myset:
                myset.add(_href_location)
                csvWriter.writerow(
                    [_href_location,elem_name])
        try:
            if (elem_name=="Природа и парки"):
                driver.find_element("xpath","//body/div[1]/main/span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[2]/div/div/section[41]/span/div/div[2]/div/div[3]/div/span/button")
            driver.find_element("xpath",
                                "//html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div/a").click()
            time.sleep(5)
            print("Page")
        except:
            counter+=1
            print("End of list")
            break

elements = driver.find_elements("xpath",'//main/span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[1]/div[1]/div[2]/div/div[1]/div/span/div/div[2]/div/div/div[1]/div')
length=len(elements)
counter = 1
iss=False

for i in range(1,100):
    if not iss:
        iss=True
        continue
    time.sleep(3)
    try:

        e=driver.find_element("xpath", '//body/div[1]/main/span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[1]/div[1]/div[2]/div/div[1]/div/span/div/div[2]/div/div/div[2]/button')
        if ("больше" in e.text):
            e.click()
    except:
        print("CANT CLICK")
    time.sleep(3)
    try:
        element=driver.find_element("xpath","//html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div/div/div/div["+str(i)+"]/a")
        #element=driver.find_element("xpath","//html/body/div[1]/main/span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[1]/div[1]/div[2]/div/div[1]/div/span/div/div[2]/div/div/div[1]/div["+str(i)+"]/a")
    except:
        break
    elem_name=element.find_element("xpath",".//div[1]").text
    time.sleep(3)
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()
    #element.click()
    time.sleep(3)
    while(True):

        q = driver.find_elements("xpath", "//div[@class='alPVI eNNhq PgLKC tnGGX']/a[1]")
        for location in q:
            _href_location = location.get_attribute("href")
            if _href_location not in myset:
                myset.add(_href_location)
                csvWriter.writerow(
                    [_href_location,elem_name])
        try:
            driver.find_element("xpath",
                                "//html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[3]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div/a").click()
            time.sleep(3)
            print("Page")
        except:
            counter+=1
            print("End of list")
            break











driver.quit()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url_hotel)

csvFile = open('hotel_source.csv', 'a', encoding="utf-8",newline="")
csvWriter = csv.writer(csvFile)

for i in range(0, 1000):
    q = driver.find_elements("xpath", '//div/div[1]/div[2]/div[1]/div/div/a[1]')
    for location in q:
        _href_location = location.get_attribute("href")
        if _href_location not in myset:
            myset.add(_href_location)
            with open('hotel_source.csv', 'a') as the_file:
                the_file.write(_href_location+"\n")
    try:
        time.sleep(2)
        try:
            driver.find_element("xpath","//div[1]/div/div[2]/div[4]/div[2]/div[9]/div/div/button").click()
        except:
            print("noclick")

        time.sleep(2)
        driver.find_element("xpath",
                            "//*[@class='nav next ui_button primary']").click()

    except:
        print("End of list")
        break
driver.quit()

csvFile.close()
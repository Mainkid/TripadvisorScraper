import sys
import csv
import os
import configparser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from multiprocessing import Process

with open('rest.txt', 'a',newline='') as the_file:
    the_file.write('')

with open('loc.txt', 'a',newline='') as the_file:
    the_file.write('')

with open('hotel.txt', 'a',newline='') as the_file:
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

#for i in range(0, 1000):
#    print("Page " + str(i))
#    time.sleep(5)

#    q = driver.find_element("xpath", "//div[@class='YtrWs']")
#    q = q.find_elements("xpath", ".//div[1]/div[2]/div[1]/div/span/a[@target='_blank']")
#    for location in q:
#        _href_location = location.get_attribute("href")
#        with open('rest.txt', 'a') as the_file:
#            the_file.write(_href_location+"\n")

#    try:
#        driver.find_element("xpath",
#                            "//a[@class='nav next rndBtn ui_button primary taLnk']").click()
#    except:
#        print("Sorry!")
#        break
#driver.quit()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url_location)

for i in range(0, 1000):
    q = driver.find_elements("xpath", '//div/span/div/article/div[2]/header/div/div/a[1]')
    for location in q:
        _href_location = location.get_attribute("href")
        with open('loc.txt', 'a') as the_file:
            the_file.write(_href_location+"\n")
    try:
        driver.find_element("xpath",
                            "//span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[2]/div/div/section[40]/span/div[1]/div/div[1]/div[2]/div").click()
        time.sleep(3)
    except:
        print("End of list")
        break

driver.quit()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url_hotel)

for i in range(0, 1000):
    q = driver.find_elements("xpath", '//div/div[1]/div[2]/div[1]/div/div/a[1]')
    for location in q:
        _href_location = location.get_attribute("href")
        with open('hotel.txt', 'a') as the_file:
            the_file.write(_href_location+"\n")
    try:
        driver.find_element("xpath",
                            "//span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[2]/div/div/section[40]/span/div[1]/div/div[1]/div[2]/div").click()
        time.sleep(3)
    except:
        print("End of list")
        break
driver.quit()
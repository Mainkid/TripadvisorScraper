import sys
import csv
import os
import uuid
import configparser
import ctypes
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from multiprocessing import Process,Value, Manager
from RestarauntScrapper import ScrapRestaraunt
from HotelScrapper import ScrapHotel
from LocationScrapper import ScrapLocation
from Tmp_services.testProxy import get_chromedriver

num_page = 100

hotel_page=0
restaraunt_page=0
location_page=0







def init_csv(filename):
    if (os.path.exists(filename)):
        return
    csvFile = open(filename, 'a', encoding="utf-8",newline="")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(
        ["Организация", "Ссылка", "Адрес", "Раздел", "Категория", "Тип", "Отзывов", "Заголовок", "Отзыв", "Тег",
         "Оценка",
         "Дата посещения", "Дата отзыва", "Количество лайков", "Имя", "Профиль",
         "Количество подписок", "Количество подписчиков",
         "Количество публикаций", "Количество блаодарностей", "Критик уровня", "Количество посещенных городов",
         "Место проживания", "Год регистрации"])
    csvFile.close()

def change_proxy(proxy):
    flag=False
    with open("Tmp_services/proxyList.txt") as file:
        for line in file:
            if line==proxy['proxy'] and not flag:
                flag=True
            elif flag:
                proxy['proxy']=line

def RestarauntScrap(url,proxy_login,proxy_password,proxy):
    proxy_val=proxy['proxy']
    with open('Data_url/rest_source.csv', newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            try:
                driver2 = get_chromedriver(proxy_val.split(":")[0],proxy_val.split(":")[1],proxy_login,proxy_password,True)
                ScrapRestaraunt(row[0].replace("\n",''),driver2,proxy_login,proxy_password,proxy)
            except Exception as e:
                #driver2.save_screenshot("/Sreenshots/" + str(uuid.uuid4())+".png")
                if ("denied" in driver2.page_source.lower()):
                    change_proxy(proxy)
                else:
                    print("____")
                    print("Error Restaraunt")
                    print(e)
                    print("____")
                driver2.quit()


def LocationScrap(url,proxy_login,proxy_password,proxy):
    proxy_val = proxy['proxy']
    with open('Data_url/location_source.csv', newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:

            try:
                driver2 = get_chromedriver(proxy_val.split(":")[0],proxy_val.split(":")[1],proxy_login,proxy_password,True)
                ScrapLocation(row[0].replace("\n",''),row[1],driver2,proxy_login,proxy_password,proxy)
            except Exception as e:
                #driver2.save_screenshot("/Sreenshots/"+str(uuid.uuid4())+".png")
                if ("denied" in driver2.page_source.lower()):
                    change_proxy(proxy)
                else:
                    print("____")
                    print("ERROR Location")
                    print(e)
                    print("____")
                driver2.quit()

def HotelScrap(url,proxy_login,proxy_password,proxy):
    proxy_val = proxy['proxy']
    with open('Data_url/hotel_source.csv', newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            try:
                driver2 = get_chromedriver(proxy_val.split(":")[0],proxy_val.split(":")[1],proxy_login,proxy_password,True)

                ScrapHotel(row[0].replace("\n",''),driver2,proxy_login,proxy_password,proxy)
            except Exception as e:
                #driver2.save_screenshot("/Sreenshots/" +str( uuid.uuid4())+".png")
                if ("denied" in driver2.page_source.lower()):
                    change_proxy(proxy)
                else:
                    print("____")
                    print("ERROR hotel!")
                    print(e)
                    print("____")
                driver2.quit()


if __name__ == "__main__":
    time.sleep(10)
    init_csv("restaraunt.csv")
    init_csv("hotel.csv")
    init_csv("location.csv")

    configParser=configparser.RawConfigParser()
    configParser.read("scrapper.cfg")

    url_restaraunt = configParser.get("config-data","rest_url")
    url_location = configParser.get("config-data","loc_url")
    url_hotel = configParser.get("config-data","hotel_url")



    hotel_page = configParser.get("config-data","hotel_page")
    restaraunt_page = configParser.get("config-data","rest_page")
    location_page = configParser.get("config-data","loc_page")

    proxy_login=configParser.get("proxy-settings","login")
    proxy_password=configParser.get("proxy-settings","password")

    manager = Manager()
    d = manager.dict()

    with open("Tmp_services/proxyList.txt") as file:
        for line in file:
            d['proxy'] = line
            break



    p_rest = Process(target=RestarauntScrap, args=(url_restaraunt,proxy_login,proxy_password,d,))
    p_location = Process(target=LocationScrap, args=(url_location,proxy_login,proxy_password,d,))
    p_hotel = Process(target=HotelScrap,args=(url_hotel,proxy_login,proxy_password,d,))
    p_rest.start()
    p_location.start()
    p_hotel.start()
    p_rest.join()
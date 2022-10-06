import sys
import csv
import os
import configparser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from multiprocessing import Process
from RestarauntScrapper import ScrapRestaraunt
from HotelScrapper import ScrapHotel
from LocationScrapper import ScrapLocation

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

def RestarauntScrap(url):
    with open("Data_url/rest.txt") as file:
        lines = file.readlines()
    for link in lines:
        try:
            driver2 = webdriver.Remote("http://selenium:4444/wd/hub",
                                        desired_capabilities=DesiredCapabilities.CHROME)
            ScrapRestaraunt(link.replace("\n",''),driver2)
        except:
            print("Error Restaraunt")
            driver2.quit()


def LocationScrap(url):
    with open("Data_url/loc.txt") as file:
        lines = file.readlines()
    for ref in lines:
        try:
            driver2 = webdriver.Remote("http://selenium:4444/wd/hub",
                                       desired_capabilities=DesiredCapabilities.CHROME)
            ScrapLocation(ref.replace("\n",''),driver2)
        except:
            print("ERROR Location")
            driver2.quit()

def HotelScrap(url):
    with open("Data_url/hotel.txt") as file:
        lines = file.readlines()
    for link in lines:
        try:
            driver2 = webdriver.Remote("http://selenium:4444/wd/hub",
                                        desired_capabilities=DesiredCapabilities.CHROME)

            ScrapHotel(link.replace("\n",''),driver2)
        except:
            print("ERROR hotel!")
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

    p_rest = Process(target=RestarauntScrap, args=(url_restaraunt,))
    p_location = Process(target=LocationScrap, args=(url_location,))
    p_hotel = Process(target=HotelScrap,args=(url_hotel,))
    p_rest.start()
    p_location.start()
    p_hotel.start()
    p_rest.join()
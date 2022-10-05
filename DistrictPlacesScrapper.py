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
    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(url)

    time.sleep(3)
    for i in range(0,num_page):
        print("Page "+ str(i))


        q=driver.find_element("xpath","//div[@class='YtrWs']")
        q=q.find_elements("xpath",".//div[1]/div[2]/div[1]/div/span/a[@target='_blank']")
        for location in q:
            _href_location=location.get_attribute("href")
            try:
                driver2 = webdriver.Remote("http://selenium:4444/wd/hub",
                                           desired_capabilities=DesiredCapabilities.CHROME)
                ScrapRestaraunt(_href_location,driver2)
            except:
                print("Error Restaraunt")
                driver2.quit()

        try:
            driver.find_element("xpath",
                                "//a[@class='nav next rndBtn ui_button primary taLnk']").click()
        except:
            print("End of list")
    driver.quit()

def LocationScrap(url):
    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    for i in range(0, num_page):
        q=driver.find_elements("xpath",'//div/span/div/article/div[2]/header/div/div/a[1]')
        for location in q:
            _href_location = location.get_attribute("href")
            try:
                driver2 = webdriver.Remote("http://selenium:4444/wd/hub",
                                           desired_capabilities=DesiredCapabilities.CHROME)
                ScrapLocation(_href_location,driver2)
            except:
                print("ERROR Location")
                driver2.quit()
        try:
            driver.find_element("xpath",
                                "//span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[2]/div/div/section[40]/span/div[1]/div/div[1]/div[2]/div").click()
            time.sleep(3)
        except:
            print("End of list")
    driver.quit()

def HotelScrap(url):
    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    for i in range(0, num_page):
        q = driver.find_elements("xpath", '//div/div[1]/div[2]/div[1]/div/div/a[1]')
        for location in q:
            _href_location = location.get_attribute("href")
            driver2 = webdriver.Remote("http://selenium:4444/wd/hub",
                                       desired_capabilities=DesiredCapabilities.CHROME)
            try:
                ScrapHotel(_href_location,driver2)
            except:
                print("ERROR hotel!")
                driver2.quit()
        try:
            driver.find_element("xpath",
                                "//span/div/div[3]/div/div[2]/div[2]/span/div/div[3]/div/div[2]/div/div/section[40]/span/div[1]/div/div[1]/div[2]/div").click()
            time.sleep(3)
        except:
            print("End of list")
    driver.quit()

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

    p_rest = Process(target=RestarauntScrap, args=(url_restaraunt,))
    p_location = Process(target=LocationScrap, args=(url_location,))
    p_hotel = Process(target=HotelScrap,args=(url_hotel,))
    p_rest.start()
    p_location.start()
    p_hotel.start()
    p_rest.join()
import sys
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from RestarauntScrapper import ScrapRestaraunt
from HotelScrapper import ScrapHotel
from LocationScrapper import ScrapLocation

target_file="locations"

num_page = 100

url = "https://www.tripadvisor.ru/Restaurants-g2324084-Perm_Krai_Volga_District.html"
#url = "https://www.tripadvisor.ru/Attractions-g2324084-Activities-a_allAttractions.true-Perm_Krai_Volga_District.html"
#url = "https://www.tripadvisor.ru/Hotels-g298516-Perm_Perm_Krai_Volga_District-Hotels.html"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url)

# Open the file to save the review
csvFile = open(target_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

time.sleep(2)
if "Restaurants" in url:

    for i in range(0,num_page):
        q=driver.find_element("xpath","//div[@class='YtrWs']")
        q=q.find_elements("xpath",".//div[1]/div[2]/div[1]/div/span/a[@target='_blank']")
        for location in q:
            _href_location=location.get_attribute("href")
            ScrapRestaraunt(_href_location)
        driver.find_element("xpath",
                            "//a[@class='nav next rndBtn ui_button primary taLnk']").click()

elif "Activities" in url:
    for i in range(0, num_page):
        q=driver.find_elements("xpath",'//div/span/div/article/div[2]/header/div/div/a[1]')
        for location in q:
            _href_location = location.get_attribute("href")
            ScrapLocation(_href_location)
else:
    for i in range(0, num_page):
        q = driver.find_elements("xpath", '//div/div[1]/div[2]/div[1]/div/div/a[1]')
        for location in q:
            _href_location = location.get_attribute("href")
            ScrapHotel(_href_location)
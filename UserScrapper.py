import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from webdriver_manager.chrome import ChromeDriverManager
import time

website_url_base = r"https://www.tripadvisor.ru/"
path_to_file = "reviews.csv"
num_page = 10
sleep_time=2

def ScrapUserEmblems(url):
    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)
    driver.get(url)
    time.sleep(sleep_time)
    try:
        total_thanks = driver.find_element("xpath","//div[4]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[2]").text
    except:
        total_thanks = 0
    try:
        level = driver.find_element("xpath", "//div[4]/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div/span").text
    except:
        level = 0
    driver.quit()

    return [total_thanks,level]

def ScrapUserCities(url):
    driver = webdriver.Remote("http://selenium:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)
    driver.get(url)
    time.sleep(sleep_time)

    cities=driver.find_element("xpath","//div[4]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span/span").text
    cities=cities[1:-1]
    driver.quit()
    return [cities]

def ScrapUser(url):
    driver = webdriver.Remote("http://selenium:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)
    driver.get(url)

    registration_date=""

    try:
        content_amount=driver.find_element("xpath","//div[1]/span[2]/a[@class='etCOn b Wc _S']").text
    except:
        content_amount = driver.find_element("xpath", "//div[1]/span[2]").text
    try:
        subscribers=driver.find_element("xpath","//div[2]/span[@class='rNZKv']").text
    except:
        subscribers = driver.find_element("xpath", "//div[2]/span[@class='rNZKv']/a[@class='etCOn b Wc _S']").text
    try:
        subscriptions=driver.find_element("xpath","//div[3]/span[2]/a[@class='etCOn b Wc _S']").text
    except:
        subscriptions = driver.find_element("xpath", "//div[3]/span[2]").text
    try:
        city = driver.find_element("xpath","//div[2]/div/div/div[3]/div[3]/div[1]/div/div[2]/span[1]").text
        if ("сообществе" in city):
            registration_date = city[15:]
            city=""
    except:
        city=""

    if (registration_date==""):
        try:
            registration_date=driver.find_element("xpath","//div[2]/div/div/div[3]/div[3]/div[1]/div/div[2]/span[2]").text
            registration_date=registration_date[15:]
        except:
            registration_date=""

    emblems_href=driver.find_element("xpath","//a[@data-tab-name='Эмблемы']").get_attribute("href")
    cities_href=driver.find_element("xpath","//a[@data-tab-name='Карта путешествий']").get_attribute("href")



    emblems_list=ScrapUserEmblems(emblems_href)
    visited_cities_list=ScrapUserCities(cities_href)

    driver.quit()

    return [subscribers,subscriptions,content_amount] + emblems_list +visited_cities_list +[city,registration_date]
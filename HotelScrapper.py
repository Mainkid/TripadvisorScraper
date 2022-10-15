import sys
import csv

import webdriver_manager.chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from UserScrapper import ScrapUser
from webdriver_manager.chrome import ChromeDriverManager
import time

website_url_base = r"https://www.tripadvisor.ru/"
path_to_file = "hotel.csv"
num_page = 1000
sleep_time=4

def ScrapHotel(url,driver):
    #driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    #driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)
    driver.get(url)
    driver.implicitly_wait(sleep_time)
    # Open the file to save the review
    csvFile = open(path_to_file, 'a', encoding="utf-8",newline="")
    csvWriter = csv.writer(csvFile)

    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element("xpath", "//*[@id='HEADING']"))

    location_name = driver.find_element("xpath","//*[@id='HEADING']").text
    location_name = location_name.replace("\r\n", " ")
    location_name = location_name.replace("\n", " ")

    location_type = "Отели"
    address = driver.find_element("xpath","//div[2]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div/div/span[2]/span").text
    reviews_amount=driver.find_element("xpath","//*[@class='qqniT']").text.split(" ")[0]
    for i in range(0, num_page):


        # expand the review
        time.sleep(sleep_time)

        container = driver.find_elements("xpath", '//*[@class="YibKl MC R2 Gi z Z BB pBbQr"]')
        next_btn=container[0].find_element("xpath", ".//*[@class='Ignyf _S Z']")
        try:
            ActionChains(driver).move_to_element(next_btn).perform()
        except:
            print("Couldnt scroll!!!")

        try:
            next_btn.click()
        except:
            print("Couldnt click!")
            continue
        print(len(container))
        for j in range(0,len(container)):
            title = container[j].find_element("xpath",".//*[@class='Qwuub']/span").text

            review = container[j].find_element("xpath", ".//*[@class='QewHA H4 _a']/span").text.replace("\n", " ")

            try:
                review_date = container[j].find_element("xpath",".//*[@class='cRVSd']/span").text.split(" ")
                review_date = review_date[3]+" "+review_date[4]+" "+review_date[5]
            except:
                review_date = " "
            rating = container[j].find_element("xpath",".//*[@class='Hlmiy F1']/span").get_attribute("class")[-2:-1]


            try:
                review_likes = container[j].find_element("xpath",".//*[@class='hVSKz S2 H2 Ch sJlxi']").text.split(" ")[0]
            except:
                review_likes = 0

            try:
                visiting_date = container[j].find_element("xpath",".//*[@class='teHYY _R Me S4 H3']").text.split(" ")
                visiting_date = visiting_date[2] + " " +visiting_date[3] + " " +visiting_date[4]
            except:
                visiting_date = ""
            time.sleep(sleep_time)

            try:
                profile_link =  container[j].find_element("xpath",".//*[@class='kjIqZ I ui_social_avatar inline']").get_attribute("href")
                user_nickname = container[j].find_element("xpath",".//div[1]/div/div[2]/span/a").text
                user_data=ScrapUser(profile_link)
            except:
                print("OI")
                continue

            csvWriter.writerow(
                [location_name, url, address, "Отели", "", location_type, reviews_amount, title,
                 review, "", rating,
                 visiting_date, review_date,
                 review_likes, user_nickname, profile_link] + user_data)
            print("OK")
            # change the page

        try:
            WebDriverWait(driver, timeout=10).until(
                lambda d: d.find_element("xpath", "//*[@class='ui_button nav next primary ']"))
            driver.find_element("xpath","//*[@class='ui_button nav next primary ']").click()
        except:
            print("END OF PAGE")
            break

    driver.quit()
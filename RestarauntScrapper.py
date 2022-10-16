import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UserScrapper import ScrapUser
from webdriver_manager.chrome import ChromeDriverManager
import time


website_url_base = r"https://www.tripadvisor.ru/"
path_to_file = "restaraunt.csv"
num_page = 100
sleep_time=2

def ScrapRestaraunt(url,driver,proxy_login,proxy_password,proxy):
    # Import the webdriver

    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element("xpath","//div[2]/div[1]/div/div[4]/div/div/div[1]/h1"))
    # Open the file to save the review
    csvFile = open(path_to_file, 'a', encoding="utf-8",newline='')
    csvWriter = csv.writer(csvFile)
    reviews_amount=driver.find_element("xpath","//html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[3]/div/div[1]/div/div[1]/span").text
    reviews_amount=reviews_amount[1:-1]
    restaraunt_name=driver.find_element("xpath","//div[2]/div[1]/div/div[4]/div/div/div[1]/h1").text

    # change the value inside the range to save more or less reviews
    for i in range(0, num_page):

        # expand the review
        time.sleep(sleep_time)
        try:
            next=driver.find_elements("xpath","//span[@class='taLnk ulBlueLinks']")
            for n in next:
                n.click()
        except:
            print("No More button")
        time.sleep(sleep_time)

        container = driver.find_elements("xpath", "//div[@class='review-container']")
        print("len:" + str(len(container)))
        for j in range(len(container)):
            title = container[j].find_element("xpath",".//span[@class='noQuotes']").text
            review_date = container[j].find_element("xpath",".//span[contains(@class, 'ratingDate')]").get_attribute("title")
            rating = \
            container[j].find_element("xpath",".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute(
                "class").split("_")[3]
            rating=rating[0]
            review = container[j].find_element("xpath",".//p[@class='partial_entry']").text.replace("\n", " ")

            address = driver.find_element("xpath","//a[@href='#MAPVIEW']").text


            try:
                review_likes = container[j].find_element("xpath",".//div/div/div/div[2]/div[4]/div[2]/span[2]").text
            except:
                review_likes = 0

            try:
                visiting_date = container[j].find_element("xpath",".//div/div/div/div[2]/div[3]").text.split(" ")
                if (visiting_date[0]==""):
                    visiting_date = container[j].find_element("xpath", ".//div/div/div/div[2]/div[4]").text.split(" ")
                visiting_date = visiting_date[2]+" "+visiting_date[3]+" "+visiting_date[4]
            except:
                visiting_date=""

            user_nickname = container[j].find_element("xpath",".//div/div/div/div[1]/div/div/div[1]/div[2]/div").text
            try:
                #container[j].find_element("xpath", ".//div/div/div/div[1]/div/div/div[1]").click()
                btn = container[j].find_element("xpath", ".//div/div/div/div[1]/div/div/div[1]")
                ActionChains(driver).move_to_element(btn).click().perform()
            except:
                print("Oops")
                continue

            time.sleep(sleep_time)

            try:
                profile_link = driver.find_element("xpath","//span/div[3]/div/div/div/a").get_attribute("href")
            except Exception as e:
                print("Oops2")
                print(e)
                continue

            user_data=ScrapUser(profile_link,proxy_login,proxy_password,proxy)

            csvWriter.writerow([restaraunt_name,url,address,"Рестораны","","Рестораны",reviews_amount,title,review,"",rating,visiting_date,review_date,
                                review_likes,user_nickname,profile_link]+user_data)

            driver.find_element("xpath",("/html/body/span/div[4]")).click()


            print("OK")
        try:
            time.sleep(5)
            next_btn=driver.find_element("xpath",'.//a[@class="nav next ui_button primary"]')
            ActionChains(driver).move_to_element(next_btn).click().perform()
        except Exception as e:
            print("End Of Page")
            print(e)
            print("_____")
            break
    driver.quit()

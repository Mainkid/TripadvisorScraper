import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from UserScrapper import ScrapUser
from webdriver_manager.chrome import ChromeDriverManager
import time


website_url_base = r"https://www.tripadvisor.ru/"
path_to_file = "restaraunt.csv"
num_page = 100
sleep_time=2

def ScrapRestaraunt(url,driver):
    # Import the webdriver

    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(url)
    # Open the file to save the review
    csvFile = open(path_to_file, 'a', encoding="utf-8",newline='')
    csvWriter = csv.writer(csvFile)

    restaraunt_name=driver.find_element("xpath","//div[2]/div[1]/div/div[4]/div/div/div[1]/h1").text

    # change the value inside the range to save more or less reviews
    for i in range(0, num_page):

        # expand the review
        time.sleep(sleep_time)
        driver.find_element("xpath","//span[@class='taLnk ulBlueLinks']").click()

        container = driver.find_elements("xpath", ".//div[@class='review-container']")

        for j in range(len(container)):
            title = container[j].find_element("xpath",".//span[@class='noQuotes']").text
            review_date = container[j].find_element("xpath",".//span[contains(@class, 'ratingDate')]").get_attribute("title")
            rating = \
            container[j].find_element("xpath",".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute(
                "class").split("_")[3]
            rating=rating[0]
            review = container[j].find_element("xpath",".//p[@class='partial_entry']").text.replace("\n", " ")

            address = driver.find_element("xpath","//a[@href='#MAPVIEW']").text

            reviews_amount = container[j].find_element("xpath",".//div/div/div/div[1]/div/div/div[2]/div/div/span").text.split(" ")[0]

            try:
                review_likes = container[j].find_element("xpath",".//div/div/div/div[2]/div[4]/div[2]/span[2]").text
            except:
                review_likes = 0

            visiting_date = container[j].find_element("xpath",".//div/div/div/div[2]/div[3]").text.split(" ")
            if (visiting_date[0]==""):
                visiting_date = container[j].find_element("xpath", ".//div/div/div/div[2]/div[4]").text.split(" ")
            visiting_date = visiting_date[2]+" "+visiting_date[3]+" "+visiting_date[4]

            user_nickname = container[j].find_element("xpath",".//div/div/div/div[1]/div/div/div[1]/div[2]/div").text
            try:
                container[j].find_element("xpath", ".//div/div/div/div[1]/div/div/div[1]").click()
            except:
                print("Oops")
                continue

            time.sleep(sleep_time)

            try:
                profile_link =  driver.find_element("xpath","//span/div[3]/div/div/div/a").get_attribute("href")
            except:
                continue

            user_data=ScrapUser(profile_link)

            csvWriter.writerow([restaraunt_name,url,address,"Рестораны","Рестораны","Рестораны",reviews_amount,title,review,"",rating,visiting_date,review_date,
                                review_likes,user_nickname,profile_link]+user_data)

            driver.find_element("xpath",("/html/body/span/div[4]")).click()


            print("OK")
        try:
            driver.find_element("xpath",'.//a[@class="nav next ui_button primary"]').click()
        except:
            print("End Of Page")
            break
    driver.quit()

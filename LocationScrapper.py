import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from UserScrapper import ScrapUser
from webdriver_manager.chrome import ChromeDriverManager
import time

website_url_base = r"https://www.tripadvisor.ru/"
path_to_file = "location.csv"
num_page = 100
sleep_time=2

def ScrapLocation(url,type_loc,driver):
    #driver = webdriver.Remote("http://selenium:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)
    driver.get(url)

    # Open the file to save the review
    csvFile = open(path_to_file, 'a', encoding="utf-8",newline='')
    csvWriter = csv.writer(csvFile)

    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element("xpath", "//div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1"))

    location_name = driver.find_element("xpath","//div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1").text
    location_type = driver.find_element("xpath","//div[1]/main/div[1]/div[2]/div[2]/div/div/span/section[1]/div/div/span/div/div[1]/div[3]/div/div/div[1]").text
    reviews_amount = driver.find_element("xpath", "//span/section[1]/div/div/span/div/div[1]/div[1]/a/div/span/span").text
    address = driver.find_element("xpath", "//div/div/span/section[4]/div/div/div[2]/div[1]/span/div/div/div/button/span").text

    for i in range(0, num_page):

        # expand the review
        time.sleep(sleep_time)
        container = driver.find_elements("xpath", "//section[7]/div/div/span/section/section/div[1]/div/div[5]/div")
        print(len(container)-1)
        for j in range(len(container)-1):
            title = container[j].find_element("xpath",".//span/div/div[3]").text
            try:
                container[j].find_element("xpath",".//span/div/div[5]/div[2]/button/span").click()
            except:
                pass
            review = container[j].find_element("xpath", ".//span/div/div[5]/div[1]/div").text.replace("\n", " ")

            try:
                review_date = container[j].find_element("xpath",".//span/div/div[7]/div[1]").text

            except:
                review_date = container[j].find_element("xpath",".//span/div/div[8]/div[1]").text

            review_date = review_date.split(" ")
            review_date = review_date[1]+" "+review_date[2]+" "+review_date[3]+" "+review_date[4]
            rating = container[j].find_element("xpath",".//span/div/div[2]/*[name()='svg']").get_attribute("aria-label")
            rating=rating[0]



            try:
                review_likes = container[j].find_element("xpath",".//span/div/div[1]/div[2]/button/span/span").text
            except:
                review_likes = 0

            user_nickname=container[j].find_element("xpath",".//span/div/div[1]/div[1]/div[2]/span/a").text
            time.sleep(sleep_time)


            profile_link =  container[j].find_element("xpath",".//span/div/div[1]/div[1]/div[2]/span/a").get_attribute("href")
            visiting_date=""
            user_data=ScrapUser(profile_link)

            csvWriter.writerow(
                [location_name, url, address, "Развлечения", type_loc, location_type, reviews_amount, title, review, "", rating,
                 visiting_date, review_date,
                 review_likes, user_nickname, profile_link] + user_data)
            print("OK")
            # change the page
        try:
            driver.find_element("xpath",'//div[11]/div[1]/div/div[1]/div[2]/div/a').click()
        except:
            print("End Of Page")
            break

    driver.quit()
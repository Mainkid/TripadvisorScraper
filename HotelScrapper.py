import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
import time

website_url_base = r"https://www.tripadvisor.ru/"
path_to_file = "reviews.csv"
num_page = 10
sleep_time=2

def ScrapHotel(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    actions = ActionChains(driver)
    driver.get(url)

    # Open the file to save the review
    csvFile = open(path_to_file, 'a', encoding="utf-8")
    csvWriter = csv.writer(csvFile)

    location_name = driver.find_element("xpath","//*[@id='HEADING']").text
    location_type = driver.find_element("xpath","//div[6]/div/div/div/div[1]/div[2]/div/a/span").text

    address = driver.find_element("xpath","//div[2]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div/div/span[2]/span").text

    for i in range(0, num_page):

        # expand the review
        time.sleep(sleep_time)

        container = driver.find_elements("xpath", "//section[7]/div/div/span/section/section/div[1]/div/div[5]/div")

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
            rating = container[j].find_element("xpath",".//span/div/div[2]/*[name()='svg']").get_attribute("aria-label")


            try:
                review_likes = container[j].find_element("xpath",".//span/div/div[1]/div[2]/button/span/span").text
            except:
                review_likes = 0


            time.sleep(sleep_time)


            profile_link =  container[j].find_element("xpath",".//span/div/div[1]/div[1]/div[2]/span/a").get_attribute("href")

            user_data=ScrapUser(profile_link)

            csvWriter.writerow([])
            print("OK")
            # change the page
        driver.find_element("xpath",'//div[11]/div[1]/div/div[1]/div[2]/div/a').click()

    driver.close()
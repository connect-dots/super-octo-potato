from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import csv
import os
import sys

working = os.path.dirname(os.path.abspath(__file__))

class BingBot(object):
    """ Automatically login to Bing and search random words
    to accumulate rewards """

    def __init__(self, email, password):

        self.login_url = "https://login.live.com/"
        self.bing_url = "https://www.bing.com/"
        self.dash_url = "https://account.microsoft.com/"

        self.word_list = os.path.join(working, "word_list.txt")

        self.email = email
        self.password = password

        self.explicit_wait = 10
        self.min_search_wait = 5
        self.max_search_wait = 20

        self.num_searches_to_perform = 32

        self.driver = webdriver.Firefox()

    def login(self):
        """Automatically log into Bing Account."""
        self.driver.get(self.login_url)

        wait = WebDriverWait(self.driver, self.explicit_wait)
        wait.until(EC.presence_of_all_elements_located((By.ID, "i0116")))

        email_input = self.driver.find_element_by_name("loginfmt")
        email_input.send_keys(self.email)

        wait = WebDriverWait(self.driver, self.explicit_wait).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))

        self.driver.find_element_by_id("idSIButton9").click()

        wait = WebDriverWait(self.driver, self.explicit_wait).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))

        password_input = self.driver.find_element_by_name("passwd")
        password_input.send_keys(self.password)

        wait = WebDriverWait(self.driver, self.explicit_wait).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))

        self.driver.find_element_by_id("idSIButton9").click()

    def get_points_start(self):
        """Get current user points"""
        self.driver.get(self.dash_url)
        self.driver.implicitly_wait(5)
        self.driver.get(self.dash_url)
        self.driver.implicitly_wait(5)

        points = self.driver.find_element_by_xpath("/html[@class='ltr home-index home js picture eventlistener']/body/div[@id='page-wrapper']/div[@id='main-content-landing']/main[@id='home-index']/div[@id='home-app-host']/div[@class='ng-scope']/home-page[@class='ng-scope ng-isolate-scope']/div[1]/home-banner[@class='ng-isolate-scope']/mee-banner[@class='home-banner ng-scope ng-isolate-scope']/div[@class='amc-banner theme-dark']/div/div[@class='space-3-col ng-scope']/div[@class='info-columns']/div[@class='info-column ng-scope'][2]/mee-banner-slot-3[@class='ng-scope']/banner-rewards[@class='ng-isolate-scope']/mee-progress-view[@class='ng-isolate-scope']/div[4]/finished-view[@class='ng-scope']/mee-banner-media[@class='ng-scope']/media-body/p[@class='ng-binding'][1]")

        print(points)

    def quit(self):
        """Close the browser."""
        self.driver.close()

    def run(self):
        """Run the primary login, search, quit protocol."""
        self.login()
        self.get_points_start()
        self.quit()


credentials = os.path.join(working, "bing_accounts.csv")

with open(credentials, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        user_id = row[0]
        password = row[1]

        bing_bot = BingBot(user_id, password)
        bing_bot.run()

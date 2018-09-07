from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import csv
import os
import random
import time
import sys

class BingBot(object):
    """ Automatically login to Bing and search random words
    to accumulate rewards """

    def __init__(self, email, password, is_mobile=False):

        self.login_url = "https://login.live.com/"
        self.bing_url = "https://www.bing.com/"

        self.word_list = "word_list.txt"

        self.email = email
        self.password = password

        self.is_mobile = is_mobile

        self.explicit_wait = 10
        self.min_search_wait = 5
        self.max_search_wait = 20

        self.num_searches_to_perform = 32

        self.profile = self.firefox_profile()
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_profile=self.profile, firefox_options=self.options)

    def firefox_profile(self):
        """Searches on mobile as well as desktop"""
        profile = webdriver.FirefoxProfile()
        if self.is_mobile:
            profile.set_preference("general.useragent.override",
                                   "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0")
        return profile

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

    def get_rand_search_time(self):
        """Randomize time for searches"""
        return random.uniform(self.min_search_wait, self.max_search_wait)

    def get_rand_search_term(self):
        """Randomly select search term for Bing from word list"""
        total_bytes = os.stat(self.word_list).st_size
        random_point = random.randint(0, total_bytes)
        file = open(self.word_list)
        file.seek(random_point)
        file.readline()
        return file.readline()

    def bing_search(self):
        """Navigate to Bing and perform random searches."""
        self.driver.get(self.bing_url)

        wait = WebDriverWait(self.driver, self.explicit_wait)
        wait.until(EC.presence_of_all_elements_located((By.ID, "sb_form_q")))

        count = 0
        for search in range(self.num_searches_to_perform):
            sys.stdout.write('\r')
            sys.stdout.write("Searching: " + str(count) + " out of " + str(self.num_searches_to_perform))
            sys.stdout.flush()
            rand_time = self.get_rand_search_time()
            time.sleep(rand_time)

            rand_word = self.get_rand_search_term()
            self.driver.get("https://www.bing.com/search?q=" + rand_word)
            count += 1
        sys.stdout.write('\n' "Completed" + str(count) + " out of " + str(self.num_searches_to_perform) + "Searches")
        sys.stdout.flush()

    def quit(self):
        """Close the browser."""
        self.driver.close()

    def run(self):
        """Run the primary login, search, quit protocol."""
        self.login()
        self.bing_search()
        self.quit()


with open('bing_accounts.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        user_id = row[0]
        password = row[1]

        sys.stdout.write("Processing User via Desktop" '\n')
        sys.stdout.write("---------------------------" '\n')
        bing_bot = BingBot(user_id, password, is_mobile=True)
        bing_bot.run()
        sys.stdout.write('\n' '\n' "Desktop Searches Complete" '\n' '\n')

        sys.stdout.write("Processing user via Mobile" '\n')
        sys.stdout.write("--------------------------" '\n')
        bing_bot = BingBot(user_id, password)
        bing_bot.run()
        sys.stdout.write('\n' '\n' "Mobile Searches Complete" '\n' '\n')

import logging
import os
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def check_dir(param):
    return os.path.exists(param)

def create_dir(param):
    os.makedirs(param)

class LinkedInBot:
    def __init__(self, delay=5):
        if check_dir("data"):
            print("Directory exists")
        else:
            create_dir("data")
            print("Directory created")

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt, filename="data/linkedin-bot.log")
        self.delay = delay
        logging.info("Starting driver")
        self.driver = webdriver.Firefox(executable_path="driver/geckodriver.exe")

    def login(self, email, password):
        if os.path.exists("data/cookies.txt"):
            """Use the previous created cookie if the authentication has already been done"""
            self.driver.get("https://www.linkedin.com/")
            self.load_cookie("data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.doLogin(email=email, password=password)

    def doLogin(self, email, password):
        """Go to login page"""
        logging.info("Logging in")
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        self.wait()

        self.driver.find_element_by_id('username').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)

        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
        self.wait()

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def search_linkedin(self, keywords, location):
        """Enter keywords into search bar"""
        logging.info("Begin linkedin searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")
        # search based on keywords and location and hit enter
        self.wait_for_element_ready(By.CLASS_NAME, 'jobs-search-box__text-input')
        self.wait()
        search_bars = self.driver.find_elements_by_class_name('jobs-search-box__text-input')
        search_keywords = search_bars[0]
        search_keywords.send_keys(keywords)
        search_location = search_bars[3]
        search_location.send_keys(location)
        self.wait()
        search_location.send_keys(Keys.RETURN)
        logging.info("Keyword search successful")
        self.wait()

    def wait(self, t_delay=None):
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def scroll_to(self, job_list_item):
        """Scroll to the list item in the column"""
        self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
        job_list_item.click()
        self.wait()

    def get_position_data(self, job):
        """ Returns  list of strings : [position, company, location, details] """
        [position, company, location] = job.text.split('\n')[:3]
        details = self.driver.find_element_by_id("job-details").text
        return [position, company, location, details]

    def add_row_to_excel(self, position, company, location, details):
        pass

    def close_session(self):
        """This function closes the actual session"""
        logging.info("Closing session")
        self.driver.close()

    def run(self, email, password, keywords, location):
        self.login(email=email, password=password)
        self.save_cookie("data/cookies.txt")
        self.search_linkedin(keywords, location)
        self.wait()

        # only first 8 pages :
        for page in range(2, 8):
            # get the jobs list items:
            jobs = self.driver.find_elements_by_class_name("occludable-update")
            for job in jobs:
                self.scroll_to(job)
                [position, company, location, details] = self.get_position_data(job)
                self.add_row_to_excel(position, company, location, details)

            # go to next page:
            bot.driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
            bot.wait()
        logging.info("Done.")
        bot.close_session()


if __name__ == "__main__":
    email = "ermal.aliraj@gmail.com"  # your linkedin username/email
    password = "astalavista23"  # your linkedin password  (DON'T panic! No requests will be sent on your name)
    jobTitle = "Data Scientist"
    location = "Canada"

    bot = LinkedInBot()
    bot.run(email, password, jobTitle, location)

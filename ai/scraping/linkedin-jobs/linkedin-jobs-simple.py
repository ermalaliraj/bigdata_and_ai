import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def method_name(element):
    print("\n")
    # print("\nelement:", element)
    print("element.tag_name:", element.tag_name)
    # print("element.text: {0}".format(element.text))
    # print("element.get_attribute('value'): {0}".format(element.get_attribute('value')))
    print("element.get_attribute('innerHTML'): {0}".format(element.get_attribute('outerHTML')))


# direct the webdriver to where the browser file is:
driver_path = "driver/geckodriver.exe"
driver = webdriver.Firefox(executable_path=driver_path)

# your secret credentials:
email = "xxxxxx@yahoo.it"
password = "yyyyyy"
driver.get('https://www.linkedin.com/login')
time.sleep(3)

driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_id('password').send_keys(Keys.RETURN)
time.sleep(4)

# find the keywords/location search bars:
keywords = "java"
location = "Bruxelles"
driver.get("https://www.linkedin.com/jobs/")
time.sleep(3)
# search_bars = driver.find_element(By.CLASS_NAME, 'jobs-search-box__text-input')
# search_keywords = search_bars[0].click()
search_bars = driver.find_elements_by_class_name('jobs-search-box__text-input')
search_keywords = search_bars[0]
search_keywords.send_keys(keywords)
# method_name(search_bars[0])

# method_name(search_bars[3])
search_location = search_bars[3]
search_location.send_keys(location)
search_location.send_keys(Keys.RETURN)
time.sleep(3)

# get a list of all the listings elements's in the side bar
list_items = driver.find_elements_by_class_name("occludable-update")
# scrolls a single page:
for job in list_items:
    # executes JavaScript to scroll the div into view
    driver.execute_script("arguments[0].scrollIntoView();", job)
    job.click()
    time.sleep(3)
    # get info:
    [position, company, location] = job.text.split('\n')[:3]
    details = driver.find_element_by_id("job-details").text

    str = "{0} ({1}) - {2} - \n{3}".format(position, company, location, details)
    print(str)
    # do what you want with that info...

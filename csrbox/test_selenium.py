from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    num = 2
    for i in range(2) :
    # while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

chrome_options = Options()
chrome_options.add_argument('--headless')
# chrome_options.set_headless() # old style
assert chrome_options.headless

driver =webdriver.Chrome(executable_path='./csrbox/chromedriver', options=chrome_options)

driver.get('https://csrbox.org/India-list-CSR-projects-India')

scroll(driver, 5)

# source = driver.page_source
list_ = driver.find_elements_by_xpath("//a[@class = 'readmore readmorebutton']")
print(list_)

driver.close()
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options

def searchLocation(location_input):
    searchElem = browser.find_element_by_css_selector("#inputstring")
    searchElem.click()
    searchElem.send_keys(location_input)
    try:
        WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.autocomplete-suggestion:nth-child(1)")))
        searchElem.submit()
        current_url = browser.current_url
        try:
            WebDriverWait(browser, 1).until(EC.url_changes(current_url))
            print('pageloading')
            get_current_weather()
        except TimeoutException:
            print('page did not laod')
    except TimeoutException:
        try: 
            browser.find_element_by_css_selector('.autocomplete-no-suggestion')
            print('Location not found. Enter new location:')
        except NoSuchElementException:
            print('Someting went wrong. Try again:')
            

def get_current_weather():
    title = browser.find_element_by_css_selector(
        "#current-conditions > div:nth-child(1) > div:nth-child(1) > h2:nth-child(2)")
    detailed_forcast = browser.find_element_by_id('detailed-forecast-body')
    spacing = re.sub(r'\n', '\n\n', detailed_forcast.text)
    print('Weather for the next week in %s is %s' % (title.text, spacing))


location_input = input("Enter location\n")
geckdriver_path = '/Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
options = Options()
options.add_argument('-headless')
browser = Firefox(executable_path='geckodriver', options=options)
browser.get('https://www.weather.gov')

while location_input != "":
    searchLocation(location_input)
    location_input = input("Enter location (or enter to exit)\n")
         
browser.quit()        

# $PATH to geckodriver

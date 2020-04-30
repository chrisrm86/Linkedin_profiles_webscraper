#!/usr/bin/python3
# -*- coding UTF-8 -*-
"""
##########################################################

Name:       LinkedIn profiles web scraper
Created by: Christian Morán
e-mail:     christianrmoran86@gmail.com
More code:  http://github.com/chrisrm86

##########################################################
"""

""" 
Steps of this script:

1. Create an 'output.csv' file where profile data will be stored.

2. Login to LinkedIn with a username and password.

3. Perform a Google search with parameters.
 
4. View 10 LinkedIn profiles and get their data.

5. Save the data of the returned profiles in the 'output.csv' file.
"""
##########################################################

import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name', 'Position', 'Location'])

driver = webdriver.Chrome('D://chromedriver')       # Replace with the location of your Chromedriver.
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

username = driver.find_element_by_name("session_key")
username.send_keys('')                              # Here you must put your Google account associated with LinkedIn
sleep(0.5)

password = driver.find_element_by_name('session_password')
password.send_keys('')                              # Here you must put your password of your LinkedIn account
sleep(0.5)


log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()
sleep(2)

driver.get('https://www.google.com/')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/ AND "python developer jr" AND "argentina"')
search_query.send_keys(Keys.RETURN)
sleep(0.5)

urls = driver.find_elements_by_xpath('//*[@class = "r"]/a[@href]')
urls = [url.get_attribute('href') for url in urls]
sleep(0.5)

for url in urls:
    driver.get(url)
    sleep(2)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
    name = ' '.join(name)

    position = sel.xpath('//*[@class = "mt1 t-18 t-black t-normal"]/text()').extract_first().split()
    position = ' '.join(position)

    location = ' '.join(sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())
    location = ' '.join(location)

    writer.writerow([name,
                     position,
                     location])

driver.quit()
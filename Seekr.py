__author__ = 'AHusbands'

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
from twilio.rest import TwilioRestClient

#Twillio account information
account = 'AC22c3efa259776b21ac14f3b62d9cd538'
token = 'a775f0c18f090adf490a3f20ca2f15a3'
client = TwilioRestClient(account, token)

def sendTextMessage(seats):
    message = client.messages.create(to='+18135396135', from_='+15102842396', body='There are ' + seats + ' available!')

def trackCourses():
    #Check to see if certain elements are available or else refresh


    #Empty array for the data
    data = []

    #Get all rows
    for tr in browser.find_elements_by_xpath('//table[@id="results"]//tr'):
        tds = tr.find_elements_by_tag_name('td')
        if tds:
            data.append([td.text for td in tds])
        print(data, '\n')

    available_seats = data[0][10]
    print ('Seats: ' + available_seats)

    #Check to see if a seat has become available
    if (int(available_seats) == 0):
        #Refresh page
        print("No seats, refreshing!")
        browser.refresh()
        time.sleep(60)
        trackCourses()
    else:
        #Send text message
        sendTextMessage(available_seats)
        browser.quit()

def loadCourseInfo():
    #Accept Course Information
    term = input("Enter the course term (eg. Summer 2017, Fall 2017: ")
    course_CRN = input("Enter the CRN of the course you would like to track: ")

    #Website changes id's & names every day
    #Implement something to fetch


    #Better way to find elements
    #Define search criteria
    search_table = browser.find_element_by_xpath('//form[@id="frmSearch"]//table')
    search_table_body = search_table.find_element_by_tag_name('tbody')
    search_trs = search_table_body.find_elements_by_tag_name('tr')
    print(search_trs)

    new_browser_term = search_trs[1].find_element_by_tag_name('td')
    new_browser_term.select_by_visible_text((term))

    #Define search criteria

    browser_term = Select(browser.find_element_by_name('P_e11a10d92e43d8244a489505ca308485'))
    browser_term.select_by_visible_text(term)

    browser_campus = Select(browser.find_element_by_id('P_27dd574067f6f462a7e264a4559bf82e'))
    browser_campus.select_by_visible_text('Tampa')

    #Pause to let other options load
    time.sleep(1)

    browser_crn = browser.find_element_by_name('P_366b8a74c8201dc4d967ce7ba4164d97')
    browser_crn.send_keys(course_CRN)

    browser_course_status = Select(browser.find_element_by_name('P_eab714c000f37a0d0be7d27506a62e39'))
    browser_course_status.select_by_visible_text('ALL')

    send_button = browser.find_element_by_name('search')
    send_button.click()

    time.sleep(1)

    #Call second function
    trackCourses()

    return

#Create new instance of chrome browser
browser = webdriver.Chrome(executable_path='/Users/AHusbands/Downloads/chromedriver')

#Go to website
browser.get('http://www.registrar.usf.edu/ssearch/search.php')

#Let the page load
time.sleep(2)

loadCourseInfo()



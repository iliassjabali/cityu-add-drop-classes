# coding=utf-8

import data

import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decimal import Decimal, ROUND_HALF_UP


def selenium_submit():
    print(f"{data.current_time()}Getting web page source from {data.url} ...")
    data.driver.get(url=data.url)
    page = BeautifulSoup(data.driver.page_source, 'lxml').prettify()
    print(f"{data.current_time()}Got source! \n")

    if "to login AIMS." in page:
        login()

    WebDriverWait(data.driver, 10).until_not(EC.title_contains("Login"))

    for item in data.cookies:
        data.driver.add_cookie(item)

    '''
    Navigation path: 
       Personal Information -> Course Registration -> Add or Drop Classes -> Registration Term -> Add or Drop Classes
    '''
    # Click: Course Registration
    data.driver.find_elements_by_xpath("//*[contains(text(), 'Course Registration')]")[0].click()
    WebDriverWait(data.driver, 10).until(EC.title_contains("Course Registration"))

    # Click: Add or Drop Classes
    data.driver.find_elements_by_xpath("//*[contains(text(), 'Add or Drop Classes')]")[0].click()
    WebDriverWait(data.driver, 10).until(EC.title_contains("Registration Term"))

    # Click: submit
    data.driver.find_elements_by_xpath("//*[@type='submit']")[1].click()
    WebDriverWait(data.driver, 10).until(EC.title_contains("Add or Drop Classes"))

    # print("You may register during the following times:" in data.driver.page_source)

    add_classes()


def login():
    print(f"{data.current_time()}Getting login web page source from {data.login_url} ...")
    data.driver.get(data.login_url)
    login_page = BeautifulSoup(data.driver.page_source, 'lxml').prettify()
    eid_name = get_eid_field_name(login_page)
    pwd_name = "p_password"
    button_name = "input_button"
    print(f"{data.current_time()}Got login page source! \n")

    print(f"{data.current_time()}Filling login information...")
    # Fill EID
    eid_field = data.driver.find_element_by_name(eid_name)
    eid_field.clear()
    eid_field.send_keys(data.username)

    # Fill password
    pwd_field = data.driver.find_element_by_name(pwd_name)
    pwd_field.clear()
    pwd_field.send_keys(data.password)

    # Click login button
    data.driver.find_element_by_class_name(button_name).click()
    print(f"{data.current_time()}Login success! \n")

    # Store Cookie
    data.cookies = data.driver.get_cookies()


def get_eid_field_name(page) -> str:
    name = re.search(r'User\d{14}', page)[0]
    return name


def add_classes():
    data.driver.refresh()
    # crn_id1, crn_id2
    # find_element_by_id

    print("add classes")


if __name__ == "__main__":
    pass

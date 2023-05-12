# https://parkingfee.pma.gov.taipei
# get
# -*- coding: UTF-8 -*-
import requests
import random
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from validateCode import downloadValidateCode, getValidateCode
from userAgent import user_agents

headers = {
    "User-Agent": random.choice(user_agents)
}

def startCrawler(search_data_array):
    print('start crawler....')
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920x1080')
                     
    web_driver = webdriver.Chrome(chrome_options=options)
    web_driver.get("https://parkingfee.pma.gov.taipei/")

    request_session = requests.session()
    request_session.cookies.update(syncWebDriverAndRequestCookie(web_driver))

    downloadValidateCode(request_session, headers)
    validate_code = getValidateCode()

    web_driver.find_element(
        By.ID, 'FeeSearchViewModel_Captcha').send_keys(validate_code)

    for i in range(len(search_data_array)):
        car_data = search_data_array[i].split(',')
        tmp_array = np.array([car_data[0], car_data[1]])

        if car_data[1] == '汽車':
            web_driver.find_element(By.ID, 'v1').click()
        else:
            web_driver.find_element(By.ID, 'v2').click()

        car_card = car_data[0].split('-')
        web_driver.find_element(
            By.ID, 'FeeSearchViewModel_PlateNumFront').clear()
        web_driver.find_element(
            By.ID, 'FeeSearchViewModel_PlateNumFront').send_keys(car_card[0])
        web_driver.find_element(
            By.ID, 'FeeSearchViewModel_PlateNumEnd').clear()
        web_driver.find_element(
            By.ID, 'FeeSearchViewModel_PlateNumEnd').send_keys(car_card[1])

        web_driver.find_element(
            By.XPATH, '//*[@id="main"]/article[2]/div/section[2]/div/form/div/div[5]/button').click()

        try:
            results = web_driver.find_element(
                By.XPATH, '//*[@id="feeContainer"]/div[3]/ul/li/div').get_attribute('innerHTML')

            soup = BeautifulSoup(results, 'html.parser')
            bills = soup.find_all('div', class_='v_parking')

            for bill in bills:
                order_id = bill.find('p', class_="v_p_text").find('span').text
                park_date = bill.find(
                    'p', class_="v_p_deadline").find('span').text
                park_time = bill.find('p', class_="v_p_deadline mm").text.replace(
                    "\n", "").replace(" ", "").strip()
                deadline = bill.find(
                    'p', class_="v_p_deadline pay").find('span').text

                search_result = [order_id, park_date, park_time, deadline]

                result = np.concatenate(
                    (tmp_array, np.array(search_result)), axis=None)

                if 'result_data' not in dir():
                    result_data = np.reshape(result, (1, 6))
                else:
                    result_data = np.vstack([result_data, result])

        except NoSuchElementException:
            search_result = []

        web_driver.back()

    web_driver.quit()

    if 'result_data' not in dir():
        return []

    return result_data


def syncWebDriverAndRequestCookie(web_driver):
    selenium_cookies = web_driver.get_cookies()
    request_cookies_jar = requests.cookies.RequestsCookieJar()
    for i in selenium_cookies:
        request_cookies_jar.set(i['name'], i['value'],
                                domain=i['domain'], path=i['path'])

    return request_cookies_jar

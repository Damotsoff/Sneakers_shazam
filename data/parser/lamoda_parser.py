import time
import os

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import urllib.request
from random import randrange


PATH = ''

if not os.path.exists(os.path.join(PATH, 'Adidas_Stan_Smith')):
    os.mkdir(os.path.join(PATH, 'Adidas_Stan_Smith'))

if not os.path.exists(os.path.join(PATH, 'Adidas_Superstar')):
    os.mkdir(os.path.join(PATH, 'Adidas_Superstar'))

LINKS_STAN_SMITH = [
    'https://www.ebay.com/itm/283948410823',
    'https://www.ebay.com/itm/304251174112',
    'https://www.ebay.com/itm/284206189957',
    'https://www.ebay.com/itm/274760469040',
    'https://www.ebay.com/itm/294533224579',
    'https://www.ebay.com/itm/324728461775',
    'https://www.ebay.com/itm/275051038181',
    'https://www.ebay.com/itm/403330873601',
    'https://www.ebay.com/itm/263156432703',
    'https://www.ebay.com/itm/373786370366',
    'https://www.ebay.com/itm/284520267344',
    'https://www.ebay.com/itm/154731141753',
    'https://www.ebay.com/itm/313237664307',
    'https://www.ebay.com/itm/373384308607',
    'https://www.ebay.com/itm/402804200580',
    'https://www.ebay.com/itm/384566469774',
    'https://www.ebay.com/itm/233968919152',
    'https://www.ebay.com/itm/324768835628',
    'https://www.ebay.com/itm/324886570488',
    'https://www.ebay.com/itm/265435258496',
    'https://www.ebay.com/itm/403052623176',
    'https://www.ebay.com/itm/303946152100',
    'https://www.ebay.com/itm/313706999962',
    'https://www.ebay.com/itm/402975247743',
]

LINKS_SUPERSTAR = [
    'https://www.ebay.com/itm/224426949216',
    'https://www.ebay.com/itm/265423509444',
    'https://www.ebay.com/itm/234267814569',
    'https://www.ebay.com/itm/373672534331',
    'https://www.ebay.com/itm/284101546316',
    'https://www.ebay.com/itm/393632409522',
]


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate -errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(executable_path='/home/jabulani/Final_Project/data/parser/chromedriver', options=options) 


for i, url in enumerate(LINKS_STAN_SMITH):
    
    driver.get(url)    
    time.sleep(randrange(2, 4))

    actions = ActionChains(driver)


    first_photo = driver.find_element_by_id("vi_main_img_fs_thImg0")
    actions.move_to_element(first_photo).click(first_photo).perform()
    time.sleep(0.5)

    driver.find_element_by_class_name("vi-img-overlay--trans").click()
    time.sleep(randrange(1, 2))

    n = 0

    while True:   
        try:
            url = driver.find_element_by_id("viEnlargeImgLayer_img_ctr").get_attribute('src')
        except Exception as e:
            print(f"Не удалось найти изображение: {e}")
            break

        n += 1

        try:
            next_photo = driver.find_element_by_class_name("activeNext")
            actions.move_to_element(next_photo).click(next_photo).perform()
            time.sleep(0.5)
        except NoSuchElementException:
            break
        name = '_'.join(url.split('/')[-2:])
        try:
            urllib.request.urlretrieve(url, os.path.join(os.path.join(PATH, 'Adidas_Superstar'), name))
        except Exception as e:
            print(f'Не удалось загрузить фотографию: {e}')
            break
    print(f'Обработан {i + 1} башмак из {len(LINKS_STAN_SMITH)}')

driver.close()
driver.quit()
print('Готово')


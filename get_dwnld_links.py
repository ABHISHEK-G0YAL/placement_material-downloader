TIME_DELAY = 8

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(TIME_DELAY)
driver.maximize_window()

def get_links(url):
    driver.get(url)
    table_body = driver.find_element_by_xpath('//*[@id="app"]/div/section/div/div/div[2]/table/tbody')
    root = dict()
    for row in table_body.find_elements_by_tag_name('tr'):
        cols = row.find_elements_by_tag_name('td')
        name = cols[0].text
        if any(ext in name.lower() for ext in ['.png', '.jpg', 'gif']):
            continue
        buttons = cols[-1].find_elements_by_tag_name('i')
        buttons[0].click()
        link = pyperclip.paste()
        root[name] = (link, len(buttons) == 2)
        # driver.implicitly_wait(0)
        # viewer_close_bttn = driver.find_elements_by_class_name('viewer-button viewer-close')
        # if viewer_close_bttn:
        #     viewer_close_bttn[0].click()
        # driver.implicitly_wait(TIME_DELAY)
        root[name] = (link, len(buttons) == 2)
        print(name)
        print(root[name])
    return root

def traverse_web_recursive(root):
    for key in root:
        if type(root[key]) is dict:
            traverse_web_recursive(root[key])
        else:
            link, folder = root[key]
            if folder:
                links_dir = get_links(link)
                root[key] = links_dir
                traverse_web_recursive(links_dir)
    save_progress()

def save_progress():
    with open('root.json', 'w') as f:
        json.dump(root, f, indent=4)

if __name__ == '__main__':
    root = {'Placement Material': ('https://dsa.csalgo3.workers.dev/0:/', True)}
    if os.path.isfile('root.json'):
        with open('root.json') as f:
            root = json.load(f)
    traverse_web_recursive(root)
    driver.close()
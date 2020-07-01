# courtesy of aj-4 on GitHub

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os
from dotenv import load_dotenv

class Person():
    def __init__(self, bot):
        self.bot = bot
        self.name =''
        self.age=''
        self.bio=''
        #removing code to harvest images
    
    def get_info(self):
        #click expand button
        expand_btn = self.bot.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button')
        expand_btn.click()
        self.name = self.bot.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/h1').text
        self.age = self.bot.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/span').text
        self.bio = self.bot.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]').text
        
class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.current_person = None

    def start_tinder(self):
        self.driver.get('https://tinder.com')

    def login(self):
        self.driver.get('https://tinder.com')
        load_dotenv()
        USERNAME = os.getenv('USERNAME_TINDER')
        PASSWORD = os.getenv('PASSWORD_TINDER')

        time.sleep(5)

        fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
        fb_btn.click()
        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])
        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(USERNAME)
        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(PASSWORD)
        pw_in.send_keys(Keys.RETURN)
        self.driver.switch_to_window(base_window)

        time.sleep(5)
        popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        popup_1.click()

        time.sleep(1)
        popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        popup_2.click()
    
    def new_person(self):
        if self.current_person:
            del self.current_person
        self.current_person = Person(self)
        self.current_person.get_info()
    
    def swipe_left(self):
        dislike_btn = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[2]/button')
        dislike_btn.click()
    
    def swipe_right(self):                            
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[4]/button')
        like_btn.click()


#exploring on how to implement get_pictures and get_info

#pictures: can we get the picture to open from URL? if so, it's kinda broken
# info: get the relevant info by parsing lel

#expand bio

# pic = bot.driver.find_elements_by_css_selector("[aria-label='Profile slider']")
# p_list = []
# for p in pic:
#     att = p.get_attribute('style')
#     att = att.split('"')
#     p_list.append(att[1])


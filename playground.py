import time
import scrapy
from scrapy import Spider
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess

from selenium import webdriver 

class FBCrawler(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver")

    def login_facebook(self, email, passw):
        self.driver.get('https://www.facebook.com/') 
        print ("Opened facebook") 
        time.sleep(1) 
          
        username_box = self.driver.find_element_by_id('email') 
        username_box.send_keys(email) 
        print ("Email Id entered") 
        time.sleep(1) 
          
        password_box = self.driver.find_element_by_id('pass') 
        password_box.send_keys(passw) 
        print ("Password entered") 
          
        login_box = self.driver.find_element_by_id('loginbutton') 
        login_box.click() 
          
        print ("Done") 
        input('Press anything to continue') 

        profile = self.driver.find_element_by_xpath('//*[@title="Perfil"]')
        profile.click()

        input('Press anything to quit') 

        self.driver.quit() 
        print("Finished")


def main():
    crawler = FBCrawler()
    crawler.login_facebook("parnibanda@yahoo.com.mx", "Perrita1")

main()

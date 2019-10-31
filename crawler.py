import time
import scrapy
from scrapy import Spider
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess

from selenium import webdriver 


    
    

class FBCrawler(object):
    def __init__(self, driver, email, passw):
        self.driver = driver
        self.email = email
        self.passw = passw

    def friends_links(self):
        self.login_facebook()
        links_list = self.crawl_friends()

        all_htmls = []
        #for link in links_list:
            #all_htmls.append(self.obtain_friend_data(link))
        # Solo hace 3
        for i in range(5):
            all_htmls.append(self.obtain_friend_data(links_list[i]))
        
        #print(all_htmls[0])

        with open("htmltest1.txt","w") as writer:
            writer.write(all_htmls[0])

        with open("htmltest2.txt","w") as writer:
            writer.write(all_htmls[1])
        with open("htmltest3.txt","w") as writer:
            writer.write(all_htmls[2])
        with open("htmltest4.txt","w") as writer:
            writer.write(all_htmls[3])


        return all_htmls

    def login_facebook(self):
        self.driver.get('https://www.facebook.com/') 
        print("Opened facebook") 
        time.sleep(1) 
          
        username_box = self.driver.find_element_by_id('email') 
        username_box.send_keys(self.email) 
          
        password_box = self.driver.find_element_by_id('pass') 
        password_box.send_keys(self.passw) 
          
        login_box = self.driver.find_element_by_id('loginbutton') 
        login_box.click() 
          
        print("Loged to facebook") 
        time.sleep(2) 

    def crawl_friends(self):
        profile = self.driver.find_element_by_xpath('//*[@title="Perfil"]')
        profile.click()

        time.sleep(1) 

        user_link = self.driver.current_url
        self.driver.get(user_link+"/friends")

        time.sleep(3) 

        self.scroll_to_bottom()

        #friends_list_item = self.driver.find_elements_by_xpath('//div[@data-testid="friend_list_item"]')
        friends_links = self.driver.find_elements_by_xpath('//*[@class="_5q6s _8o _8t lfloat _ohe"]')
        #friends_list_item = self.driver.find_elements_by_xpath('//*[@class="_698"]')
        print(len(friends_links))
        print(type(friends_links[0]))

        friends_list = []

        for friend_link in friends_links:
            try:
                link = friend_link.get_attribute("href")
                print(link)
                friends_list.append(link)
            except:
                pass

        print("total friends: {}".format(len(friends_list)))

        return friends_list

    def scroll_to_bottom(self):
        size = 0
        while size != len(self.driver.page_source):
            size = len(self.driver.page_source)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

    def obtain_friend_data(self, link):
        self.driver.get(link)
        about = self.driver.find_element_by_xpath('//*[@data-tab-key="about"]')
        about.click()
        time.sleep(2
        )

        return self.driver.page_source
   

def main():
    #email = input("Email:")
    #passw = input("Password:")
    placeList = []
    email = "superdiegoshowdown@gmail.com"
    passw = "kinect2401"
    driver = webdriver.Chrome(executable_path="./chromedriver")
    crawler = FBCrawler(driver, email, passw)

    friends_data = crawler.friends_links()

    
    #for i in friends_data:
        #placeList[i] = extractor()
    
    #for j in placeList:
        #print(placeList[j])

    
    
    input("Enter to end")
    driver.quit()

main()

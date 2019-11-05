import time
from matplotlib import pyplot as plt
import scrapy
from scrapy import Spider
from scrapy.utils.response import open_in_browser
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
from selenium import webdriver 

def extractor(testLines):
    
    
    x = -1
    z = 0
    #testLines = []
    #txtTestR_file = open(path,'r') #ABRE EL ARCHIVO ESPESIFICADO EN EL "path"
   
    line = []
    #testLines = txtTestR_file.readlines() #DIVIDE EL HTML EN LINAS DE CODIGO 
    #testLines = html.readlines() #DIVIDE EL HTML EN LINAS DE CODIGO 

    x = testLines.find("Vive en ")       #CHECA EN CADA LINEA SI ESTA LA SUBCADENA DESEADA Y REGRESA EL IDICE DINDE SE ENCUENTRA

    if x == -1:
        print ("")
        print ("chale")
        print ("")

        return "NoData"
    #for i in range (len(testLines)):    #ITERA DESDE LA PRIMERA LINEA HASTA LA ULTIMA DEL HTML
        #line = testLines[i]              # OBTIENE LA PRIMERA LINEA DEL HTML    
    #print("------->")
    #print(testLines[i])
    if x > -1:                      #SI LA ENCUENTRA DETIENE LA BUSQUEDA
        
        #print("el indice donde esta -Vive en- es:" )
        #print(x)
        #print("")
        z = testLines.find(">",x,len(testLines)) #BUSCA A PARTIR DEL INDICE vive en HASTA ENTCONTRAR UN '>'
        #print("")
        #print("el indice donde esta la ciudad es:" )
        #print(z)
        #print("")
            #break
        

   
    
            
    w = []
    j=1
    places = []
    place = ''


    while  w != "<":
        #EN EL HTML DE GIL "VIVE EN ESTA EN LA POS 196,048 DE LA LINEA 103"
        w = testLines[z+j]
        place += w
        #print (w)
        j += 1
        places.append(place)

    place = place.replace("<","")
    print(place) 
    return place


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
        for i in range(100):
            all_htmls.append(self.obtain_friend_data(links_list[i]))
            time.sleep(4) 
    
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

        time.sleep(4) 

        self.scroll_to_bottom()
        time.sleep(4) 

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
        time.sleep(4) 

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
        time.sleep(2)

        return self.driver.page_source
   

def main():
    email = input("Email:")
    passw = input("Password:")
    placeList = []
    driver = webdriver.Chrome(executable_path="./chromedriver")
    crawler = FBCrawler(driver, email, passw)

    friends_data = crawler.friends_links()

    
    #///////////////////////////////////////////////

    d_all_htmls = []
    d_all_places = []
    places_dict = {}

    for f in range (len(friends_data)):
        key = extractor(friends_data[f])
        if not key in places_dict:
            places_dict[key] = 1
        else:
            places_dict[key] += 1
        d_all_places.append(key)
   
    #print("hola")
    #print(d_all_htmls[0])
    print("")
    print("ciudades:")
   
    for a in range (len(d_all_places)):
        print(d_all_places[a])
    
    print("")
    print(places_dict)
    
    #print("hola")
    #print(len(testLines))
    #print(len(d_all_htmls))

    #///////////////////////////////////////////////////////////////////
    print("Creating PIE Chart")
    labels = []
    sizes = []
    for k in places_dict:
        labels.append(k)
        sizes.append(places_dict[k])

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.savefig("pie.png")

    
    
    input("Enter to end")
    driver.quit()

main()

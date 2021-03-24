from selenium import webdriver
from time import sleep
import json, time, random
from selenium.common.exceptions import NoSuchElementException

from secrets import ebay_email, ebay_password
from details import keywords, excluded_words, price_maximum

class eBayBot():

    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://www.ebay.com.au/sch/ebayadvsearch')
        sleep(2)

        signin_link = self.driver.find_element_by_xpath('//*[@id="gh-ug"]/a')
        signin_link.click()
        sleep(2)

        signin_email = self.driver.find_element_by_xpath('//*[@id="userid"]')
        signin_email.send_keys(ebay_email)
        sleep(2)

        continue_button = self.driver.find_element_by_xpath('//*[@id="signin-continue-btn"]')
        continue_button.click()
        sleep(2)

        password_field = self.driver.find_element_by_xpath('//*[@id="pass"]')
        password_field.send_keys(ebay_password)
        sleep(2)

        signin_button = self.driver.find_element_by_xpath('//*[@id="sgnBt"]')
        signin_button.click()
        sleep(2)


    def fill_advanced_options(self):

        keywords_input = self.driver.find_element_by_xpath('//*[@id="_nkw"]')
        for x in keywords:
            keywords_input.send_keys(x + ' ')
        sleep(2)

        excluded_words_input = self.driver.find_element_by_xpath('//*[@id="_ex_kw"]')
        for x in excluded_words:
            excluded_words_input.send_keys(x + ' ')
        sleep(2)

        camera_dropdown_option = self.driver.find_element_by_xpath('//*[@id="e1-1"]/option[7]')
        camera_dropdown_option.click()
        sleep(2)

        search_including = self.driver.find_element_by_xpath('//*[@id="LH_TitleDesc"]')
        search_including.click()
        sleep(2)

        price_checkbox = self.driver.find_element_by_xpath('//*[@id="_mPrRngCbx"]')
        price_checkbox.click()
        sleep(2)

        price_max = self.driver.find_element_by_xpath('//*[@id="adv_search_from"]/fieldset[3]/input[3]')
        price_max.send_keys(price_maximum)
        sleep(2)

        location_preferred_radio = self.driver.find_element_by_xpath('//*[@id="LH_PrefLocRadio"]')
        location_preferred_radio.click()
        sleep(2)

        location_preferred_dropdown = self.driver.find_element_by_xpath('//*[@id="_sargnSelect"]/option[2]')
        location_preferred_dropdown.click()
        sleep(2)

        sort_by_dropdown = self.driver.find_element_by_xpath('//*[@id="LH_SORT_BY"]/option[2]')
        sort_by_dropdown.click()
        sleep(2)
    

    def search_advanced_options(self):
        search_button = self.driver.find_element_by_xpath('//*[@id="searchBtnLowerLnk"]')
        search_button.click()
        sleep(2)
    

    def clear_advanced_options(self):
        clear_options_anchor = self.driver.find_element_by_xpath('//*[@id="adv_search_from"]/div[3]/a')
        clear_options_anchor.click()
        sleep(2)

    
    def find_new_item(self):
        top_item_li = self.driver.find_element_by_xpath('//*[@r="1"]')
        top_item_id = top_item_li.get_attribute("id")

        top_item_match = False
        with open('itemid.json', 'r') as json_file:
            data = json.load(json_file)
            if data['itemid'] != top_item_id:
                try: 
                    watch_list_button = self.driver.find_element_by_xpath('//*[@id="' + top_item_id + '"]/ul[1]/li[@class="lvextras"]/div[@class="anchors"]/div/div/a')
                    watch_list_button.click()
                    top_item_match = True
                except NoSuchElementException:
                    top_item_match = True
        
        if top_item_match:
            with open('itemid.json', 'w') as json_file:
                data = {'itemid' : top_item_id}
                json.dump(data, json_file)


bot = eBayBot()
bot.login()
bot.fill_advanced_options()
bot.search_advanced_options()
try:
    while True:
        bot.find_new_item()
        time.sleep(random.randint(60, 120))
        bot.driver.refresh()
except KeyboardInterrupt:
    print('Stopping script')
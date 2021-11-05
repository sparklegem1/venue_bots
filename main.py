from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
import time





show_info = {'knuckleheads': [],
             'riotroom': []
             }



class KnuckleHeadScraper:


    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.show_info = show_info['knuckleheads']


    def find_price(self, show):
        # where show is the object in shows
        self.driver.get('https://knuckleheadskc.com/')
        time.sleep(5)

        upcoming_shows = self.driver.find_element_by_xpath('//*[@id="navTopLevel"]/li[2]/a')
        upcoming_shows.click()
        time.sleep(5)

        all_shows = self.driver.find_elements_by_class_name('pl-item')
        for element in all_shows[:11]:
            print(element.find_element_by_class_name('pl-event-link').text)
            print(show['title'])
            if show['price'] != 'Not Free':
                print('this event is free')
                return {'msg': 'this event is free'}
            if element.find_element_by_class_name('pl-event-link').text == show['title']:
                try:
                    price_button = element.find_element_by_class_name('buy-tickets')
                    price_button.click()
                    time.sleep(2)
                    self.driver.get(self.driver.current_url)
                    price = self.driver.find_element_by_class_name('price-cell').text
                    print(price)
                    return {'price': price}
                except NoSuchElementException:
                    print('no price available or third-party ticketing')
                    return {'msg': 'this event likely is priced through third party ticketing'}


    def get_shows(self):
        import time


        self.driver.get('https://knuckleheadskc.com/')
        time.sleep(5)

        upcoming_shows = self.driver.find_element_by_xpath('//*[@id="navTopLevel"]/li[2]/a')
        upcoming_shows.click()
        time.sleep(5)


        all_shows = self.driver.find_elements_by_class_name('pl-item')

        for element in all_shows[:11]:
            individual_show = {}
            title = element.find_element_by_class_name('pl-event-link').text
            print(title)
            date = f"{element.find_element_by_class_name('pl-weekday').text}/" \
                   f"{element.find_element_by_class_name('pl-monthday').text}/" \
                   f"{element.find_element_by_class_name('pl-month').text}"
            try:
                time = element.find_element_by_class_name('show-end-time-0').text

            except NoSuchElementException:
                time = 'no time available'

            try:
                price = element.find_element_by_class_name('pl-sale-status').text

            except NoSuchElementException:
                # import time
                price = element.find_element_by_class_name('buy-tickets').text


            individual_show['title'] = title
            individual_show['date'] = date
            individual_show['time'] = time
            if price == 'BUY TICKETS':
                price = 'Not Free'
            individual_show['price'] = price
            show_info['knuckleheads'].append(individual_show)
        print(show_info)



class RiotRoomScraper:

    response = requests.get('https://theriotroom.com/')
    soup = BeautifulSoup(response.text, 'html.parser')

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.show_info = show_info['riotroom']

    #####Selenium######
    def get_shows(self):

        self.driver.get('https://theriotroom.com/')
        time.sleep(2)

        all_shows = self.driver.find_elements_by_class_name('type-tribe_events')

        for show in all_shows[:11]:
            date_and_time = {'date': '', 'title': '', 'price': ''}
            try:
                date = show.find_element_by_class_name('singleEventDate').text
            except NoSuchElementException:
                date = 'no date available'
            event_time = show.find_element_by_tag_name('span').text.strip('Show| //Doors | ')[:6]
            try:
                title = show.find_element_by_tag_name('h2').text
            except NoSuchElementException:
                title = 'no available title'
            try:
                cost = show.find_element_by_class_name('eventCost').text
            except NoSuchElementException:
                cost = 'free'

            date_and_time['date'] = date

            if event_time[:2] != 'Sh':
                date_and_time['time'] = event_time
            else:
                date_and_time['time'] = 'No time available'
            date_and_time['title'] = title
            date_and_time['price'] = cost
            self.show_info.append(date_and_time)
            print('------------------------------------')
            print(date)
            print(event_time)
            print(title)
            print(cost)
            print(date_and_time)
            print('------------------------------------')


knucklehead = KnuckleHeadScraper()
knucklehead.get_shows()





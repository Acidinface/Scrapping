import time
from selenium import webdriver

website = 'https://www.audible.co.uk/search'

driver = webdriver.Chrome()
driver.get(website)
main_list = driver.find_element(by='xpath', value="//div[contains(@class, 'adbl-impression-container')]//ul[contains(@class, 'bc-list')]")
list_of_books = main_list.find_elements(by='xpath', value='//li[contains(@class, "bc-list-item")]')
# print(main_list.text)
for book in list_of_books:
    print(book.text)
time.sleep(300)
driver.close()
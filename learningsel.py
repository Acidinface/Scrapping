from selenium import webdriver

website = 'https://www.audible.co.uk/search'

driver = webdriver.Chrome()
response = driver.get(website)

list_of_books = response.find_element()

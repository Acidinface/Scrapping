from selenium import webdriver

website = 'https://www.adamchoi.co.uk/overs/detailed'
driver_path = r'Users/Scrapping/chromedriver-win64/chromedriver'

driver = webdriver.Chrome(driver_path)
response = driver.get(website)



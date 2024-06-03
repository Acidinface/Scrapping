import pandas as pd
from selenium import webdriver

column_names = ['Name', 'Author', 'Narrator', 'Length', 'Release', 'Languege', 'Rating', 'Most_popular', 'Trending', 'Price']
df = pd.DataFrame(columns=column_names)

website = 'https://www.audible.co.uk/search'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get(website)
number_of_pages = int(driver.find_elements(by='xpath', value='//ul[contains(@class, "pagingElements")]/li')[-2].text)
for page in range(number_of_pages+1):
    driver.get(f'https://www.audible.co.uk/search?page={page}')
    book_list = driver.find_elements(by='xpath', value="//li[contains(@class, 'productListItem')]")
    for i, book in enumerate(book_list):
        name = book.get_attribute('aria-label')
        author = book.find_element(by='xpath', value='//li[contains(@class, "authorLabel")]').text[4:]
        narrator = book.find_element(by='xpath', value='//li[contains(@class, "narratorLabel")]').text[13:]
        length = book.find_element(by='xpath', value='//li[contains(@class, "runtimeLabel")]').text[8:]
        release = book.find_element(by='xpath', value='//li[contains(@class, "releaseDateLabel")]').text[14:]
        languege = book.find_element(by='xpath', value='//li[contains(@class, "languageLabel")]').text[10:]
        rating = book.find_element(by='xpath', value='//li[contains(@class, "ratingsLabel")]').text
        most_popular = bool(book.find_element(by='xpath', value='//li[contains(@class, "mostPopularLabel")]').text)
        trending = bool(book.find_element(by='xpath', value='//li[contains(@class, "trendingLabel")]').text)
        price = book.find_element(by='xpath', value='//p[@id="buybox-regular-price-0"]/span[2]').text
        df.loc[len(df)] = [name, author, narrator, length, release, languege, rating, most_popular, trending, price]
driver.close()

df.to_csv('audible_parse.csv', index=False)
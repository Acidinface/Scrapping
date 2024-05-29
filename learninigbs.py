import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

movies_urls = []
website = f'https://subslikescript.com/movies'
html = requests.get(website).text
soup = BeautifulSoup(html, 'lxml')
pages = soup.find_all('li', class_='page-item')
pages = pages[-2]

for page in tqdm(range(1, int(pages.text)+1)):
    website = f'https://subslikescript.com/movies/?page={page}'
    html = requests.get(website).text
    soup = BeautifulSoup(html, 'lxml')

    list_of_movies = soup.find('ul', class_='scripts-list')
    movies = list_of_movies.find_all('a', href=True)

for movie in movies:
    movies_urls.append('https://subslikescript.com/' + movie['href'])
    

for movie in movies_urls:
    html = requests.get(movie).content
    soup = BeautifulSoup(html, 'lxml')
    main_article = soup.find('article')
    try:
        title = main_article.find('h1').get_text(strip=True).replace(' - full transcript', '')
    except AttributeError:
        title = '__No title found!__'
    try:
        plot = main_article.find('p').get_text(strip=True)
    except AttributeError:
        plot = '__Plot description missing!__'
    try:
        transcription = main_article.find('div').get_text(strip=True)
    except AttributeError:
        transcription = '__No transcription found!__'
    print('\n','='*len(title),'\n', title, '\n', '='*len(title), '\n'*2, plot, '\n')#, transcription, '\n')

    
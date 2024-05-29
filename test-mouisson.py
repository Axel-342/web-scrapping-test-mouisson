import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    quotes = []
    for quote in soup.select('div.quote'):
        text = quote.find('span', class_='text').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
        
        quotes.append({
            'text': text,
            'tags': tags
        })
    
    return quotes

urls = [
    "https://quotes.toscrape.com/page/1/",
    "https://quotes.toscrape.com/page/2/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/4/",
    "https://quotes.toscrape.com/page/5/"
]

desired_tags = {'love', 'inspirational', 'life', 'humor'}

filtered_quotes = []
for url in urls:
    quotes = scrape_page(url)
    for quote in quotes:
        if desired_tags.intersection(quote['tags']):
            filtered_quotes.append(quote)

df_quotes = pd.DataFrame(filtered_quotes, columns=['text', 'tags'])
print(df_quotes)

df_quotes.to_csv('results.csv', index=False)
print("Les citations filtrées ont été écrites dans 'results.csv'.")

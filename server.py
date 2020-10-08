import requests
from bs4 import BeautifulSoup

def get_soup(url):
    print('loading coding love random from', url)
    response = requests.get(url)
    return BeautifulSoup(response.content, features="html.parser")


the_coding_love_random_url = "https://thecodinglove.com/tag/random"
soup = get_soup(the_coding_love_random_url)


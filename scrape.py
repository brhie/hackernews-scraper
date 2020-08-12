import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')

soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['vote'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.get_text()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].get_text().replace(' points', ''))
            if points >= 100:
                hn.append({'title': title, 'link': href, 'vote': points})

    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links, subtext))

result = create_custom_hn(links, subtext)

with open('news.txt', mode='w') as file:
    for news in result:
        file.write(f"{news['title']}({news['link']})\n")
import requests
import base64
import csv
from bs4 import BeautifulSoup

# main page
all_actors = []
r = requests.get(
    'https://starngage.com/app/global/influencer/ranking/india'
).text
soup = BeautifulSoup(r, 'html.parser')

# loop via all accounts
humans_table = soup.find('table', {'class': 'table-hover'})
table_rows = humans_table.find_all('tr')

for row in table_rows:
    columns = row.find_all('td')
    if columns:
        # link to full page
        full_page = columns[2].find('a')['href']

        # send request
        profile = requests.get(full_page).text
        profile_soup = BeautifulSoup(profile, 'html.parser')

        # get extra data
        card_body = profile_soup.find('div', {'class': 'card-body'})
        flex_columns = card_body.find_all('div', {'class': 'd-flex'})

        # get profile picture
        profile_picture = requests.get(columns[1].find('img')['src'])

        profile_picture_b64 = ("data:" +
                               profile_picture.headers['Content-Type'] + ";" +
                               "base64," +
                               base64.b64encode(
                                   profile_picture.content
                               ).decode('utf-8'))

        # create actor
        actor = {
            'username': columns[2].find('a').text,
            #'age': flex_columns[2].text,
            'bio': card_body.find('div', {'class': 'text-secondary'}).text,
            'following_count': columns[5].text,
            'engagement_rate': columns[6].text,
            'avg_likes': profile_soup.find('div', {
                'class': 'avg-likes'
            }).find('div', {
                'class': 'text-number'
            }).text,
            'avg_comments': profile_soup.find('div', {
                'class': 'avg-comments'
            }).find('div', {
                'class': 'text-number'
            }).text,
            'total_posts': profile_soup.find('div', {
                'class': 'posts'
            }).find('div', {
                'class': 'text-number'
            }).text,
            'profile_pic_url': columns[1].find('img')['src'],
            'profile_picture': profile_picture_b64
        }

        # append to actors list
        all_actors.append(actor)

# write data to csv file
fieldnames = [
    'username', 'age', 'bio', 'following_count', 'engagement_rate',
    'avg_likes', 'avg_comments', 'total_posts', 'profile_pic_url',
    'profile_picture'
]
with open('result.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_actors)

print(result.csv)
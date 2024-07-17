#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

def fetch_and_save_movies():

    url = 'http://www.cgv.co.kr/movies/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    titles = soup.find('div', class_='wrap-movie-chart')
    titless = titles.find_all('strong', class_='title')
    title_name = [title.text for title in titless]

    box = soup.find('div', class_='sect-movie-chart')
    percent = box.find_all('strong', class_='percent')
    percent_list = [per.text[3:] for per in percent]

    dates = box.find_all('span', class_='txt-info')
    dates_list = [date.text.strip()[:10] for date in dates]

    movie_df = pd.DataFrame({
        "영화 제목": title_name,
        "예매율": percent_list,
        "개봉일": dates_list
    })

    top_10_movies = movie_df.head(10).reset_index(drop=True)
    top_10_movies.index += 1

    file_path = r'/Users/chosoobin/be04-4th-6team-CINE-VERSE/be04-4th-6team-CINE-VERSE-FRONT/CINEVERSE_FRONT/cine-verse/public/top_10_movies.json'
    top_10_movies.to_json(file_path, force_ascii=False, orient='index', indent=2)

    print(f"파일이 저장되었습니다: {file_path}")

schedule.every(1).hours.do(fetch_and_save_movies)

fetch_and_save_movies()

while True:
    schedule.run_pending()
    time.sleep(1)

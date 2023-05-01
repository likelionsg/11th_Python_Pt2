from bs4 import BeautifulSoup
import requests
import sys


def build(soup):
    weather_info = {}  # 딕셔너리 초기화. 여기에 크롤링 정보 저장할 것.

    lowest_temp_str = soup.find('span', class_='lowest').text.strip()
    final_lowest = int(''.join(c for c in lowest_temp_str if c.isdecimal()))
    weather_info['lowest_temp'] = final_lowest

    highest_temp_str = soup.find('span', class_='highest').text.strip()
    final_highest = int(''.join(c for c in highest_temp_str if c.isdecimal()))
    weather_info['highest_temp'] = final_highest

    temp_text = soup.select_one('.temperature_text strong').text
    temperature = float(''.join(c for c in temp_text if c.isdigit() or c == '.'))
    weather_info['temperature'] = temperature

    weather_summary = soup.select_one('p.summary').text.strip().split()
    weather = weather_summary[-1]
    comparison = ' '.join(weather_summary[:3])
    weather_info['temp_comparison'] = comparison
    weather_info['weather'] = weather

    for item in soup.select('li.item_today')[:2]:
        title = item.select_one('strong.title').text.strip()
        status = item.select_one('span.txt').text.strip()
        weather_info[title] = status

    return weather_info


def store_message(weather_info):
    weather_str = (
        f'오늘의 대흥 날씨 정보입니다!\n\n'
        f'현재온도 {weather_info["temperature"]}도'
        f'({weather_info["temp_comparison"]})\n'
        f'날씨는 {weather_info["weather"]}입니다.\n'
        f'최저기온은 {weather_info["lowest_temp"]}도, '
        f'최고기온은 {weather_info["highest_temp"]}도이며\n'
        f'미세먼지 농도는 {weather_info["미세먼지"]},\n'
        f'초미세먼지 농도는 {weather_info["초미세먼지"]}입니다.\n'
    )

    return weather_str

def crawl_and_store_message():
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%8C%80%ED%9D%A5+%EB%82%A0%EC%94%A8'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_info = build(soup)
        return store_message(weather_info)
    else:
        return f"Error {response.status_code}"

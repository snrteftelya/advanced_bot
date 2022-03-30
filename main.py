from bs4 import BeautifulSoup
import requests
import json
import time


def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/all_news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item lenta_item")

    news_dict = {}
    date = time.strftime("%d" + ' ' + "%B" + ' ' + "%Y" + ' ')

    for article in articles_cards:
        article_title = article.find("span", class_="lenta_item_title").text.strip()
        article_url = article.find_all("a")[1].get("href")
        article_time = article.find(class_="date").text.strip()[0:5]
        article_topic = article.find(class_="date").text.strip()[22::]

        rep = ' '
        for item in rep:
            if item in article_topic:
                article_topic = article_topic.replace(item, "_")
        print(article_topic)

        article_id = article_url.split("-")[-2]

        # print(f"\n | {article_title}\n | {article_desc}\n | https://www.belta.by{article_url}\n | {article_time}\n | {article_topic}\n")

        news_dict[article_id] = {
            "date_time": date,
            "article_time": article_time,
            "article_topic": article_topic,
            "article_title": article_title,
            "article_url": f'https://www.belta.by{article_url}'
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/all_news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item lenta_item")

    fresh_news = {}

    date = time.strftime("%d" + ' ' + "%B" + ' ' + "%Y" + ' ')


    for article in articles_cards:
        article_url = article.find_all("a")[1].get("href")
        article_id = article_url.split("-")[-2]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("span", class_="lenta_item_title").text.strip()
            article_time = article.find(class_="date").text.strip()[0:5]
            article_topic = article.find(class_="date").text.strip()[22::]
            rep = ' '
            for item in rep:
                if item in article_topic:
                    article_topic = article_topic.replace(item, "_")

            news_dict[article_id] = {
                "date_time": date,
                "article_time": article_time,
                "article_topic": article_topic,
                "article_title": article_title,
                "article_url": f'https://www.belta.by{article_url}'
            }

            fresh_news[article_id] = {
                "date_time": date,
                "article_time": article_time,
                "article_topic": article_topic,
                "article_title": article_title,
                "article_url": f'https://www.belta.by{article_url}'
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def sport_class():
    sport_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Спорт":
                    sport_news_keys.append(dictionary)
    return sport_news_keys


def world_class():
    world_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "В_мире":
                    world_news_keys.append(dictionary)
    return world_news_keys


def society_class():
    society_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Общество":
                    society_news_keys.append(dictionary)
    return society_news_keys

def economy_class():
    economy_news_keys = []

    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Экономика":
                    economy_news_keys.append(dictionary)
    return economy_news_keys

def politics_class():
    politics_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Политика":
                    politics_news_keys.append(dictionary)
    return politics_news_keys

def regions_class():
    regions_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Регионы":
                    regions_news_keys.append(dictionary)
    return regions_news_keys

def accident_class():
    accident_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Происшествия":
                    accident_news_keys.append(dictionary)
    return accident_news_keys

def president_class():
    president_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Президент":
                    president_news_keys.append(dictionary)
    return president_news_keys

def kaleidoscope_class():
    kaleidoscope_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Калейдоскоп":
                    kaleidoscope_news_keys.append(dictionary)
    return kaleidoscope_news_keys

def technological_class():
    technological_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Технологии":
                    technological_news_keys.append(dictionary)
    return technological_news_keys

def cultural_class():
    cultural_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Культура":
                    cultural_news_keys.append(dictionary)
    return cultural_news_keys

def playbill_class():
    playbill_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Афиша":
                    playbill_news_keys.append(dictionary)
    return playbill_news_keys

def comments_class():
    comments_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Комментарии":
                    comments_news_keys.append(dictionary)
    return comments_news_keys

def interview_class():
    interview_news_keys = []
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        for dictionary in news_dict:
            nested_dictionary = news_dict[dictionary]
            for elements in dictionary:
                element = nested_dictionary['article_topic']
                if element == "Интервью":
                    interview_news_keys.append(dictionary)
    return interview_news_keys

def mix_class():
    mix_news_keys = []
    if len(sport_class()) >0:
        mix_news_keys.append(sport_class()[-1])
    if len(world_class()) > 0:
        mix_news_keys.append(world_class()[-1])
    if len(society_class()) >0:
        mix_news_keys.append(society_class()[-1])
    if len(economy_class()) > 0:
        mix_news_keys.append(economy_class()[-1])
    if len(politics_class()) > 0:
        mix_news_keys.append(politics_class()[-1])
    if len(regions_class()) > 0:
        mix_news_keys.append(regions_class()[-1])
    if len(accident_class()) > 0:
        mix_news_keys.append(accident_class()[-1])
    if len(president_class()) > 0:
        mix_news_keys.append(president_class()[-1])
    if len(kaleidoscope_class()) > 0:
        mix_news_keys.append(kaleidoscope_class()[-1])
    if len(technological_class()) > 0:
        mix_news_keys.append(technological_class()[-1])
    if len(cultural_class()) > 0:
        mix_news_keys.append(cultural_class()[-1])
    if len(playbill_class()) > 0:
        mix_news_keys.append(playbill_class()[-1])
    if len(comments_class()) > 0:
        mix_news_keys.append(comments_class()[-1])
    if len(interview_class()) > 0:
        mix_news_keys.append(interview_class()[-1])
    return mix_news_keys





def main():
    #get_first_news()
    check_news_update()
    sport_class()
    world_class()
    society_class()
    economy_class()
    politics_class()
    regions_class()
    accident_class()
    president_class()
    kaleidoscope_class()
    technological_class()
    cultural_class()
    playbill_class()
    comments_class()
    interview_class()
    mix_class()




if __name__ == '__main__':
    main()

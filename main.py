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
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    }
    url = "https://www.belta.by/sport/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards


def world_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/world"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards


def society_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    }

    url = "https://www.belta.by/society/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def economy_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/economics/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def politics_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    }

    url = "https://www.belta.by/politics/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def regions_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/regions/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def accident_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    }

    url = "https://www.belta.by/incident/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def president_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/president/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def kaleidoscope_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    }

    url = "https://www.belta.by/kaleidoscope/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def technological_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    url = "https://www.belta.by/tech/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards

def cultural_class():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    }

    url = "https://www.belta.by/culture/"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all(class_="news_item")
    return articles_cards






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




if __name__ == '__main__':
    main()

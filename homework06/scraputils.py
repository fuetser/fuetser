import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    titles = parser.findAll("span", class_="titleline")
    subtexts = parser.findAll("span", class_="subline")
    for title, subtext in zip(titles, subtexts):
        news_list.append(form_record(title, subtext))
    return news_list


def form_record(title, subtext):
    main_link = title.find("a")
    subtext_links = subtext.findAll("a")
    record = {
        "title": main_link.text,
        "url": main_link["href"],
        "points": subtext.find("span", class_="score").text.split()[0],
        "author": subtext_links[0].text,
        "comments": subtext_links[-1].text.split()[0],
    }
    if record["comments"] == "discuss":
        record["comments"] = 0
    return record


def extract_next_page(parser):
    """Extract next page URL"""
    return parser.find("a", class_="morelink")["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News
from scraputils import get_news


@route("/")
def index():
    redirect("/news")


@route("/news")
def news_list():
    rows = News.get()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    News.add_label(request.query["id"], request.query["label"])
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest")
    News.add_many(news)
    redirect("/news")


@route("/classify")
def classify_news():
    model = NaiveBayesClassifier(alpha=1)
    x, y = [], []
    for record in News.get_labeled():
        x.append(record.title)
        y.append(record.label)
    model.fit(x, y)
    not_labeled = News.get()
    titles = [record.title for record in not_labeled]
    predictions = model.predict(titles)
    good, maybe, never = [], [], []
    for i in range(len(titles)):
        if predictions[i] == "good":
            good.append(not_labeled[i])
        elif predictions[i] == "maybe":
            maybe.append(not_labeled[i])
        elif predictions[i] == "never":
            never.append(not_labeled[i])
    return template("news_template", rows=good + maybe + never)


if __name__ == "__main__":
    run(host="localhost", port=8080)

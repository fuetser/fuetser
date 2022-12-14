from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

    @staticmethod
    def add_many(records):
        s = session()
        for record in records:
            if (
                s.query(News)
                .filter(
                    News.title == record["title"],
                    News.author == record["author"],
                )
                .first()
                is None
            ):
                s.add(News(**record))
        s.commit()

    @staticmethod
    def get(count=30):
        s = session()
        return s.query(News).filter(News.label == None).limit(count).all()

    @staticmethod
    def get_labeled():
        s = session()
        return s.query(News).filter(News.label != None).all()

    @staticmethod
    def add_label(news_id, label):
        s = session()
        record = s.query(News).get(news_id)
        record.label = label
        s.commit()


Base.metadata.create_all(bind=engine)

import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from scrapy.exceptions import DropItem

Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'mondaypost'
    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    date = Column(Date)
    text = Column(Text)


class MondayPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        date_example = item['date']
        post_date = dt.datetime.strptime(date_example, '%d.%m.%Y')
        if post_date.weekday() == 0:
            monday_post = MondayPost(
                author=item['author'],
                date=post_date,
                text=item['text']
            )
            self.session.add(monday_post)
            self.session.commit()
            return item
        else:
            raise DropItem("Этотъ постъ написанъ не въ понедѣльникъ")

    def close_spider(self, spider):
        self.session.close()

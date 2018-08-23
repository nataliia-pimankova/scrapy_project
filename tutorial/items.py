from scrapy import Item, Field


class QuoteItem(Item):
    text = Field()
    author = Field()
    tag = Field()

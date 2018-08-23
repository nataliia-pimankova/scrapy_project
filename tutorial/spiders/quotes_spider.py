import scrapy

from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # download_delay = 5.0

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        root = scrapy.Selector(response)
        quotes = root.xpath('//div[@class="quote"]')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.xpath('//span[@class="text"]/text()').extract_first()
            item['author'] = quote.xpath('//small[@class="author"]/text()').extract_first()
            item['tags'] = quote.xpath('//div[@class="tags"]/a[@class="tag"]/text()').extract()
            yield item

        next_page_url = root.xpath('//li[@class="next"]/a@href').extract_first()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

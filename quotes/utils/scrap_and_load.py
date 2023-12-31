import scrapy
import os
import django
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from itemadapter import ItemAdapter
from datetime import datetime


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from quotesapp.models import Tag as T, Quote as Q, Author as A

class Quote(Item):
    author = Field()
    quote = Field()
    tags = Field()


class Author(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesPipeline:
    authors_file = "authors.json"
    quotes_file = "quotes.json"
    authors = []
    quotes = []
    user = None

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if isinstance(item, Author):
            self.authors.append(adapter.asdict())
        if isinstance(item, Quote):
            self.quotes.append(adapter.asdict())
        return item

    def close_spider(self, spider):
        for author in self.authors:
            author["born_date"] = datetime.strptime(author["born_date"], "%B %d, %Y").date()
            new_author, created = A.objects.get_or_create(**author)
            if self.user and created:
                new_author.user = self.user
                new_author.save()

        for quote in self.quotes:
            new_quote, created = Q.objects.get_or_create(
                                    quote=quote["quote"],
                                    author=A.objects.get(fullname=quote["author"]),
                                    )
            for tag in quote["tags"]:
                new_tag = T.objects.get_or_create(name=tag)[0]
                new_quote.tags.add(new_tag)
            
            new_quote.save()
        

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"ITEM_PIPELINES": {QuotesPipeline: 300}}

    def parse(self, response):
        for item in response.xpath("/html//div[@class='quote']"):
            tags = item.xpath("div[@class='tags']/a/text()").extract()
            author = item.xpath("span/small/text()").get().strip()
            quote = item.xpath("span[@class='text']/text()").get().strip()
            yield Quote(quote=quote, tags=tags, author=author)
            yield response.follow(url=self.start_urls[0] + item.xpath("span/a/@href").get(), 
                                  callback=self.nested_parse_author, 
                                  meta={"author": author})
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response):
        # For corresponding quotes author field to authors fullname field
        fullname = response.meta.get("author")

        author = response.xpath("/html//div[@class='author-details']")
        born_date = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = author.xpath("div[@class='author-description']/text()").get().strip()

        yield Author(fullname=fullname, 
                     born_date=born_date, 
                     born_location=born_location, 
                     description=description)


def main(user=None):
    QuotesPipeline.user = user
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start(install_signal_handlers=0)
    process.join()
    QuotesPipeline.user = None

if __name__ == "__main__":

    main()

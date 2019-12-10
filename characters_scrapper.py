# This Python file uses the following encoding: utf-8
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'characterspider'
    start_urls = [
        'https://www.aroma-zone.com/info/guide-des-huiles-essentielles/tous',
    ]

    def parse(self, response):
        for next_page in response.css('div.select-filter li'):
            if next_page is not None:
                title = next_page.css('a ::text').extract()
                url = next_page.css('a::attr(href)').extract_first()
                next_page = response.urljoin(url)
                yield scrapy.Request(next_page, callback=self.parse, meta={"title": title})

        for link in response.css('div.products compact'):
            if link.css('a::attr(href)').extract_first() is not None:
                meta = response.meta
                url1 = link.css('a::attr(href)').extract_first()
                next_page1 = response.urljoin(url1)
                meta["character"] = link.css('a::attr(title)').extract_first()
                yield scrapy.Request(next_page1, callback=self.parse, meta=meta)

        for link1 in response.css('div.propriete-desc proprietes li'):
            if link1.css('a::attr(href)').extract_first() is not None:
                meta = response.meta
                yield {'title': meta["title"],
                       'character': meta["character"],
                       'properties': "essai"
                       }


        # for link in response.css('div.select-filter li'):
        #     yield {'character': link.css('a ::text').extract_first(),
        #            'link': link.css('a::attr(href)').extract_first()
        #            }
        # for link in response.css('div.view-content div'):
        #     yield {'character': link.css('a::attr(title)').extract_first(),
        #            'link': link.css('a::attr(href)').extract_first()
        #            }
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'characterspider'
    start_urls = ['https://www.aroma-zone.com/info/guide-des-huiles-essentielles/tous?tid_problematique=519']

    def parse(self, response):
        for link in response.css('div.select-filter li'):
            yield {'character': link.css('a ::text').extract_first(),
                   'link': link.css('a::attr(href)').extract_first()
                   }

            # for link in response.css('div.view-content div'):
            #     yield {'character': link.css('a::attr(title)').extract_first(),
            #            'link': link.css('a::attr(href)').extract_first()
            #            }
            
            hxs = HtmlXPathSelector(response)
            sites = hxs.select('//table[@class="custom_table"]/tr')





            items = []

            for site in sites:

                #print site
                item = DeloitteListingItem()

                name = ''.join(site.select('./td/a/text()').extract())
                url = ''.join(site.select('./td/a/@href').extract())
                ca = ''.join(site.select('./td[4]/text()').extract())

                item['name'] = name
                item['url'] = url
                item['ca'] = ca

                items.append(item)

            return items
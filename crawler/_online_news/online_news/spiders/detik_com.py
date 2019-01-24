import scrapy

class DetikCom(scrapy.Spider):
    name = "detikcom"

    def start_requests(self):
        urls = [
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
            # 'http://www.liputan6.com/search?q=bubarkan+hti&type=all',
            # 'http://liputan6.com/tag/pilkada-dki-jakarta-2017',
            'http://m.liputan6.com/search?q=bubarkan+hti',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
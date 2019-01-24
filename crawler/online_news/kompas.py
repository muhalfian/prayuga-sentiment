import scrapy
from scrapy.crawler import CrawlerProcess
import crawler.online_news.settings as settings; 
import crawler.online_news.baseSpider as baseSpider; 

class Kompas(scrapy.Spider):
    name = "Kompas"

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': { 'wait': 0.5 }
                }
            })

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)


def run(urls):
    process = CrawlerProcess({'USER_AGENT': settings.USER_AGENT})
    process.crawl(Kompas,urls=urls)
    process.start() # the script will block here until the crawling is finished
import scrapy
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
import crawler.online_news.settings as settings; 
import crawler.online_news.base as baseSpider; 

from crawler.online_news.i18n import _
from crawler.online_news.util.wib_to_utc import wib_to_utc

class Liputan6(scrapy.Spider):
    name = "Liputan6"
    allowed_domains = ["liputan6.com"]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        
        articles = response.css('div.article-snippet__info');
        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]
            
            info_selectors = article.css('div.article-snippet__date')
            info_selectors = info_selectors.css('.timeago::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            # Example '13 Okt 2016 16:10'
            info_time = info_selectors.extract()[0]
            # Example '13 Oct 2016 16:10'
            info_time = ' '.join([_(w) for w in info_time.split(' ')])
            
            title_selectors = article.css('.article-snippet__title-text::text')
            if not title_selectors:
                raise CloseSpider('title_selectors not found');
            title = title_selectors.extract()[0]
            
            print info_time;
            print title;
            print url;
            print "==========================================================";
            
            if(baseSpider.checkNewsIsMatch(title,self.query['tags']) and baseSpider.checkValidDate(info_time,self.query['since'],self.query['until'])):
            # For each url we create new scrapy Request
                yield Request(url, meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  }, callback=self.parse_news)

        
    # TODO: Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)
        id_url = response.url;

        comments = response.css('div.article-comment--item')
        if not comments:
            raise CloseSpider('comment not found')
        
        for comment in comments:
            data_save = {};
            # Name commentator
            name_selector = comment.css('a.article-comment--item__title::text')
            if not name_selector:
                raise CloseSpider('name comment not found')
            data_save['name'] = name_selector.extract()[0];
            
            # Date comment
            date = comment.css('time.article-comment--item__time::text');
            if not date:
                raise CloseSpider('date comment not found')
            info_time = date.extract()[0];
            # Example '13 Oct 2016 16:10'
            info_time = ' '.join([_(w) for w in info_time.split(' ')])
            data_save['date'] = datetime.strptime(info_time, "%d %b %Y %H:%M").strftime("%Y-%m-%d %H:%M")
            
            # Text comment
            text_comment_selector = comment.css('p.article-comment--item__content::text');
            if not text_comment_selector:
                raise CloseSpider('text comment not found')
            data_save['text_comment'] = text_comment_selector.extract()[0];
            data_save['id_url']       = id_url;
            data_save['id_apps']      = self.query['idApps'];
            data_save['sosmed']       = settings.online_news['liputan6'];

            baseSpider.saveComment(data_save);


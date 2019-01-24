import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from datetime import datetime
import urllib2,cookielib
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
import crawler.online_news.settings as settings; 
import crawler.online_news.base as baseSpider; 

from crawler.online_news.i18n import _
from crawler.online_news.util.wib_to_utc import wib_to_utc
from pprint import pprint
import json

class DetikCom(scrapy.Spider):
    name = "DetikCom"
    allowed_domains = ["detik.com"]
    current_page = 0;

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        
        articles = response.css('div.list.media_rows.list-berita > article');
        print len(articles);
        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                continue;
            url = url_selectors.extract()[0]
            id_news = '';
            if('/d-' in url):
                id_news = url.split('/d-')[1];
                id_news = id_news.split('/')[0];
                print id_news;
            
            # Example 'Sabtu 08 Oct 2016, 14:54 WIB  - '
            info_selectors = article.css('.box_text span.date::text')
            if not info_selectors:
                continue;
            info_time = info_selectors.extract()[0]
            # Example 'Sabtu, 08 Oct 2016 14:54 WIB'
            info_time = info_time.split('   -  ')[0];
            info_time = info_time.split(', ')[1];
            info_time = info_time.split(' WIB')[0];
            # Example '13 Oct 2016 16:10'
            info_time = ' '.join([_(w) for w in info_time.split(' ')])
            
            title_selectors = article.css('.box_text h2.title::text')
            if not title_selectors:
                continue;
            title = title_selectors.extract()[0]
            
            print info_time;
            print title;
            print url;
            print "==========================================================";

            if(id_news != '' and baseSpider.checkNewsIsMatch(title,self.query['tags']) and baseSpider.checkValidDate(info_time,self.query['since'],self.query['until'])):
                url_comment = 'https://comment.detik.com/v2/?get&key='+id_news+'&group=10&start=1&limit=9999&sort=newest';
                self.extract_comment_json(self.file_get_contents(url_comment));

        next_url = None;
        next_url = response.css('.paging a.last::attr(href)');
        if not next_url:
            raise CloseSpider('next_url not found')
        next_url = next_url.extract()[-1];

        cp = next_url.split('&page=')[1];
        if (cp < self.current_page):
            raise CloseSpider('last page');

        self.current_page = self.current_page + 1;
        yield Request(next_url, callback=self.parse)

               
    
    def extract_comment_json(self,json_data):
        comments = json.loads(json_data)
        comments = comments['entries'];
        for comment in comments:
            data_save = {};
            data_save['name']         = comment['prf_name'];
            data_save['text_comment'] = comment['cmt_text'];
            data_save['date']         = datetime.fromtimestamp(int(comment['created'])).strftime('%Y-%m-%d %H:%M:%S');
            data_save['id_url']       = comment['link'];
            data_save['id_apps']      = self.query['idApps'];
            data_save['sosmed']       = settings.online_news['detikcom'];
            baseSpider.saveComment(data_save);

    '''
    Function that returns the source from the target url
    @param url  
    '''
    def file_get_contents(self,url):
        url = str(url).replace(" ", "+") # just in case, no space in url
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
            return page.read()
        except urllib2.HTTPError, e:
            print e.fp.read()
        return ''

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


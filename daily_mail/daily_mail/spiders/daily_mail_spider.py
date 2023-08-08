import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class DailyMailSpiderSpider(CrawlSpider):
    name = "daily_mail_spider"
    allowed_domains = ["www.dailymail.co.uk"]
    start_urls = ["https://www.dailymail.co.uk/home/index.html"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    rules = [Rule(LinkExtractor(allow='www.dailymail.co.uk'), callback='parse_article', follow=True)]
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10
    }


    def parse_article(self, response):
        title = response.xpath('//div[@id="js-article-text"]/h2/text()').get()
        if 'article' in response.url and title:
            publish_date = response.xpath('//span[@class="article-timestamp article-timestamp-published"]/time/@datetime').get()
            if not publish_date:
                publish_date = response.xpath('//span[@class="article-timestamp article-timestamp-updated"]/time/@datetime').get()
            category = re.search('\.co\.uk\/(.*?)\/', response.url).group(1)
            article_text = response.xpath('//p[@class="mol-para-with-font"]/text()').getall()
            if not article_text:
                article_text = response.xpath('//p[@class="mol-para-with-font"]/*[1]/text()').get()

            yield {
                'url': response.url,
                'title': title,
                'publish_date': publish_date,
                'category': category,
                'article_text': article_text
            }

        else:
            pass

        
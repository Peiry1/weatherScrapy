import scrapy
from weatherScrapy.items import WeatherItem


class WeatherSpider(scrapy.Spider):
    name = "weather_spider"  # 爬虫的唯一名称
    allowed_domains = ["d1.weather.com.cn"]  # 允许爬取的域名
    start_urls = ["https://d1.weather.com.cn/calendar_new/2025/101270101_202506.html?_=1749718395948"] # 成都40天天气数据的URL

    def parse(self, response):
        # 实例化 Item 对象
        item = WeatherItem()
        item['content'] = response.text[11:]
        return item

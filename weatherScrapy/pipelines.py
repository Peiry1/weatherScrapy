# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import xlwt
import csv
import sqlite3

class WeatherPipelineXls:
    def process_item(self, item, spider):
        weathers = json.loads(item['content'])
        writebook = xlwt.Workbook()
        sheet = writebook.add_sheet('Sheet1')
        keys = ['date','nlyf','nl','w1','wd1','max','min','jq','t1','hmax','hmin','hgl','alins','als']
        for i in range(len(keys)):
            sheet.write(0, i, keys[i])
        for i in range(len(weathers)):
            for j in range(len(keys)):
                sheet.write(i + 1, j, weathers[i][keys[j]])
        writebook.save('weathers.xls')

class WeatherPipelineCsv:
    def process_item(self, item, spider):
        weathers = json.loads(item['content'])
        keys = ['date','nlyf','nl','w1','wd1','max','min','jq','t1','hmax','hmin','hgl','alins','als']
        with open('weathers.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            for weather in weathers:
                writer.writerow({k: weather.get(k, '') for k in keys})
        return item
    
class WeatherPipelineSqlite3:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('weathers.db')
        self.cursor = self.conn.cursor()
        self.keys = ['date','nlyf','nl','w1','wd1','max','min','jq','t1','hmax','hmin','hgl','alins','als']
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS weather (
                date TEXT, nlyf TEXT, nl TEXT, w1 TEXT, wd1 TEXT, max TEXT, min TEXT, jq TEXT,
                t1 TEXT, hmax TEXT, hmin TEXT, hgl TEXT, alins TEXT, als TEXT
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        weathers = json.loads(item['content'])
        for weather in weathers:
            values = [weather.get(k, '') for k in self.keys]
            self.cursor.execute(f'''
                INSERT INTO weather ({','.join(self.keys)}) VALUES ({','.join(['?']*len(self.keys))})
            ''', values)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
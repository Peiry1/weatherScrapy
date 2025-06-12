# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import xlwt

class WeatherPipeline:
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

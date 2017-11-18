# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser
import csv

myData = [['Name', 'Parent', 'Age']]

class SpidyQuotesViewStateSpider(scrapy.Spider):
    name = 'spidyquotes-viewstate'
    start_urls = ['http://sec.up.nic.in/ElecLive/resultsearch.aspx']
    download_delay = 1.5

    def parse(self, response):
        i = 1
        for post in response.css('select#ContentPlaceHolder1_ddlPostTypes > option ::attr(value)').extract():
            if int(post) == -1:
                continue
            # yield scrapy.FormRequest.from_response(response, 
            #     'http://sec.up.nic.in/ElecLive/resultsearch.aspx',
            #     formdata={
            #         'ContentPlaceHolder1_ddlPostTypes': post,
            #         '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()
            #     },
            #     callback=self.parse_districts
            # )
            yield scrapy.FormRequest.from_response(response,
                formdata={
                    'ctl00$ContentPlaceHolder1$ddlPostTypes': '1',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()
                },
                callback=self.parse_districts
            )
            break

    def parse_districts(self, response):
        for district in response.css('select#ContentPlaceHolder1_ddlDistrict > option ::attr(value)').extract():
            if int(district) == -1:
                continue
            yield scrapy.FormRequest.from_response(response, formid='form1',
                formdata={
                    'ctl00$ContentPlaceHolder1$ddlPostTypes': response.css(
                        'select#ContentPlaceHolder1_ddlPostTypes > option[selected] ::attr(value)'
                    ).extract_first(),
                    'ctl00$ContentPlaceHolder1$ddlDistrict': district,
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()
                },
                callback=self.parse_results,
                clickdata = {'name':'ctl00$ContentPlaceHolder1$btnshow'}
            )

    
    def check(self, response):
        open_in_browser(response)

    def parse_results(self, response):
        # print(response.css('h3::text').extract())
        # print(response.css('html').extract())
        for quote in response.css("div#ContentPlaceHolder1_Panel1"):
            # yield {
            #     'name': quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first(),
            #     'mom/dad': quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first(),
            #     'age': quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first(),
            # }
            myData.append([quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first().encode('utf-8'),quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first().encode('utf-8'), quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first().encode('utf-8')])
            print([quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first(),quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first(), quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first()])
            f = open('csvfile.csv','w')
            f.write('hi there\n') #Give your csv text here.
            f.write(quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first() + "," + quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first() + "," + quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first())
            ## Python will convert \n to os.linesep
            f.close()
            break


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(SpidyQuotesViewStateSpider)
    process.start() # the script will block here until the crawling is finished
    csv.register_dialect('myDialect', quoting=csv.QUOTE_NONE)
    myFile = open('csvexample4.csv', 'w', encoding='utf-8')
    with myFile:  
       writer = csv.writer(myFile, dialect='myDialect')
       writer.writerows(myData)
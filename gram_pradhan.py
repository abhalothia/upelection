# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser
import csv
import sys

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
                    'ctl00$ContentPlaceHolder1$ddlPostTypes': '5',
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
                callback=self.parse_vikas
            )
            break

    def parse_vikas(self, response):
        for block in response.css('select#ContentPlaceHolder1_ddlBlock > option ::attr(value)').extract():
            if int(block) == -1:
                continue
            yield scrapy.FormRequest.from_response(response, formid='form1',
                formdata={
                    'ctl00$ContentPlaceHolder1$ddlPostTypes': response.css(
                        'select#ContentPlaceHolder1_ddlPostTypes > option[selected] ::attr(value)'
                    ).extract_first(),
                    'ctl00$ContentPlaceHolder1$ddlDistrict': response.css(
                        'select#ContentPlaceHolder1_ddlDistrict > option[selected] ::attr(value)'
                    ).extract_first(),
                    'ctl00$ContentPlaceHolder1$ddlBlock': block,
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()
                },
                callback=self.parse_panch,
                clickdata = {'name':'ctl00$ContentPlaceHolder1$btnshow'}
            ) 
            break 

    def parse_panch(self, response):
        for panch in response.css('select#ContentPlaceHolder1_ddlGpName > option ::attr(value)').extract():
            if int(panch) == -1:
                continue
            yield scrapy.FormRequest.from_response(response, formid='form1',
                formdata={
                    'ctl00$ContentPlaceHolder1$ddlPostTypes': response.css(
                        'select#ContentPlaceHolder1_ddlPostTypes > option[selected] ::attr(value)'
                    ).extract_first(),
                    'ctl00$ContentPlaceHolder1$ddlDistrict': response.css(
                        'select#ContentPlaceHolder1_ddlDistrict > option[selected] ::attr(value)'
                    ).extract_first(),
                    'ctl00$ContentPlaceHolder1$ddlBlock': response.css(
                        'select#ContentPlaceHolder1_ddlBlock > option[selected] ::attr(value)'
                    ).extract_first(),
                    'ctl00$ContentPlaceHolder1$ddlGpName': panch,
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()
                },
                callback=self.parse_results,
                clickdata = {'name':'ctl00$ContentPlaceHolder1$btnshow'}
            ) 
            break

    def parse_results(self, response):
        # print(response.css('h3::text').extract())
        # print(response.css('html').extract())
        for quote in response.css("div#ContentPlaceHolder1_Panel1"):
            # yield {
            #     'name': quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first(),
            #     'mom/dad': quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first(),
            #     'age': quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first(),
            # }
            # myData.append([quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first(),quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first().encode('utf-8'), quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first().encode('utf-8')])
            

            #agg info
            total_cands =  response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(1)::text').extract_first().strip()
            reservation =  response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text').extract_first().strip()
            electors =  response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(3)::text').extract_first().strip()
            tv = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(4)::text').extract_first().strip()
            rejected = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(5)::text').extract_first().strip()
            tvv = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(6)::text').extract_first().strip()
            turnout = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(7)::text').extract_first().strip()

            #winner_info
            
            
            winner = (quote.css('span#ContentPlaceHolder1_Repeater2_Label12_0 ::text').extract_first())
            district = response.css('select#ContentPlaceHolder1_ddlDistrict > option[selected] ::text').extract_first()
            block = response.css('select#ContentPlaceHolder1_ddlBlock > option[selected] ::text').extract_first()
            #myData.append(quote.css('span#ContentPlaceHolder1_Repeater2_Label12_1 ::text').extract_first() + "," + quote.css('span#ContentPlaceHolder1_Repeater2_Label7_1 ::text').extract_first() + "," + quote.css('span#ContentPlaceHolder1_Repeater2_Label8_1 ::text').extract_first())
            ## Python will convert \n to os.linesep


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    f = open("test.csv", 'w')
    # sys.stdout = f
    process.crawl(SpidyQuotesViewStateSpider)
    process.start() # the script will block here until the crawling is finished
    for s in myData:
        print (s)
    # with myFile:  
    #    writer = csv.writer(myFile, dialect='myDialect')
    #    writer.writerows(myData)
# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser
import csv
import sys

myData = []
head = ['district','block_name','village_name','total_cand', 'seat_res', 'electors', 'tv', 'rejected', 'tvv', 'turnout']
head = head + ['cand1', 'f_hus1', 'age1', 'sex1', 'mob1', 'edu1', 'v1', 'canr1', 'tv1', 'tvv1']

next_c = ['cand', 'f_hus', 'age', 'sex', 'mob', 'edu', 'v', 'canr', 'tv', 'tvv', 'deposit']

for i in range(2,20):
    for s in next_c:
        head.append(s + str(i))
myData.append(head)

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
            currRow = []
            district = response.css('select#ContentPlaceHolder1_ddlDistrict > option[selected] ::text').extract_first()
            currRow.append(district)

            block = response.css('select#ContentPlaceHolder1_ddlBlock > option[selected] ::text').extract_first()
            currRow.append(block)

            village = response.css('select#ContentPlaceHolder1_ddlGpName > option[selected] ::text').extract_first()
            currRow.append(village)
            #agg info
            total_cands =  response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(1)::text').extract_first().strip()
            currRow.append(total_cands)

            reservation =  response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text').extract_first().strip()
            currRow.append(reservation)

            electors =  response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(3)::text').extract_first().strip()
            currRow.append(electors)

            tv = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(4)::text').extract_first().strip()
            currRow.append(tv)

            rejected = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(5)::text').extract_first().strip()
            currRow.append(rejected)

            tvv = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(6)::text').extract_first().strip()
            currRow.append(tvv)

            turnout = response.css('div#topstat>table:nth-child(1) > tr:nth-child(2) > td:nth-child(7)::text').extract_first().strip()
            currRow.append(turnout)

            #winner_info
            winner = (quote.css('span#ContentPlaceHolder1_Repeater2_Label12_0::text').extract_first())
            currRow.append(winner)

            parent = (quote.css('span#ContentPlaceHolder1_Repeater2_Label7_0::text').extract_first())
            currRow.append(parent)

            age = (quote.css('span#ContentPlaceHolder1_Repeater2_Label8_0::text').extract_first())
            currRow.append(age)

            gender = (quote.css('span#ContentPlaceHolder1_Repeater2_Label9_0::text').extract_first())
            currRow.append(gender)

            mobile = (quote.css('span#ContentPlaceHolder1_Repeater2_Label10_0::text').extract_first())
            currRow.append(mobile)

            education = (quote.css('span#ContentPlaceHolder1_Repeater2_Label16_0::text').extract_first())
            currRow.append(education)

            v1 = (quote.css('span#ContentPlaceHolder1_Repeater2_Label11_0::text').extract_first())
            currRow.append(v1)

            canr1 = (quote.css('span#ContentPlaceHolder1_Repeater2_Label14_0::text').extract_first())
            currRow.append(canr1)

            tv1 = (quote.css('span#ContentPlaceHolder1_Repeater2_Label18_0::text').extract_first())
            currRow.append(tv1)

            tvv1 = (quote.css('span#ContentPlaceHolder1_Repeater2_Label19_0::text').extract_first())
            currRow.append(tvv1)

            table = response.xpath('//*[@id="topstat"]/table[3]')
            i = 1
            for row in table.xpath('.//tr'):
                if i == 1:
                    i+=1
                    continue
                test = []
                for col in row.xpath('.//td'):
                    val = col.xpath('span/text()').extract_first()
                    if val:
                        test.append(val.strip())
                    else:
                        test.append("")
                test.pop()
                currRow = currRow + test
        myData.append(currRow)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    f = open("test.csv", 'w')
    sys.stdout = f
    process.crawl(SpidyQuotesViewStateSpider)
    process.start() # the script will block here until the crawling is finished
    # f = open("test.csv", 'w')
    # sys.stdout = f
    # for s in myData:
    #     print (s)
    csv.register_dialect('myDialect', quoting=csv.QUOTE_NONE)
    myFile = open('csvexample4.csv', 'w', encoding='utf-8')
    with myFile:  
       writer = csv.writer(myFile, dialect='myDialect')
       writer.writerows(myData)






# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from aims.items import CourseItem
from aims.common_function import (
    custom_escape,
    convert_to_reverse_polish_notation,
    string_to_element_array
)
from logined_spider import LoginedSpider


class CourseSpider(LoginedSpider):

    name = 'course'
    download_delay = 2

    def request_after_login(self):
        return Request(
            url='https://banweb.cityu.edu.hk/pls/PROD/' +
                'hwscrssh_cityu.P_CrseSearch',
            callback=self.course_terms_page)

    def course_terms_page(self, response):
        yield FormRequest.from_response(
                response,
                formxpath='/html/body/div[5]/form',
                formdata={'TERM': '201602'})

    def build_courses_url(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        courses = soup.find_all(
            href=re.compile("hwscrssh_cityu.P_DispOneSection"))
        courses_link = \
            map(lambda x:
                "https://banweb.cityu.edu.hk/pls/PROD/{}".format(x['href']),
                courses)
        return list(set(courses_link))

    def parse(self, response):
        courses_link = self.build_courses_url(response)

        for idx, course_link in enumerate(courses_link):
            if idx % 10 == 0:
                yield self.request_after_login()
            yield Request(
                url=course_link,
                callback=self.parse_course_item)

    def parse_course_item(self, response):
        hxs = HtmlXPathSelector(response)
        full_header = hxs.select('/html/body/div[5]/form/b[1]/text()')\
                         .extract()
        unit = hxs.select('/html/body/div[5]/form/b[2]/text()').extract()
        a_requirement = hxs.select('/html/body/div[5]/form/b[4]/font/text()')\
                           .extract()
        a_exclusive = hxs.select('/html/body/div[5]/form/b[6]/font/text()')\
                         .extract()

        # table = hxs.select('/html/body/div[5]/form/table/tbody').extract()
        # self.log(table)
        operators = {'and': 1, 'or': 2}
        requirement_text = custom_escape(a_requirement)
        requirement_formula = convert_to_reverse_polish_notation(
                                string_to_element_array(requirement_text),
                                operators
                              )
        exclusive_text = custom_escape(a_exclusive)
        exclusive_formula = string_to_element_array(exclusive_text)

        item = CourseItem()
        item['full_header'] = full_header[0].replace('Course : ', '')
        item['code'] = item['full_header'].split(' ')[0]
        item['unit'] = unit[0].replace('Offering Academic Unit: ', '')
        item['requirement_text'] = requirement_text
        item['requirement_formula'] = requirement_formula
        item['exclusive_text'] = exclusive_text
        item['exclusive_formula'] = exclusive_formula
        yield item

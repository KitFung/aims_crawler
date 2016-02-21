# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from aims.items import CourseItem
from aims.string_parser import (
    str_to_int,
    str_to_bool,
    str_to_list,
    str_to_daterange,
    str_to_timerange
)
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
            href=re.compile('hwscrssh_cityu.P_DispOneSection'))
        courses_link = \
            ['https://banweb.cityu.edu.hk/pls/PROD/{}'.format(x['href'])
             for x in courses]
        return list(set(courses_link))

    def parse(self, response):
        courses_link = self.build_courses_url(response)

        for idx, course_link in enumerate(courses_link):
            if idx % 10 == 0:
                yield self.request_after_login()
            yield Request(
                url=course_link,
                callback=self.parse_course_item)

    def parse_course_table(self, table):
        details = []
        tmp = {}
        # one class one attribute
        attributes = [('CRN', None), ('Section', None),
                      ('Credit', str_to_int), ('Campus', None),
                      ('WEB', str_to_bool), ('Level', None),
                      ('Avail', str_to_int), ('Cap', str_to_int),
                      ('Waitlist_Avail', str_to_bool)]
        num_of_attr = len(attributes)
        # one attribite may map to multiple sub_attributes
        sub_attributes = [('Date', str_to_daterange),
                          ('Day', None), ('Time', str_to_timerange),
                          ('Bldg', None), ('Room', None),
                          ('Instructor', str_to_list)]
        restriction_pair = [('only for Major: ', 'only_majors'),
                            ('not for Major: ', 'not_allow_majors'),
                            ('only for College: ', 'only_colleges'),
                            ('not for College: ', 'not_allow_colleges'),
                            ('only for Degree: ', 'only_degrees'),
                            ('not for Degree: ', 'not_allow_degrees'),
                            ('only for Programme: ', 'only_programmes'),
                            ('not for Programme: ', 'not_allow_programmes')]

        for tr in table:
            if len(tr.xpath('./td')) > 2:
                CRN = custom_escape(
                    tr.xpath('./td[1]/text()').extract_first()
                ).replace(' ', '')
                if len(CRN) > 0:
                    if len(tmp) > 0:
                        details.append(tmp)
                    tmp = {}
                    tmp['lessons'] = []
                    for idx, (key, parser) in enumerate(attributes):
                        value = tr.xpath('./td[{}]/text()'.format(idx + 1))\
                                     .extract_first()
                        # Special Case "FULL"
                        value = custom_escape(value)
                        if parser:
                            value = parser(value)
                        tmp[key] = value
                lessons = {}
                for idx, (key, parser) in enumerate(sub_attributes):
                    j = num_of_attr + idx + 1
                    value = tr.xpath('./td[{}]/text()'.format(j))\
                              .extract_first()
                    # Special Case "FULL"
                    value = custom_escape(value)
                    if parser:
                        value = parser(value)
                    lessons[key] = value
                tmp['lessons'].append(lessons)
            else:
                text = tr.xpath('./td[2]/text()').extract_first()
                is_done = False
                for start_word, key in restriction_pair:
                    if not text.find(start_word) == -1:
                        l = text.replace(start_word, '').split(',')
                        tmp[key] = [t.strip() for t in l]
        details.append(tmp)
        return details

    def parse_course_item(self, response):
        selector = response.selector
        full_header = selector\
            .xpath('//html/body/div[5]/form/b[1]/text()')\
            .extract_first()
        unit = selector\
            .xpath('//html/body/div[5]/form/b[2]/text()')\
            .extract_first()
        a_requirement = selector\
            .xpath('//html/body/div[5]/form/b[4]/font/text()')\
            .extract_first()
        a_exclusive = selector\
            .xpath('//html/body/div[5]/form/b[6]/font/text()')\
            .extract_first()

        table = selector\
            .xpath('//html/body/div[5]/form/table/tr')

        table.pop(0)
        details = self.parse_course_table(table)

        operators = {'and': 1, 'or': 2}
        requirement_text = custom_escape(a_requirement)
        requirement_formula = convert_to_reverse_polish_notation(
                                string_to_element_array(requirement_text),
                                operators
                              )
        exclusive_text = custom_escape(a_exclusive)
        exclusive_formula = string_to_element_array(exclusive_text)

        item = CourseItem()
        item['full_header'] = full_header.replace('Course : ', '')
        item['code'] = item['full_header'].split(' ')[0]
        item['unit'] = unit.replace('Offering Academic Unit: ', '')
        item['requirement_text'] = requirement_text
        item['requirement_formula'] = requirement_formula
        item['exclusive_text'] = exclusive_text
        item['exclusive_formula'] = exclusive_formula
        item['details'] = details
        yield item

import re
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from aims.items import CourseItem
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
        requirement = hxs.select('/html/body/div[5]/form/b[4]/font/text()')\
                         .extract()
        exclusive = hxs.select('/html/body/div[5]/form/b[6]/font/text()')\
                       .extract()

        # table = hxs.select('/html/body/div[5]/form/table/tbody').extract()
        # self.log(table)

        if len(requirement) > 0:
            requirement = requirement[0].replace('&nbsp', '').split(' ')
        if len(exclusive) > 0:
            exclusive = exclusive[0].replace('&nbsp', '').split(' ')
        filter(lambda x: len(x) > 0, requirement)
        filter(lambda x: len(x) > 0, exclusive)

        item = CourseItem()
        item['full_header'] = full_header[0].replace('Course : ', '')
        item['unit'] = unit[0].replace('Offering Academic Unit: ', '')
        item['requirement'] = requirement
        item['exclusive'] = exclusive
        yield item

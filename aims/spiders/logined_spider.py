import os
import abc
from scrapy import Spider
from scrapy.http import Request, FormRequest


class LoginedSpider(Spider):
    allowed_domains = ['banweb.cityu.edu.hk']

    def start_requests(self):
        login_page =\
            'https://banweb.cityu.edu.hk/pls/PROD/twgkpswd_cityu.P_WWWLogin'
        return [Request(url=login_page, callback=self.login)]

    def login(self, response):
        '''Generate a login request.'''
        return FormRequest.from_response(
                response,
                formxpath='/html/body/div[4]/form[2]',
                formdata={
                    'p_username': os.environ['AIMS_NAME'],
                    'p_password': os.environ['AIMS_PASSWORD']
                },
                callback=self.check_login_response)

    def check_login_response(self, response):
        if response.status == 200:
            self.log('Successfully logged in. Let\'s start crawling!')
            return self.request_after_login()
        else:
            self.log('Failed Login.')

    @abc.abstractmethod
    def request_after_login(self):
        pass

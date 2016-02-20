# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AimsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CourseItem(scrapy.Item):
    code = scrapy.Field()
    full_header = scrapy.Field()
    unit = scrapy.Field()
    requirement_text = scrapy.Field()
    requirement_formula = scrapy.Field()
    exclusive_text = scrapy.Field()
    exclusive_formula = scrapy.Field()
    details = scrapy.Field()

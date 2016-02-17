# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AimsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    pass


class CourseItem(scrapy.Item):
    full_header = scrapy.Field()
    unit = scrapy.Field()
    requirement = scrapy.Field()
    exclusive = scrapy.Field()

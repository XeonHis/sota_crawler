# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SotaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_category = scrapy.Field()
    main_category_url = scrapy.Field()
    sub_category = scrapy.Field()
    sub_category_url = scrapy.Field()
    third_category = scrapy.Field()
    third_category_url = scrapy.Field()
    detail = scrapy.Field()
    detail_url = scrapy.Field()

    pass

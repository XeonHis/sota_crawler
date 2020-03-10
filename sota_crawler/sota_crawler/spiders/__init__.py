import scrapy
from sota_crawler.items import SotaCrawlerItem
import openpyxl


class sotaSpider(scrapy.Spider):
    name = "sota_crawler"
    start_urls = [
        'https://paperswithcode.com/sota'
        # 'https://paperswithcode.com/area/computer-vision'
    ]

    def parse(self, response):
        selectors = response.xpath('//div[contains(@class,"task-group-title")]')

        for each in selectors:
            main_object = SotaCrawlerItem()

            main_catagory = each.xpath('div/h4/a/text()').get().strip()
            main_object['main_category'] = main_catagory

            main_catagory_url = response.urljoin(each.xpath('div/h4/a/@href').get().strip())
            main_object['main_category_url'] = main_catagory_url

            yield scrapy.Request(main_catagory_url, callback=self.parse_2nd, meta={'main': main_object})

            # yield main_object

    def parse_2nd(self, response):
        main_object = response.meta['main']
        selectors = response.xpath("//div[contains(@class,'featured-task')]/div[@class='row']")

        for each in selectors:
            # second_object = SotaCrawlerItem()

            sub_category = each.xpath('div/h4/text()').get().strip()
            main_object['sub_category'] = sub_category
            # second_object['sub_category'] = sub_category

            sub_category_url = main_object['main_category_url'] + '/'+sub_category.lower().replace(' ', '-')
            main_object['sub_category_url'] = sub_category_url
            # second_object['sub_category_url'] = sub_category_url


            yield main_object

    def parse_3rd(self, response):
        main_object = response.meta['main']
        second_object = response.meta['second']
        selectors = response.xpath("//div[@class='card']")

        for each in selectors:
            third_object = SotaCrawlerItem()

            detail = each.xpath("a/div/h1/text()").get().strip()
            third_object['detail'] = detail

            detail_url = response.urljoin(each.xpath("a/@href").get().strip())
            third_object['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.parse_detail,
                                 meta={'main': main_object, 'second': second_object, 'third': third_object})

    def parse_detail(self, response):
        final_object = SotaCrawlerItem()
        main_object = response.meta['main']
        second_object = response.meta['second']

        final_object['main_category'] = main_object['main_category']
        final_object['main_category_url'] = main_object['main_category_url']
        final_object['sub_category'] = second_object['sub_category']
        final_object['sub_category_url'] = second_object['sub_category_url']

        if second_object['sub_category_url'] == '':
            final_object['detail'] = second_object['detail']
            final_object['detail_url'] = second_object['detail_url']
        else:
            third_object = response.meta['third']

            final_object['detail'] = third_object['detail']
            final_object['detail_url'] = third_object['detail_url']

        yield final_object

    def item_init(self, item):
        item['main_category'] = 'null'
        item['main_category_url'] = 'null'
        item['sub_category'] = 'null'
        item['sub_category_url'] = 'null'
        item['third_category'] = 'null'
        item['third_category_url'] = 'null'
        item['detail'] = 'null'
        item['detail_url'] = 'null'
        return item

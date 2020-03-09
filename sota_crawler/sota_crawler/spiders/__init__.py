import scrapy
from sota_crawler.items import SotaCrawlerItem


class sotaSpider(scrapy.Spider):
    name = "sota_crawler"
    start_urls = [
        'https://paperswithcode.com/sota'
    ]

    def parse(self, response):
        selectors = response.xpath('//div[contains(@class,"task-group-title")]')

        for each in selectors:
            sota_object = SotaCrawlerItem()

            main_catagory = each.xpath('div/h4/a/text()').get().strip()
            sota_object['main_category'] = main_catagory

            main_catagory_url = response.urljoin(each.xpath('div/h4/a/@href').get().strip())
            sota_object['main_category_url'] = main_catagory_url

            yield scrapy.Request(main_catagory_url, callback=self.parse_2nd, meta={'item': sota_object})

            # yield sota_object

    def parse_2nd(self, response):
        sota_object = response.meta['item']
        selectors = response.xpath("//div[contains(@class,'featured-task')]")

        for each in selectors:

            sub_category = each.xpath('div/div/h4/text()').get().strip()
            sota_object['sub_category'] = sub_category

            sub_category_url = each.xpath('div[@class="sota-all-tasks"]/a/@href').get()
            if not sub_category_url:
                sota_object['sub_category_url'] = "None"
                sota_object['detail'] = sub_category
                detail_url = each.xpath('div[@class="card-deck card-break infinite-item"]/div/a/@href').get().strip()
                sota_object['detail_url'] = detail_url

                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': sota_object})
            else:
                sota_object['sub_category_url'] = response.urljoin(sub_category_url.strip())

                yield scrapy.Request(sub_category_url, callback=self.parse_3rd, meta={'item': sota_object})

            # yield sota_object

    def parse_3rd(self, response):
        sota_object = response.meta['item']
        selectors = response.xpath("//div[@class='card']")

        for each in selectors:
            detail = each.xpath("a/div/h1/text()").get.strip()
            sota_object['detail'] = detail

            detail_url = response.urljoin(each.xpath("a/@href").get().strip())
            sota_object['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': sota_object})

    def parse_detail(self, response):
        pass

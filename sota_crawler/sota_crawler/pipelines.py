from openpyxl import Workbook


class SotaCrawlerPipeline(object):
    def __init__(self):
        self.wb = Workbook()  # 类实例化
        self.ws = self.wb.active  # 激活工作表
        # self.ws.append(['main_category', 'main_category_url', 'sub_category',
        #                 'sub_category_url', 'third_category', 'third_category_url',
        #                 'detail', 'detail_url'])  # 添加表头

    def process_item(self, item, spider):
        data = [
            item['main_category'], item['main_category_url'],
            item['sub_category'], item['sub_category_url'],
            item['detail'], item['detail_url']
        ]
        self.ws.append(data)
        self.wb.save('sota_data.xlsx')
        return item

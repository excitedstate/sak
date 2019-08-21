import json
from func.sak_dbs import SAKSqlDBS
from func.my_calendar import get_n_date

class GetResponse:
    def __init__(self, type='name', value='平安银行'):
        self.db = SAKSqlDBS()
        self.dic_stock = {}
        self.dic_news = {}
        self.type = type
        self.value = value

    def get_stock(self):
        self.dic_stock.clear()
        if self.type == 'name':
            res = self.db.get_stock_by_name(self.value)
        elif self.type == 'symbol':
            res = self.db.get_stock_by_symbol(self.value)
        elif self.type == 'id':
            res = self.db.get_stock_by_id(self.value)
        else:
            condition = self.type+ '=' + self.value
            res = self.db.get_stock(condition)
        if len(res) != 0:
            stock = res[0][0]
            tmp_stock = json.loads(stock)
            for key, value in tmp_stock.items():
                self.dic_stock[key] = float(value)
            return self.dic_stock
        else:
            print('NOT FOUND ERROR!')

    def get_news(self):
        now_date = get_n_date(0)
        # now_date = now_date[:4]+'-'+now_date[4:6]+'-'+now_date[6:]
        res = self.db.get_news_by_date(now_date)
        if not res:
            print("DATETIME ERROR")
            now_date = get_n_date(-1)
            res = self.db.get_news_by_date(now_date)
        for ele in res:
            self.dic_news[ele[0]] = ele[1]


    def flow(self):
        self.get_stock()
        self.get_news()
        return self.dic_stock, self.dic_news

# class GetResponse:
#     def __init__(self):
#         self.urls = ["https://data.gtimg.cn/flashdata/hk/daily/{}/hk00700.js".format(i) for i in range(10, 20)]
#         self.dic_stock = {}
#         self.dic_news = {}
#
#     def get_stock(self):
#         import requests
#         for url in self.urls:
#             a = requests.get(url)
#             if a.status_code == 200:
#                 with open(r".\src\all_stock.txt", "a", encoding="utf-8") as f:
#                     f.write(a.text)
#             else:
#                 print("Failed to connect")
#
#     def sort_the_stock(self):
#         try:
#             for line in open(r".\src\all_stock.txt", "r", encoding="utf-8").readlines():
#                 if len(line) < 40:
#                     continue
#                 else:
#                     num1 = line.find(" ", 0)
#                     self.dic_stock[line[0:6]] = float(line[num1+1:str(line).find(" ", num1+1)])
#             count = 0
#             with open(r".\src\response.txt", "r", encoding="utf-8")as f:
#                 for l in f.readlines():
#                     count += 1
#             if count == 0:
#                 with open(r".\src\response.txt", "a", encoding="utf-8") as f:
#                     f.write(str(json.dumps(self.dic_stock)))
#                     f.write("\n")
#         except FileNotFoundError:
#             self.get_stock()
#             self.sort_the_stock()
#
#     def get_the_news(self):
#         pass
#
#     def sort_the_news(self):
#         for line in open(r".\src\all_news.txt", "r", encoding="utf-8").readlines():
#             dic_tmp = dict(json.loads(line, encoding="utf-8"))
#             self.dic_news[dic_tmp["title"]] = dic_tmp["news"]
#         count = 0
#         with open(r".\src\response.txt", "r", encoding="utf-8")as f:
#             for line in f.readlines():
#                 count += 1
#         with open(r".\src\response.txt", "a", encoding="utf-8")as f:
#             if count == 1:
#                 f.write(str(json.dumps(self.dic_news, ensure_ascii=False)))
#                 f.write("\n")
#
#     def flow(self):
#         self.sort_the_stock()
#         self.sort_the_news()
#         return self.dic_stock, self.dic_news

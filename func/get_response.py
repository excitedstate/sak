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

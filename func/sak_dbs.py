import pymysql
import json

class SAKSqlDBS:
    def __init__(self):
        # # we hope you create database via our tips in this code...
        try:
            self.conn = pymysql.connect(host='your host',
                                      user='root',
                                      password='your password',
                                      charset="utf8",
                                      database='your database',
                                      port=10164)
        except Exception as e:
            print(e)
            self.__init__()
        self.conn.autocommit(True)

    def insert_stock(self,id, ts_code, symbol, name, area, industry,list_date, stock_month):
        table = 'stock_all'
        name = name.replace("'",r"\'")
        sql_query = '''insert into %s values(%d,'%s','%s','%s','%s','%s','%s','%s')'''%(table,id,ts_code,symbol,name,area,industry,list_date,stock_month)
        self.exec_sql_query(sql_query)

    def get_ts_code_by_id(self,start, end):
        sql_query = '''select ts_code from stock_all where id>=%d and id<=%d'''%(start,end)
        return self.exec_sql_query(sql_query)

    def get_symbol_by_name(self, name):
        sql_query = '''select symbol from stock_all where name ='%s' ''' % (name)
        return self.exec_sql_query(sql_query)

    def get_symbol_by_id(self,start, end):
        sql_query = '''select symbol from stock_all where id>=%d and id<=%d'''%(start,end)
        return self.exec_sql_query(sql_query)

    def get_stock(self, condition, like_pattern=''):
        if not like_pattern:
            sql_query = '''select stock_month from stock_all where %s'''%(condition)
        else:
            sql_query = '''select stock_month from stock_all where %s like %s'''%(condition,like_pattern)
        return self.exec_sql_query(sql_query)

    def get_stock_by_symbol(self, symbol):
        return self.get_stock("symbol='%s'"%symbol)

    def get_stock_by_name(self, name):
        return self.get_stock("name='%s'"%name)

    def get_stock_by_id(self,id):
        return self.get_stock("id=%d"%id)

    def get_stock_by_industry(self,industry):
        return self.get_stock("industry='%s'"%industry)

    def get_news_by_date(self, date):
        sql_query = '''select title,content,src from sak_news where `date`= %s ''' % (date)
        return self.exec_sql_query(sql_query)

    def update_trend(self, trend, condition):
        sql_query = "update sak_news set trend='%s'  where %s" % (trend, condition,)
        self.exec_sql_query(sql_query)

    def update_trend_by_content(self, trend, content):
        self.update_trend(trend, "content='%s'"%content)

    def update_stock_month(self,condition, stock_month):
        sql_query = "update stock_all set stock_month='%s'  where %s"%(stock_month,condition,)
        self.exec_sql_query(sql_query)

    def update_us_stock_by_symbol(self, symbol, date, value):
        tmp = self.get_stock_by_symbol(symbol)
        tmp = [ele[0] for ele in tmp]
        if not len(tmp):
            return
        dic_ori = json.loads(tmp[0])
        dic_ori[date] = value
        dic_now = json.dumps(dic_ori)
        self.update_stock_month_by_symbol(symbol, dic_now)

    def update_stock_month_by_id(self, id, stock_month):
        self.update_stock_month("id='%d'"%id, stock_month)

    def update_stock_month_by_symbol(self, symbol,stock_month):
        self.update_stock_month("symbol='%s'"%symbol, stock_month)

    def update_stock_month_by_ts_code(self, ts_code,stock_month):
        self.update_stock_month("ts_code='%s'"%ts_code, stock_month)

    def insert_news(self, classification, title, content,src ,date):
        table = 'sak_news'
        title = title.replace("'",r"\'")
        content = content.replace("'",r"\'")
        sql_query = '''insert into %s values('%s', '%s', '%s', '%s', '%s','[]',5)'''%(table,classification,title,content,src,date)
        self.exec_sql_query(sql_query)

    def exec_sql_query(self,sql_query:str):
        sql_query = sql_query.lower()
        try:
            cur = self.conn.cursor()
            if not sql_query.endswith(";"):
                sql_query += ";"
            print("正在执行>>", sql_query)
            cur.execute(sql_query)
            result = cur.fetchall()
            return result
        except Exception as e:
            print(e)
            self.__init__()
            self.exec_sql_query(sql_query)

    def __del__(self):
        '''
        close the connection when you leave
        :return:  None
        '''
        self.conn.close()

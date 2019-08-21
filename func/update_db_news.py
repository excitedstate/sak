from func.my_calendar import  *
from func.sak_dbs import *
import tushare as ts

def update_news_daily():
    db = SAKSqlDBS()
    sql_query = '''delete from sak_news where date = '%s' ''' % get_today_date()
    db.exec_sql_query(sql_query)
    pro = ts.pro_api('30d71042b9fd2cfc2fa40e23caaf1adebd069b3e323bd11e6cc54a37')
    srcs = ['sina','10jqka','eastmoney','yuncaijing']
    calendar = get_the_calendar(2019, 2020)
    start_date = get_today_date()
    end_date = calendar[calendar.index(start_date) + 1]
    for src in srcs:
        tmp = pro.news(src=src, start_date=start_date, end_date=end_date)
        dic_list =  json.loads(tmp.to_json(orient='index',force_ascii=False)).values()
        for tmp_dic in dic_list:
            content = tmp_dic['content']
            date = tmp_dic['datetime'].split(' ')[0].replace('-','')
            if tmp_dic['title'] != '':
                title = tmp_dic['title'].lstrip()
            else:
                if len(content)<10:
                    title = content.replace('【',' ').replace('】',' ').lstrip()
                else:
                    title = content[:10].replace('【',' ').replace('】',' ').lstrip()+'...'
            content = '[' + tmp_dic['datetime'] + ']\n' + content
            db.insert_news('财经', title,content, src, date)
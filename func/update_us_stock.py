from func.sak_dbs import SAKSqlDBS
from func.my_calendar import *
import requests
import json

def get_value(symbol):
    # # 该函数无法查全,
    url = 'http://hq.sinajs.cn/list=gb_'
    r = requests.get(url + symbol.lower())
    res = r.text
    mv = ['var hq_str_gb_', ';', '"']
    res = res.strip()
    res = res.strip(mv[0] + symbol + '=')
    res = res.strip(mv[1])
    res = res.strip(mv[2])
    res_list = res.split(',')
    if len(res_list)>=2:
        return res_list[1]
    else:
        return '0.0'

def update_us_stock():
    now_date = get_today_date()
    db = SAKSqlDBS()
    for page_num in range(1,160):
        rep = requests.get('''http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['fa8Vo3U4TzVRdsLs']/US_CategoryService.getList?page=%s&num=60&sort=&asc=0&market=&id='''%(page_num))
        rep.encoding='utf-8'
        text = rep.text
        tmp = text.split('\n')[1].split('{')[2:]
        for t in tmp:
            t = '{' + t[:-1]
            if t.endswith(']})'):
                t = t[:-3]
            tmp_dic = json.loads(t)
            symbol = tmp_dic['symbol'].lower()
            db.update_us_stock_by_symbol(symbol, now_date, tmp_dic['price'])

if __name__ == '__main__':
    update_us_stock()
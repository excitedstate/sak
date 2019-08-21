from func.sak_dbs import SAKSqlDBS
import json
from func.my_calendar import *
import tushare as ts

def get_stock_info(db):
    # # 传入的是一个数据库对象
    pro = ts.pro_api('30d71042b9fd2cfc2fa40e23caaf1adebd069b3e323bd11e6cc54a37')
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data = json.loads(data.to_json(orient='index',force_ascii=False))
    i=0
    for key, info in data.items():
        db.insert_stock(int(key)+1, info['ts_code'], info['symbol'], info['name'], info['area'], info['industry'], info['list_date'], '')
        i += 1
        if i > 100:
            break

def update_hk_stock(start=1, end=3656):
    # # 获取2019年的完整日历
    calendar = get_the_calendar(2019,2020)
    # # 登陆数据库
    db = SAKSqlDBS()
    # # 初始化tushare接口
    pro = ts.pro_api('30d71042b9fd2cfc2fa40e23caaf1adebd069b3e323bd11e6cc54a37')
    # # 获取当前时间
    end_date= get_today_date()
    start_date = calendar[calendar.index(end_date)-200]
    # # 获取股票的ts_codes
    ts_codes = db.get_ts_code_by_id(start,end)
    # # 遍历更新
    for i in range(start-1,len(ts_codes)):
        # # 取一个股票编号
        tmp_ts_code = ts_codes[i][0]
        # # 获取日线数据
        res = pro.query('daily', ts_code=tmp_ts_code, start_date=start_date, end_date=end_date)
        # # 数据标准化
        data_dict = dict(json.loads(res.to_json(orient="index", force_ascii=False)))
        tmp_dic = dict()
        for key, info in data_dict.items():
            tmp_dic[info['trade_date']] = info['close']
        tmp_stock = json.dumps(tmp_dic,ensure_ascii=False)
        # # 更新数据库
        db.update_stock_month_by_ts_code(tmp_ts_code, tmp_stock)
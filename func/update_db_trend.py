from func.sak_dbs import SAKSqlDBS
from func.my_calendar import *
import jieba_fast as jieba
import jieba_fast.analyse
import pandas as pd
import os

def get_threshold_value(sentence, positive_dict, negative_dict):
    li = jieba.lcut(sentence, cut_all=True)
    p_threshold_value = 0
    n_threshold_value = 0
    for item in li:
        for key, value in positive_dict.items():
            if item == key:
                p_threshold_value += value[4]
        for key, value in negative_dict.items():
            if item == key:
                n_threshold_value += value[4]
    if (p_threshold_value != 0 or n_threshold_value != 0) and max(p_threshold_value, n_threshold_value) < 1.0:
        if p_threshold_value >= n_threshold_value:
            return 'positive, '+str(p_threshold_value)
        else:
            return 'negative, '+str(n_threshold_value)
    else:
        return 'medium, 0'

def update_db_trend():
    db = SAKSqlDBS()
    sql_query = '''select content from sak_news where date='%s' and company!='[]' '''% get_today_date()
    res = db.exec_sql_query(sql_query)
    if res:
        with open(r'src\Result.txt', 'r',encoding="utf-8") as f:
            dics = f.readlines()
            positive_dict = eval(dics[1])
            negative_dict = eval(dics[2])
        for tup in res:
            news = tup[0]
            trend = get_threshold_value(news, positive_dict, negative_dict)
            db.update_trend_by_content(trend, news)

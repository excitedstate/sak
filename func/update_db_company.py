# encoding=utf-8
from func.sak_dbs import SAKSqlDBS
from func.my_calendar import get_today_date

def update_db_company():
    now_date = get_today_date()
    with open('src/stock_code.txt','r',encoding='utf-8')as f:
        lines = f.readlines()
    com_code = {}
    for line in lines:
        tmp = line.strip().split(',')
        com_code[tmp[1]] = tmp[0]
    db = SAKSqlDBS()
    sql_query = '''select title,content from sak_news where date='%s';''' %now_date
    res = db.exec_sql_query(sql_query)
    test_dic = {ele[0]:ele[1] for ele in res}
    dic_all = {}
    for title,content in test_dic.items():
        tmp_content = []
        for com in com_code.keys():
            if com in content:
                tmp_content.append(com)
        dic_all[title] = tmp_content
    for title, company in dic_all.items():
        print(title, company)
        sql_query = '''update sak_news set company="%s" where title='%s' '''%(str(company),title)
        db.exec_sql_query(sql_query)

# # 已完成历史使命的函数
def get_symbol_name():
    db = SAKSqlDBS()
    sql_query = '''select symbol,name from stock_all'''
    list_ = [ele[0]+','+ele[1] for ele in db.exec_sql_query(sql_query)]
    str_ = '\n'.join(list_)
    with open('../src/stock_code.txt','w',encoding='utf-8') as f:
        f.write(str_)

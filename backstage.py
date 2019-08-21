from func.update_db_stock import update_hk_stock
from func.update_db_news import update_news_daily
from func.update_us_stock import update_us_stock
from func.update_db_company import update_db_company
from func.update_db_trend import update_db_trend
from threading import Thread

def update_news():
    # # 新闻
    update_news_daily()
    # 提取新闻中的公司
    update_db_company()
    # 对新闻进行分析
    update_db_trend()

def main():
    import time
    for i in range(0,10):
        print("即将更新数据...{}s".format(10-i))
        time.sleep(1)
    print("开始更新数据")
    Thread(target=update_news).start()
    # # 美股数据
    # Thread(target=update_us_stock).start()
    # # 港股数据
    # Thread(target=update_hk_stock).start()


if __name__ == '__main__':
    main()
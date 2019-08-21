from PyQt5.QtWidgets import (QApplication, QGraphicsOpacityEffect,
                             QAction, QTextBrowser, QLabel,
                             QFileDialog, QListWidget, QMainWindow, QMessageBox)
from PyQt5.QtGui import (QFont, QIcon, QKeyEvent, QPalette,
                         QBrush, QPixmap)
from PyQt5.QtChart import (QChartView, QLineSeries, QValueAxis, QDateTimeAxis
                           )
from PyQt5.QtCore import (Qt, QTimer, QPointF, QPropertyAnimation,
                          QRect, QDateTime)
from func.get_response import GetResponse
from func.my_calendar import *
from tiplog import TipDialog
from chosen_widget import ChosenDialog
import os, platform
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # # 窗口属性
        self.desktop = QApplication.desktop()
        self.screen = self.desktop.screenGeometry()
        self.s_width = self.screen.height()
        self.s_height = self.screen.width()
        # #创建状态栏
        self.status_bar = self.statusBar()
        # #创建菜单栏
        self.menu_bar = self.menuBar()
        self.import_menu = QAction("&Import")
        self.import_menu.setShortcut("Ctrl+O")
        self.menu_bar.addAction(self.import_menu)
        self.export_menu = QAction("&Export")
        self.export_menu.setShortcut("Ctrl+E")
        self.menu_bar.addAction(self.export_menu)
        self.analyse_menu = QAction("&Analyse")
        self.analyse_menu.setShortcut("Ctrl+A")
        self.menu_bar.addAction(self.analyse_menu)
        self.about_widget = QAction("&About")
        self.about_widget.setShortcut("Ctrl+W")
        self.menu_bar.addAction(self.about_widget)
        # #创建其他控件
        self.chart_view = QChartView(self)
        self.logo = QLabel(self)
        self.text_browser = QTextBrowser(self)
        self.list_view = QListWidget(self)
        self.output = QLabel(self)
        self.sugg = QLabel(self)
        self.export_dialog = TipDialog("OK!", "\n   Export Completed", [300, 300, 300, 100])
        self.about_dialog = TipDialog("About", "\n    SAK", [300, 300, 300, 100])
        # #收集响应
        self.pos = 0
        self.points = list()
        self.response_path = r".\Export\export_data_0"
        self.get_response = GetResponse()
        self.dic_stock, self.dic_news = self.get_response.flow()
        # self.import_from_the_file()
        self.purge_the_response()
        self.qFont = QFont("SimHei", int(self.s_height*(20/self.s_height)))
        if platform.system() == 'Darwin':
            self.qFont = QFont('STHeiti', int(self.s_height*(20/self.s_height)))
        self.op = QGraphicsOpacityEffect()
        # # 表格相关
        self.line_series = QLineSeries()
        self.stock_max = max(list(self.dic_stock.values()))
        self.stock_min = min(list(self.dic_stock.values()))
        self.x_aix, self.y_aix = QDateTimeAxis(), QValueAxis()
        self.update_data_timer = QTimer(self)
        self.update_data_timer.start(100)
        self.update_data_timer.timeout.connect(self.update_data_series)
        self.stock_max = max(list(self.dic_stock.values()))
        self.stock_min = min(list(self.dic_stock.values()))
        # # 动画设计
        self.text_browser_timer = QTimer(self.text_browser)
        self.anim = QPropertyAnimation(self.text_browser, b'geometry')
        self.logo.setPixmap(QPixmap(r"src\logo.png"))
        # # 分析股票结果
        self.content = '平安银行'
        self.companies = list()
        self.trend = '正在评估'
        self.res = []
        # #设置样式和布局
        self.setup()

    def setup(self):
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # # 设置主窗口背景色
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(os.getcwd() + r"\src\background.jpg")))
        # palette.setColor(palette.Background, QColor(0, 0, 0))
        self.setPalette(palette)
        # #布局
        self.s_width = 1960
        self.s_height = 1080
        self.setGeometry(0, 0, self.s_width, self.s_height)
        self.status_bar.setGeometry(int(self.s_width*(20/self.s_width)), int(self.s_height*(1060/self.s_height)), int(self.s_width*(1600/self.s_width)), int(self.s_height*(20/self.s_height)))
        self.menu_bar.setGeometry(int(self.s_width*(0/self.s_width)), int(self.s_height*(0/self.s_height)), int(self.s_width*(1660/self.s_width)), int(self.s_height*(30/self.s_height)))
        self.chart_view.setGeometry(int(self.s_width*(0/self.s_width)), int(self.s_height*(50/self.s_height)), int(self.s_width*(1600/self.s_width)), int(self.s_height*(500/self.s_height)))
        self.logo.setGeometry(int(self.s_width*(400/self.s_width)), int(self.s_height*(640/self.s_height)), int(self.s_width*(782/self.s_width)), int(self.s_height*(332/self.s_height)))
        self.text_browser.setGeometry(int(self.s_width*(10/self.s_width)), int(self.s_height*(540/self.s_height)), int(self.s_width*(1580/self.s_width)), int(self.s_height*(500/self.s_height)))
        self.list_view.setGeometry(int(self.s_width*(1600/self.s_width)), int(self.s_height*(540/self.s_height)), int(self.s_width*(320/self.s_width)), int(self.s_height*(530/self.s_height)))
        self.output.setGeometry(int(self.s_width*(1600/self.s_width)), int(self.s_height*(150/self.s_height)), int(self.s_width*(340/self.s_width)), int(self.s_height*(140/self.s_height)))
        self.sugg.setGeometry(int(self.s_width*(1600/self.s_width)), int(self.s_height*(300/self.s_height)), int(self.s_width*(340/self.s_width)), int(self.s_height*(140/self.s_height)))
        # self.status_bar.setGeometry(20, 1060, 1600, 20)
        # self.menu_bar.setGeometry(0, 0, 1060, 30)
        # self.chart_view.setGeometry(0, 50, 1600, 500)
        # self.logo.setGeometry(400, 640, 782, 332)
        # self.text_browser.setGeometry(10, 540, 1580, 500)
        # self.list_view.setGeometry(1600, 540, 320, 530)
        # self.output.setGeometry(1600, 150, 340, 140)
        # self.sugg.setGeometry(1600, 300, 340, 140)
        # #各控件的状态栏显示
        self.setStatusTip("Stand By")
        self.menu_bar.setStatusTip("Menu")
        self.import_menu.setStatusTip("Import From the File")
        self.export_menu.setStatusTip("Export To the File")
        self.analyse_menu.setStatusTip("Analyse")
        self.chart_view.setStatusTip("Stock Chart Zone")
        self.text_browser.setStatusTip("News Zone")
        self.about_widget.setStatusTip("About,Noc")
        self.list_view.setStatusTip("News List Zone")
        # #设置标题和控件名称
        self.setWindowTitle("Stock Analyse Kits")
        # #设置控件字体和其他样式
        self.list_view.setStyleSheet("color:grey")
        self.menu_bar.setStyleSheet("color:grey")
        self.status_bar.setStyleSheet('color:white')
        self.output.setStyleSheet('color:white')
        self.sugg.setStyleSheet('color:red')
        self.menu_bar.setFont(self.qFont)
        self.list_view.setFont(self.qFont)
        self.text_browser.setFont(self.qFont)
        self.status_bar.setFont(self.qFont)
        tmp = self.qFont
        tmp.setBold(True)
        self.output.setFont(tmp)
        tmp.setPixelSize(int(self.s_height*(40/self.s_height)))
        self.sugg.setFont(tmp)
        self.setWindowIcon(QIcon("./src/app.png"))
        self.output.setAlignment(Qt.AlignCenter)
        self.output.setWordWrap(True)
        self.sugg.setAlignment(Qt.AlignCenter)
        self.sugg.setWordWrap(True)
        self.output.setText("公司:平安银行\n代码:000001\n昨收:14\n上涨趋势明显\n")
        self.sugg.setText("")
        self.list_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # #信号与槽函数
        self.import_menu.triggered.connect(self.import_act)
        self.list_view.itemClicked.connect(self.chosen_item)
        self.export_menu.triggered.connect(self.export_act)
        self.analyse_menu.triggered.connect(self.analyse_act)
        self.about_widget.triggered.connect(self.about_act)
        # # 显示图表
        self.chart_view.chart().createDefaultAxes()
        self.chart_view.chart().legend().hide()
        self.chart_view.chart().setTheme(3)
        self.show_the_chart()
        # #启动
        self.text_browser.hide()
        self.show()

    def about_act(self):
        self.about_dialog.show()

    def show_the_chart(self):
        index = 0
        for date, value in self.dic_stock.items():
            if index > 100:
                break
            self.points.append(QPointF(index, float(value)))
            index += 1
        self.line_series.append(self.points)
        self.chart_view.show()

    def update_data_series(self):
        if self.chart_view.chart().series():
            self.chart_view.chart().removeSeries(self.line_series)
        self.line_series = QLineSeries()
        self.points.clear()
        min_y, max_y, min_x, max_x = 700, 0, '21001231', '20000000'
        index = 0
        # # 输入新点集
        for date, value in self.dic_stock.items():
            if index > 100 + self.pos:
                break
            if index < self.pos:
                index += 1
                continue
            # # 获取到y最大值和最小值 方便设置坐标
            max_y = max_y if value < max_y else value
            min_y = min_y if value > min_y else value
            # # 这两句太笨了
            max_x = max_x if date < max_x else date
            min_x = min_x if date > min_x else date
            self.points.append(QPointF(index, float(value)))
            index += 1
            if index == len(self.dic_stock) - 1:
                self.update_data_timer.stop()
        self.line_series.append(self.points)
        min_date = QDateTime.fromString(min_x, 'yyyyMMdd')
        max_date = QDateTime.fromString(max_x, 'yyyyMMdd')
        self.x_aix = QDateTimeAxis()
        self.x_aix.setRange(min_date, max_date)
        self.x_aix.setFormat('yyyyMMdd')
        self.x_aix.setTickCount(5)  # 设置每个单元格有几个小的分级
        self.y_aix = QValueAxis()
        self.y_aix.setRange(min_y, max_y)
        self.y_aix.setLabelFormat("%0.2f")  # 设置坐标轴坐标显示方式，精确到小数点后两位
        self.y_aix.setTickCount(5)  # 设置y轴有几个量程
        self.chart_view.chart().setAxisX(self.x_aix)
        self.chart_view.chart().setAxisY(self.y_aix)
        self.chart_view.chart().addSeries(self.line_series)
        self.pos += 1

    def analyse_function(self):
        self.sugg.setText("")
        if len(self.companies) == 1:
            # self.trend = self.res[0][1]
            company = self.companies[0]
            self.get_response.value = company
            symbol = self.get_response.db.get_symbol_by_name(company)[0][0]
            self.dic_stock = self.get_response.get_stock()
            self.purge_the_response()
            price = self.dic_stock[get_n_date(-1)]
            if price > self.dic_stock[get_n_date(-2)]:
                tip = '上涨'
            elif price < self.dic_stock[get_n_date(-2)]:
                tip = '下跌'
            else:
                tip = '平'
            info = "公司:%s\n代码:%s\n昨收:%.2f\n%s\n" % (company, symbol, price, tip)
            self.output.setText(info)
            trend_list = str(self.trend).split(",")
            if trend_list[0].strip() == 'positive':
                self.sugg.setStyleSheet('color:red')
                sugg = "推荐," + trend_list[1].strip()[:4]
            elif trend_list[0].strip() == 'negative':
                self.sugg.setStyleSheet('color:green')
                sugg = "不推荐," + trend_list[1].strip()[:4]
            else:
                self.sugg.setStyleSheet('color:white')
                sugg = "无法判断"
            self.sugg.setText(sugg)
        elif len(self.companies) > 1:
            chosen_widget = ChosenDialog('请输入想选择的公司', [800, 300, 320, 80], self.companies, self)
            chosen_widget.show()
            chosen_widget.signal.connect(self.multifactor)
        else:
            self.output.setText("该新闻中不包含已知数据的公司, 请您见谅")

    def analyse_act(self):
        # # 找出当前新闻内容所含公司
        sql_query = '''select company, trend from sak_news where content='%s' ''' % self.content
        self.res = self.get_response.db.exec_sql_query(sql_query)
        self.companies = eval(self.res[0][0])
        self.trend = self.res[0][1]
        self.analyse_function()

    def multifactor(self, company):
        self.companies = [company]
        self.analyse_function()

    def export_act(self):
        file_name = r".\Export\export_data_0"
        while os.path.exists(file_name):
            num = int(file_name[-1]) + 1
            file_name = file_name[:-1] + str(num)
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.dic_stock, ensure_ascii=False))
            file.write("\n")
            file.write(json.dumps(self.dic_news, ensure_ascii=False))
            file.write("\n")
        self.export_dialog.show()

    def import_act(self):
        f_name = QFileDialog.getOpenFileName(self, "Import From File", "~/PycharmProjects/SAK_GUI")
        if f_name[0]:
            try:
                self.response_path = f_name[0]
                self.import_from_the_file()
            except Exception as e:
                reply = QMessageBox.question(self, "Error", str(e) + "\nRetry?",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.import_act()
                else:
                    self.close()

    def chosen_item(self):
        self.text_browser.show()
        self.anim.setDuration(100)
        self.anim.setStartValue(QRect(1570, 540, 0, 505))
        self.anim.setEndValue(QRect(10, 540, 1580, 505))
        self.anim.start()
        self.text_browser.show()
        self.content = self.dic_news[self.list_view.currentItem().text()]
        self.text_browser.setText(self.content)
        self.text_browser_timer.start(10000)
        self.text_browser_timer.timeout.connect(self.text_browser.hide)

    def keyPressEvent(self, k: QKeyEvent) -> None:
        if k.key() == Qt.Key_Q:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.close()
        if k.key() == Qt.Key_C:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.text_browser.hide()
        if k.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, "Exit?", "Are you sure to exit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def import_from_the_file(self):
        f = open(self.response_path, "r", encoding="utf-8")
        lines = f.readlines()
        self.dic_stock = dict(json.loads(str(lines[0]).strip()))
        self.dic_news = dict(json.loads(str(lines[1]).strip()))
        f.close()
        self.purge_the_response()

    def purge_the_response(self):
        if self.pos == 0:
            self.list_view.addItems(self.dic_news.keys())
            self.dic_stock = self.generate_mapping(get_the_calendar(2019, 2020))
        else:
            self.list_view.clear()
            self.chart_view.chart().removeSeries(self.line_series)
            self.update_data_timer.start(100)
            self.pos = 0
            self.purge_the_response()
            self.show_the_chart()

    def generate_mapping(self, calender: list):
        '''
            接下来的方法提供了规范化x轴数据的可能
        '''
        min_date = min(list(self.dic_stock.keys()))
        min_date = min_date if min_date < '20190101' else '20190101'
        max_date = max(list(self.dic_stock.keys()))
        tmp_dict = {}
        for date in calender:
            if date < min_date:
                continue
            if date > max_date:
                break
            tmp_dict[date] = self.get_nn_stock(date, calender)
        min_date = max_date
        max_date = get_today_date()
        if min_date == max_date:
            return tmp_dict
        else:
            self.dic_stock = tmp_dict
        for date in calender:
            if date < min_date:
                continue
            if date > max_date:
                break
            tmp_dict[date] = self.get_np_stock(date, calender)
        return tmp_dict

    def get_nn_stock(self, date, calendar: list):
        if self.dic_stock.get(date) != None:
            return self.dic_stock[date]
        else:
            return self.get_nn_stock(calendar[calendar.index(date) + 1], calendar)

    def get_np_stock(self, date, calendar: list):
        if self.dic_stock.get(date) != None:
            return self.dic_stock[date]
        else:
            return self.get_nn_stock(calendar[calendar.index(date) - 1], calendar)

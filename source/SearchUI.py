'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-04-10 23:50:38
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\SearchUI.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2023~2024 by HDJ, All Rights Reserved. 
'''
import os
import re
import sys
import typing
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QLineEdit, QTreeWidget, QTreeWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Simple_Qt import Label, PushButton, Menu, Action, PackingModificationMethod
from DataProtector import IMAGE_FOLDER_PATH, style_css, style_js, config_js


class SearchUI(QDialog):
    """ 歌曲搜索界面 """

    def __init__(self, main_window = None, parent = None, width=1250, height=950) -> None:
        super().__init__()
        # 一级UI对象传入
        self.main_window = main_window
        self.parent = parent
        

        # 设置二级UI
        self.setWindowTitle("歌曲查询中...")
        self.setFixedSize(width, height)  # 禁止修改窗口大小
        self.setWindowIcon(QIcon(config_js['SearchUIIcon']))
        PackingModificationMethod.set_background_image(self, config_js['SearchUIBackGround'])
        PackingModificationMethod.set_desktop_center(self)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # 方法绑定
        self.build_search_platform()
        self.build_menu()

        # 底层变量
        self.onclick_song_number = None  # 鼠标选中的序号

    def build_menu(self) -> None:
        """ 创建菜单用于呼出二级UI(SearchUI) """

        # 二级菜单
        action_open_searchUI = Action.create(
            parent=self.parent,
            text="打开查询界面",
            triggered_callback=lambda: self.exec_rewrite(),
            Icon_path=IMAGE_FOLDER_PATH + r"\Beauty With Headset.png",
            superior=self.parent.menu_setting
        )

    def exec_rewrite(self) -> None:
        """ 自定义的窗口呼出方法 """
        self.label_current_folder.setText(os.path.basename(config_js['current_songlist_path']))
        self.show()
        self.main_window.showMinimized()

    def searching(self, input_song_name) -> None:
        """ 搜索(二级UI按钮绑定操作) """
        input_song_name = self.lineEdit_input_song_title.text()
        if len(input_song_name) > 0:
            self.treeview_search_result.clear()  # 清除图表所有项
            num = 0
            for key, value in self.main_window.current_songlist.items():  # 在循环中处理键和值,items()方法将返回 包含字典中的键值对的 可迭代对象
                # 判断用户输入内容与音乐文件名是否有重叠
                filename = os.path.basename(value)
                if input_song_name in filename:
                    num += 1
                    # 用正则表达式来提取歌手的名字
                    pattern = r"(.+?)--(.+?)(" + "|".join(re.escape(suffix) for suffix in config_js['audio_file_suffixes']) + ")$" # 将配置文件中的所有后缀转译,拼接,添加到末尾
                    result = re.search(pattern, filename)
                    singer_name = "暂无"
                    if result:
                        # 在文件名中找到最后一个 '--' 分隔符的索引
                        last_separator_index = filename.rfind("--")
                        # 获取歌曲名和歌手名
                        song_name = filename[:last_separator_index]
                        singer_name = filename[last_separator_index +2:result.start(2) + len(result.group(2))]
                        file_extension = result.group(3)
                        # 根据文件拓展名处理歌曲名
                        if file_extension == '.flac': # 无损压缩
                            song_name = song_name + '(FLAC)'
                        elif file_extension == '.wav': # 无损未压缩
                            song_name = song_name + '(WAV)'
                        elif file_extension == '.ogg': # 多媒体
                            song_name = song_name + '(OGG)'
                    else:
                        song_name, _ = os.path.splitext(filename)
                    # 将搜索内容显示到图表中
                    self.add_tree_item(
                        f'{key}', # 音频文件在目录中的序号
                        song_name,  # 提取的歌曲名
                        singer_name # 提取的歌手名
                    )
            if num <= 0:
                QMessageBox.warning(self, '搜素结束', '很抱歉,没有找到歌曲', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'ERROR', '您未输入需查询的歌曲, 请输入后搜索!', QMessageBox.Retry)

    def add_tree_item(self, text1, text2, text3) -> None:
        """ 自定义的树形图方法,用于批量添加项目 """
        item = QTreeWidgetItem(self.treeview_search_result)
        item.setText(0, text1)
        item.setText(1, text2)
        item.setText(2, text3)

    def onclick(self, item, column) -> None:
        """ 二级UI树型视图的鼠标单击点击事件绑定操作 """
        # 获取树型视图被点击行中第一列的信息(获取歌曲序号)
        self.onclick_song_number = int(item.text(0))

        if self.onclick_song_number is not None:
            self.main_window.current_music_number = self.onclick_song_number
        else:
            QMessageBox.critical(
                self, 'ERROR', '请点击歌曲进行选定!', QMessageBox.Retry)

    def search_ui_play(self) -> None:
        """ 播放(二级UI按钮绑定操作),用于播放选中的歌曲"""
        if self.onclick_song_number is None or isinstance(self.main_window.current_music_number, str):
            QMessageBox.warning(self, 'Warning', '您未选定歌曲', QMessageBox.Ok)
        else:
            if self.main_window.current_music_number is not None:
                self.main_window.player.pause()
                self.main_window.player.delete()
            self.main_window.play_song()
            # 按钮文本显示为"暂停"
            self.main_window.button_pause_or_begin.setText('暂停')
            # 将查询界面关闭
            self.close()
            # 将一级UI界面还原到上一次最小化前的位置
            self.main_window.showNormal()
            # 将鼠标获取到的序号清除
            self.onclick_song_number = None

    def build_search_platform(self) -> None:
        """ 二级UI(SearchUI)搭建,使用绝对布局 """

        # 主体标签设置
        self.label_SearchUI_main_text = Label.create(
            parent=self, text='@ 歌曲查找界面 #',
            Geometry=(400, 0, 1000, 100),
            ObjectName=style_js["label_SearchUI_main_text"],
            StyleSheet=style_css
        )

        # F1
        # "当前文件夹(库名):"标签
        self.label_folder_path_text = Label.create(
            parent=self, text='当前文件夹(库名):',
            Alignment=Qt.AlignVCenter,
            Geometry=(150, 100, 300, 60),
            ObjectName=style_js["label_folder_path_text"],
            StyleSheet=style_css
        )

        # 显示当前文件夹路径的标签
        self.label_current_folder = Label.create(
            parent=self, text=os.path.basename(config_js['current_songlist_path']),
            Alignment=Qt.AlignVCenter,
            Geometry=(450, 100, 550, 60),
            ObjectName=style_js["label_current_folder"],
            StyleSheet=style_css
        )

        # 输入提示文本
        self.label_input_reminder_text = Label.create(
            parent=self, text='请输入歌曲/歌手名称:',
            Alignment=Qt.AlignVCenter,
            Geometry=(100, 160, 350, 60),
            ObjectName=style_js["label_input_reminder_text"],
            StyleSheet=style_css
        )

        # 输入框
        self.lineEdit_input_song_title = QLineEdit(parent=self)
        self.lineEdit_input_song_title.setPlaceholderText('输入信息,点击搜索')
        self.lineEdit_input_song_title.setGeometry(450, 160, 450, 60)
        self.lineEdit_input_song_title.setObjectName("QLineEdit--1")
        self.lineEdit_input_song_title.setStyleSheet(style_css)

        # 搜索按钮
        self.button_searching = PushButton.create(
            parent=self, text='搜索',
            clicked_callback=lambda: self.searching(
                self.lineEdit_input_song_title.text()),
            setFocusPolicy=Qt.TabFocus,
            Geometry=(900, 160, 100, 60),
            ObjectName=style_js["button_searching"],
            StyleSheet=style_css
        )

        # F2 (用于显示搜索结果的树形图)
        self.treeview_search_result = QTreeWidget(self)
        self.treeview_search_result.setGeometry(100, 250, 1000, 300)
        # 树型视图表头文本设置
        self.treeview_search_result.setHeaderLabels(["序号", "歌曲名称", "歌手"])
        self.treeview_search_result.setHeaderHidden(True)  # 隐藏表头
        # 禁止拖拽表头
        self.treeview_search_result.header().setSectionsMovable(False)
        # 禁止拉伸表头
        self.treeview_search_result.header().setSectionResizeMode(0, QHeaderView.Fixed)
        self.treeview_search_result.header().setSectionResizeMode(1, QHeaderView.Fixed)
        self.treeview_search_result.header().setSectionResizeMode(2, QHeaderView.Fixed)
        # 设置列宽
        self.treeview_search_result.setColumnWidth(0, 120)
        self.treeview_search_result.setColumnWidth(1, 650)
        self.treeview_search_result.setColumnWidth(2, 340)
        # 设置样式
        self.treeview_search_result.setObjectName("treeview--1")
        self.treeview_search_result.setStyleSheet(style_css)
        # 鼠标单击(点击操作绑定)
        self.treeview_search_result.itemClicked.connect(self.onclick)

        # 播放所选歌曲按钮
        self.button_play_selected_song = PushButton.create(
            parent=self, text='播放',
            clicked_callback=self.search_ui_play,
            setFocusPolicy=Qt.TabFocus,
            Geometry=(570, 550, 100, 60),
            ObjectName=style_js["button_play_selected_song"],
            StyleSheet=style_css
        )

        # F3 注意事项文本标签
        self.label_use_attention_text = Label.create(
            parent=self,
            text='注意事项:'
            '\n1.该功能仅限于在所添加的文件夹中搜索歌曲(序号按文件夹内顺序),而非爬虫!'
            '\n2.该搜索功能仅进行宽泛搜索,罗列,并不能精确导向.'
            '\n3.使用步骤: 输入搜索内容,点击所搜按钮,在所罗列的内容中用\n'
            '鼠标左键单击选定需要播放的歌曲,点击播放按钮即可.'
            '\n4.点击播放后,该搜索界面会自动关闭,如有二次需求请重新进入.'
            '\n5.并不是所有的音乐文件名都符合规范,为了好的体验请保持文件名格式为:'
            '\n歌曲名(歌曲信息)--歌手1&歌手2...(歌手信息).后缀名',
            Alignment=Qt.AlignLeft,
            Geometry=(110, 650, 1200, 300),
            ObjectName=style_js["label_use_attention_text"],
            StyleSheet=style_css
        )

    @typing.override
    def closeEvent(self, event) -> None:
        """ 二级UI窗口关闭方法重写 """
        # 将一级UI界面还原到上一次最小化前的位置
        self.main_window.showNormal()
        # 调用父类的 closeEvent 方法，确保原有的行为能够正常执行
        super().closeEvent(event)



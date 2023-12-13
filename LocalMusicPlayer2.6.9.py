'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2023-12-13 14:41:52
version: 2.6.9
FilePath: \python\py.1求道境\音乐随机播放器\LocalMusicPlayer.py
Description: 
此代码实现的是一个基于Python与本地储存的mp3文件的本地播放器.
其余参数可根据注释,慎重更改.

				/*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				\*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) ${2023} by ${HDJ}, All Rights Reserved. 
'''
import time
import glob
import os
import random
import re
import threading
import json
import sys
import functools
import typing
# 需要cmd安装
import pyglet
import pynput.keyboard
import keyboard
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QLineEdit, QTreeWidget, QTreeWidgetItem, QHeaderView, QMessageBox, 
    QMenu, QAction
    )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

from MyWidgetMethod import PackingCreateMethod, PackingModificationMethod


# 声明全局变量
WORKING_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__)) # 获取当前文件所在目录的绝对路径
# 读取 PlayerConfig.json 文件并加载为 JSON 对象
with open(WORKING_DIRECTORY_PATH + r'\PlayerConfig.json', 'r', encoding='utf-8') as config_json:
    config_js = json.load(config_json)
with open(WORKING_DIRECTORY_PATH + r'\PlayerStyle.json', 'r', encoding='utf-8') as style_json:
    style_js = json.load(style_json)
# 读取 PlayerStyle.css 文件内容为文本
with open(WORKING_DIRECTORY_PATH + r'\PlayerStyle.css', 'r', encoding='utf-8') as player_style_css:
    style_css = player_style_css.read()


class ApplicationWindow(QMainWindow): 
    """ 
    简单的本地播放器

    主UI界面
    """
    def __init__(self, width=1236, height=764) -> None:
        super().__init__()
        # 一级UI设置
        self.setWindowTitle("Music Player")
        self.setFixedSize(width, height)  # 禁止修改窗口大小
        self.setWindowIcon(QIcon(WORKING_DIRECTORY_PATH + r"\player.png"))
        PackingModificationMethod.set_background_image(self, WORKING_DIRECTORY_PATH + r"\Golden Buddha.png")
        PackingModificationMethod.set_desktop_center(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)# 一级UI界面的层次设置, False置于最底部, True置顶
        #self.setWindowFlag(Qt.FramelessWindowHint)

        # 方法绑定
        self.build_platform()

        # 底层变量
        self.player = pyglet.media.Player()  # 播放器
        self.music_folder_path = config_js['music_folder_path'] # 获取音乐文件夹的绝对路径
        self.play_dict = config_js['play_dict']  # 播放字典
        self.current_music_number = ( # 当前播放的音乐文件序号
            config_js['current_music_number'] 
            if not isinstance(config_js['current_music_number'], int) 
            else f'*{config_js['current_music_number']}*'
        )  
        self.current_position = config_js['current_position']  # 当前(文件的)播放位置
        self.need_cycle = config_js['need_cycle']  # 是否循环播放的标志
        self.file_total_time = config_js['file_total_time']  # 音乐文件总时长
        self.key_press_programme = config_js['key_press_programme'] # 键盘快捷方案序号

        #绑定线程
        self.is_over_monitor = IsOverMonitor(self)
        self.key_board_listener = KeyboardListener(self)
        self.data_protector = DataProtector(self)

    def update_song_list(self) -> None:
        """ 更新音乐列表 """

        # 创建一个空字典
        self.play_dict = {}
        # 导入音乐文件夹
        music_file_path = self.music_folder_path
        # 获取全部mp3文件的路径列表
        mp3_files_list = glob.glob(os.path.join(music_file_path, '*.mp3'))
        # 创建播放字典
        for music_number, music_path in enumerate(mp3_files_list, start=1):
            self.play_dict[f'{music_number}'] = f'{music_path}'

    def play_song(self, music_position=0) -> None:
        """ 
        播放音乐 
        
        基于音乐文件路径 与 pyglet.media.player.Player的播放操作
        """
        try:
            # 加载音乐文件
            music_file_path = self.play_dict.get(f'{self.current_music_number}')           
        except TypeError:
            QMessageBox.critical(self, '温馨提示', '切换文件夹后,请在查找界面选择歌曲或点击随机播放.')
        else:
            # 根据绝对路径创建音频文件的MediaSource对象
            music = pyglet.media.load(music_file_path)
            # 获取音频文件总时长
            self.file_total_time = int(music.duration)
            # 创建播放器
            self.player = pyglet.media.Player()
            # 将MediaSource对象添加到播放器(player)
            self.player.queue(music)
            # 调整播放位置
            self.player.seek(music_position)
            # 开始播放
            self.player.play()
            # 更改当前正在播放标签的文本
            self.change_label_current_play_content()

    def change_label_current_play_content(self) -> None:
        """ 用于更改"当前播放歌曲"标签显示内容的操作 """
        music_file_path = self.play_dict.get(f'{self.current_music_number}')
        music_file_name = os.path.basename(music_file_path)
        self.label_current_play_content.setText(music_file_name.replace('.mp3', ''))

     
    def random_play(self) -> None:
        """ 随机播放(按钮绑定操作) """
        if self.current_music_number is not None:
            self.player.pause()
        if isinstance(self.current_music_number, str):  # 确保解密/确保对象类型为int
            self.current_music_number = int(self.current_music_number.replace('*', ''))
        self.current_music_number = random.randint(1, len(self.play_dict))
        self.play_song()
        # 按钮文本显示为"暂停"
        self.button_pause_or_begin.setText('暂停')

    def previous_play(self) -> None:
        """ 上一首(按钮绑定操作) """
        if self.current_music_number is None:
            QMessageBox.critical(self, '错误', '请点击开始播放')
        else:
            self.player.pause()
            if isinstance(self.current_music_number, str):  # 确保解密/确保对象类型为int
                self.current_music_number = int(self.current_music_number.replace('*', ''))
            self.current_music_number -= 1
            if self.current_music_number == 0:
                self.current_music_number = len(self.play_dict)
            self.play_song()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

    def next_play(self) -> None:
        """ 下一首(按钮绑定操作) """
        if self.current_music_number is None:
            QMessageBox.critical(self, '错误', '请点击开始播放')
        else:
            self.player.pause()
            if isinstance(self.current_music_number, str):  # 确保解密/确保对象类型为int
                self.current_music_number = int(self.current_music_number.replace('*', ''))
            self.current_music_number += 1
            if self.current_music_number > len(self.play_dict):
                self.current_music_number = 1
            self.play_song()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

    def music_pause(self) -> None:
        """ 暂停||开始(按钮绑定操作) """
        
        # 开始路径1:如果之前无播放内容,则随机播放  QwQ:克服选择困难症
        if self.current_music_number is None:
            self.random_play()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

        # 开始路径2:之前有播放内容被暂停,点击按钮继续播放
        elif isinstance(self.current_music_number, str):  # QwQ:通过类型的转化来区分路径
            self.current_music_number = int(self.current_music_number.replace('*', ''))
            self.play_song(self.current_position)
            self.current_position = 0.0
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

        # 当前有文件正在播放,点击按钮暂停
        else:
            self.current_position = self.player.time
            self.player.pause()
            # QwQ将当前播放序号在转类型的时候稍微加密
            self.current_music_number = f'*{self.current_music_number}*'
            # 按钮文本显示为"开始"
            self.button_pause_or_begin.setText('开始')

    def single_cycle_play(self) -> None:
        """ 单曲循环(按钮绑定操作) """
        if self.current_music_number is None:
            QMessageBox.critical(self, '错误', '请点击开始播放')
        else:
            # 点击开始循环
            if not self.need_cycle:
                self.need_cycle = True
                # 将文本更改为"cycling",按钮显示为凹陷
                self.button_single_loop.setText('cycling')                                             
            elif self.need_cycle:
                self.need_cycle = False
                # 将文本更改为"单曲循环",按钮显示为凸起
                self.button_single_loop.setText('单曲循环')

    def confirm_to_quit(self) -> None:
        """ 确认退出(按钮绑定操作) """
        reply = QMessageBox.question(self, '温馨提示', '记得给 作者:HDJ 一颗小星星', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()  # 使用close方法来关闭窗口

    def build_platform(self) -> None:
        """ 一级UI搭建(使用绝对布局,写死UI界面) """

        # 创建主体文字标签
        self.label_MainWindow_main_text = PackingCreateMethod.my_label(
            parent=self, text='Q*& 私人专属音乐播放工具 Qwq', 
            Alignment = Qt.AlignHCenter | Qt.AlignBottom, 
            Geometry = (18, 30, 1200, 100),
            ObjectName = "label--1_1",
            StyleSheet =style_css
        )

        # F1 创建当前正在播放内容的显示器
        # "正在播放"标签
        self.label_current_play_text = PackingCreateMethod.my_label(
            parent=self, text='正在\n播放', 
            Alignment = Qt.AlignHCenter | Qt.AlignVCenter,
            Geometry = (270, 290, 100, 100),
            ObjectName = "label--2_1",
            StyleSheet =style_css
        )

        # 显示当先正在播放歌曲名称的标签
        self.label_current_play_content = PackingCreateMethod.my_label(
            parent=self, text=config_js['current_music_name'], 
            WordWrap = True, # 允许自动换行 QwQ:这个很重要
            Alignment = Qt.AlignVCenter | Qt.AlignLeft,
            TextInteractionFlags = Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard, # 允许鼠标,键盘与标签文本交互
            Geometry = (410, 265, 650, 150),
            ObjectName = "label--3_1",
            StyleSheet =style_css
        )
        
        #上一首按钮
        self.button_previous = PackingCreateMethod.my_button(
            parent=self, text='上一首',
            clicked_callback = self.previous_play,
            Geometry = (400, 600, 150, 80),
            ObjectName = "button--1",
            StyleSheet = style_css
        )

        #下一首按钮
        self.button_next = PackingCreateMethod.my_button(
            parent=self, text='下一首',
            clicked_callback = self.next_play,
            Geometry = (700, 600, 150, 80),
            ObjectName = "button--2",
            StyleSheet = style_css
        )

        #开始/暂停按钮
        self.button_pause_or_begin = PackingCreateMethod.my_button(
            self, text='开始',
            clicked_callback = self.music_pause,
            Geometry = (550, 600, 150, 80),
            ObjectName = "button--3",
            StyleSheet = style_css
        )
        
        # F3
        # 随机播放按钮
        self.button_shuffle_play = PackingCreateMethod.my_button(
            parent=self, text='随机播放',
            clicked_callback = self.random_play,
            Geometry = (475, 520, 150, 80),
            ObjectName = "button--4",
            StyleSheet = style_css
        )                                               

        # 单曲循环按钮
        self.button_single_loop = PackingCreateMethod.my_button(
            parent=self, text=('单曲循环' if config_js['need_cycle'] is False else 'cycling'),
            clicked_callback = self.single_cycle_play,
            Geometry = (625, 520, 150, 80),
            ObjectName = "button--5",
            StyleSheet = style_css
        )
 
        # F4
        # 退出按钮
        self.button_quit = PackingCreateMethod.my_button(
            parent=self, text='退出',
            clicked_callback = self.confirm_to_quit,
            Geometry = (0, 735, 50, 30),
            ObjectName = "button--8",
            StyleSheet = style_css
        )

        # 警告标签
        self.label_warning_text = PackingCreateMethod.my_label(
            parent=self, text='请不要点击过快,UI响应需要时间!此工具仅用于学术交流!', 
            Alignment = Qt.AlignCenter,
            Geometry = (250, 680, 800, 100),
            ObjectName = "label--4_1",
            StyleSheet =style_css
        )

        # 菜单设置
        # 菜单栏
        self.menubar = self.menuBar()  # 创建菜单栏对象
        self.menubar.setFixedHeight(40)
        self.menubar.setObjectName('menubar--1')
        self.menubar.setStyleSheet(style_css)

        #一级菜单创建操作
        menu_setting = SettingMenu(self)

        menu_chang_folder_path = ChangeFolderMenu(self)

        menu_search_for_target_song = SearchUI(self)
        
        menu_change_key_press_programme = ChangeKeyPressProgrammeMenu(self)

    # 窗口跟随鼠标移动(单击拖动窗口)
    def mousePressEvent(self, event) -> None:
        """ 一级UI的鼠标点击事件 """

        # 记录鼠标按下时的位置
        self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event) -> None:
        """ 一级UI的鼠标移动事件 """
        if hasattr(self, 'drag_start_position'):
            # 计算鼠标移动的距离
            delta = event.globalPos() - self.drag_start_position

            # 更新窗口位置
            new_position = self.pos() + delta
            self.move(new_position)

            # 更新起始位置，以便下一次移动计算
            self.drag_start_position = event.globalPos()

    def mouseReleaseEvent(self, event) -> None:
        """ 一级UI的鼠标释放事件 """
        
        # 鼠标释放时清空起始位置
        if hasattr(self, 'drag_start_position'):
            delattr(self, 'drag_start_position')


class SearchUI(QDialog):
    """ 歌曲搜索界面 """
    def __init__(self, main_window, width=1250, height=950) -> None:
        super().__init__()
        #一级UI对象传入
        self.main_window = main_window

        # 设置二级UI
        self.setWindowTitle("歌曲查询中...")
        self.setFixedSize(width, height)  # 禁止修改窗口大小
        self.setWindowIcon(QIcon(WORKING_DIRECTORY_PATH + r"\Beauty With Headset.png"))
        PackingModificationMethod.set_background_image( self, WORKING_DIRECTORY_PATH + r"\Beauty With Headset.png")
        PackingModificationMethod.set_desktop_center(self)
        #self.setWindowFlag(Qt.FramelessWindowHint)
        # 方法绑定
        self.build_search_platform()
        self.build_menu()

        # 底层变量
        self.onclick_song_number = None  # 鼠标选中的序号

    def build_menu(self) -> None:
        """ 创建菜单用于呼出二级UI(SearchUI) """

        # 一级菜单
        self.menu_search_for_target_song = QMenu('查询界面', self.main_window)
        # 二级菜单
        entry_action = QAction('打开查询界面', self.main_window)
        entry_action.triggered.connect(lambda: self.exec_rewrite())
        # 向一级菜单添加二级菜单(action)
        self.menu_search_for_target_song.addAction(entry_action)
        # 向菜单栏添加一级菜单
        self.main_window.menubar.addMenu(self.menu_search_for_target_song)

    def exec_rewrite(self) -> None:
        """ 自定义的窗口呼出方法 """
        self.label_current_folder.setText(os.path.basename(config_js['music_folder_path']))
        self.show()
        self.main_window.showMinimized()

    def searching(self, input_song_name) -> None:  
        """ 搜索(二级UI按钮绑定操作) """
        input_song_name = self.lineEdit_input_song_title.text()
        if len(input_song_name) > 0:  
            self.treeview_search_result.clear()  # 清除图表所有项
            num = 0
            for key, value in self.main_window.play_dict.items():  # 在循环中处理键和值,items()方法将返回 包含字典中的键值对的 可迭代对象
                if input_song_name in os.path.basename(value):  # 判断用户输入内容与音乐文件名是否有重叠
                    num += 1
                    # 用正则表达式来提取歌手的名字
                    singer_name = "暂无"
                    pattern = r"--(.+?)\.mp3"
                    result = re.search(pattern, os.path.basename(value))
                    if result:
                        singer_name = result.group().replace("--", '').replace(".mp3", '')
                    # 将搜索内容显示到图表中
                    self.add_tree_item(
                        f'{key}', 
                        os.path.basename(self.main_window.play_dict[key]).replace(".mp3", '').split("--")[0],
                        f'{singer_name}'
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
            QMessageBox.critical(self, 'ERROR', '请点击歌曲进行选定!', QMessageBox.Retry)

    def search_ui_play(self) -> None:
        """ 播放(二级UI按钮绑定操作),用于播放选中的歌曲"""
        if self.onclick_song_number is None or isinstance(
            self.main_window.current_music_number, str
        ):
            QMessageBox.warning(self, 'Warning', '您未选定歌曲', QMessageBox.Ok )
        else:
            if self.main_window.current_music_number is not None:
                self.main_window.player.pause()
                self.main_window.player.delete()
            #self.main_window.change_label_current_play_content()
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
        self.label_SearchUI_main_text = PackingCreateMethod.my_label(
            parent=self, text='@ 歌曲查找界面 #', 
            Geometry = (400, 0, 1000, 100),
            ObjectName = "label--5_1",
            StyleSheet =style_css
        )
    
        # F1
        # "当前文件夹(库名):"标签
        self.label_folder_path_text = PackingCreateMethod.my_label(
            parent=self, text='当前文件夹(库名):', 
            Alignment = Qt.AlignVCenter,
            Geometry = (150, 100, 300, 60),
            ObjectName = "label--6_1",
            StyleSheet =style_css
        )
        
        # 显示当前文件夹路径的标签
        self.label_current_folder = PackingCreateMethod.my_label(
            parent=self, text=os.path.basename(config_js['music_folder_path']), 
            Alignment = Qt.AlignVCenter,
            Geometry = (450, 100, 550, 60),
            ObjectName = "label--7_1",
            StyleSheet =style_css
        )

        # 输入提示文本
        self.label_input_reminder_text = PackingCreateMethod.my_label(
            parent=self, text='请输入歌曲/歌手名称:', 
            Alignment = Qt.AlignVCenter,
            Geometry = (100, 160, 350, 60),
            ObjectName = "label--8_1",
            StyleSheet =style_css
        )

        # 输入框
        self.lineEdit_input_song_title = QLineEdit(parent=self)
        self.lineEdit_input_song_title.setPlaceholderText('输入信息,点击搜索') 
        self.lineEdit_input_song_title.setGeometry(450, 160, 450, 60) 
        self.lineEdit_input_song_title.setObjectName("QLineEdit--1")
        self.lineEdit_input_song_title.setStyleSheet(style_css)

        # 搜索按钮
        self.button_searching = PackingCreateMethod.my_button(
            parent=self, text='搜索',
            clicked_callback = lambda: self.searching(self.lineEdit_input_song_title.text()),
            setFocusPolicy = Qt.TabFocus,
            Geometry = (900, 160, 100, 60),
            ObjectName = "button--6",
            StyleSheet = style_css
        )

        # F2 (用于显示搜索结果的树形图)
        self.treeview_search_result = QTreeWidget(self)
        self.treeview_search_result.setGeometry(100, 250, 1000, 300)
        # 树型视图表头文本设置
        self.treeview_search_result.setHeaderLabels(["序号", "歌曲名称", "歌手"])
        self.treeview_search_result.setHeaderHidden(True) # 隐藏表头
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
        self.button_play_selected_song = PackingCreateMethod.my_button(
            parent=self, text='播放',
            clicked_callback = self.search_ui_play,
            setFocusPolicy = Qt.TabFocus,
            Geometry = (570, 550, 100, 60),
            ObjectName = "button--7",
            StyleSheet = style_css
        )

        # F3 注意事项文本标签
        self.label_use_attention_text = PackingCreateMethod.my_label(
            parent=self, 
            text='注意事项:'
            '\n1.该功能仅限于在所添加的文件夹中搜索歌曲(序号按文件夹内顺序),而非爬虫!'
            '\n2.该搜索功能仅进行宽泛搜索,罗列,并不能精确导向.'
            '\n3.使用步骤: 输入搜索内容,点击所搜按钮,在所罗列的内容中用\n'
            '鼠标左键单击选定需要播放的歌曲,点击播放按钮即可.'
            '\n4.点击播放后,该搜索界面会自动关闭,如有二次需求请重新进入.'
            '\n5.并不是所有的音乐文件名都符合规范,为了好的体验请保持文件名格式为:'
            '\n歌曲名(歌曲信息)--歌手1&歌手2...(歌手信息).mp3', 
            Alignment = Qt.AlignLeft,
            Geometry = (110, 650, 1200, 300),
            ObjectName = "label--9_1",
            StyleSheet =style_css
        )
 
    def closeEvent(self, event) -> None:
        """ 二级UI窗口关闭方法重写 """
        print("SearchUI: closeEvent")
        # 将一级UI界面还原到上一次最小化前的位置
        self.main_window.showNormal()
        # 调用父类的 closeEvent 方法，确保原有的行为能够正常执行
        super().closeEvent(event)


class ChangeFolderMenu(object):
    """ 一级菜单--更改文件夹(歌单) """
    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window
        # 底层变量
        self.menu_change_folder_path = None  # 一级菜单对象
        # 方法绑定
        self.build_menu()

    def build_menu(self) -> None:
        """ 创建菜单,用于显示用户自定义的歌单 """
        
        # 一级菜单
        self.menu_change_folder_path = QMenu('更改文件夹', self.main_window)
        
        # 在config_js的music_folders_path中找到所有一级菜单名
        secmenu_names = [js_secmenu[0] for js_secmenu in config_js["music_folders_path"]]        
        # 以二级菜单个数作为循环结束条件
        for i in range(0, len(config_js["music_folders_path"])):
            # 创建二级菜单 
            secmenu = QMenu(secmenu_names[i], self.main_window) 
            # 在config_js的music_folders_path中找到当先二级菜单下的所有三级菜单列表
            actions = config_js["music_folders_path"][i][1:]
            # 创建三级菜单
            for action_name, action_path in actions:
                if isinstance(action_name, str) and isinstance(action_path, str):
                    action = QAction(f'{action_name}',  self.main_window)
                    # 使用functools.partial动态的传递参数
                    action.triggered.connect(functools.partial(self.change_music_path, action_path))
                    # 将三级菜单添加到二级菜单
                    secmenu.addAction(action)
            # 将二级菜单添加到一级菜单
            self.menu_change_folder_path.addMenu(secmenu)

        # 向菜单栏添加一级菜单
        self.main_window.menubar.addMenu(self.menu_change_folder_path)
        
    def change_music_path(self, path:str) -> None:
        """ 更改文件夹路径(菜单项绑定操作),用于切换歌单 """
        self.main_window.music_folder_path = path
        self.main_window.update_song_list()


class ChangeKeyPressProgrammeMenu(object):
    """ 一级菜单--更改键盘快捷方案"""
    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window
        # 底层变量
        self.menu_change_key_press_programme = None
        # 方法绑定
        self.build_menu()

    def build_menu(self) -> None:
        """ 创建菜单,用于显示键盘快捷方案"""
        #一级菜单
        self.menu_change_key_press_programme = QMenu('快捷方式', self.main_window)

        # 二级菜单
        default_action_1 = QAction('关闭快捷方式', self.main_window)
        default_action_1.triggered.connect(lambda: setattr(self.main_window, 'key_press_programme', None))
        default_action_2 = QAction('主键盘+方向键', self.main_window)
        default_action_2.triggered.connect(lambda: setattr(self.main_window, 'key_press_programme', '1'))
        default_action_3 = QAction('Ctrl+主键盘', self.main_window)
        default_action_3.triggered.connect(lambda: setattr(self.main_window, 'key_press_programme', '2'))
        default_action_4 = QAction('数字键盘', self.main_window)
        default_action_4.triggered.connect(lambda: setattr(self.main_window, 'key_press_programme', '3'))
        default_action_5 = QAction('Ctrl+数字键盘', self.main_window)
        default_action_5.triggered.connect(lambda: setattr(self.main_window, 'key_press_programme', '4'))
        
        # 向一级菜单添加二级菜单(action)
        self.menu_change_key_press_programme.addAction(default_action_1)
        self.menu_change_key_press_programme.addAction(default_action_2)
        self.menu_change_key_press_programme.addAction(default_action_3)
        self.menu_change_key_press_programme.addAction(default_action_4)
        self.menu_change_key_press_programme.addAction(default_action_5)

        #向菜单栏添加一级菜单
        self.main_window.menubar.addMenu(self.menu_change_key_press_programme)

        #绑定操作(可以被setattr()替换)
    #def change_key_press_programme(self, programme_number):
        #self.main_window.key_press_programme = programme_number


class SettingMenu(object):
    """ 一级菜单--设置 """
    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window
        # 底层变量
        self.menu_setting = None  # 一级菜单对象
        # 方法绑定
        self.build_menu()
    
    def build_menu(self) -> None:
        # 创建一级菜单
        self.menu_setting = QMenu("⚙️", self.main_window)
        
        configuration_files_menu = self.ConfigurationFilesMenu(self)

###############################################################################
        # 创建二级菜单(样式选择)
        secmenu_style_selection = QMenu(" ❖样式", self.main_window)

        # 将二级菜单(样式选择)添加到一级菜单
        self.menu_setting.addMenu(secmenu_style_selection)


        # 将一级菜单添加到菜单栏
        self.main_window.menubar.addMenu(self.menu_setting)


    class ConfigurationFilesMenu(object):
        """ 
        二级菜单--配置文件

        提供打开配置文件的操作
        """
        def __init__(self, setting_menu) -> None:
            # 一级菜单SettingMenu对象传入
            self.setting_menu = setting_menu
            # 一级UI对象
            #self.setting_menu.main_window
            # 底层变量
            self.secmenu_setting_files = None # 二级菜单对象
            # 方法绑定
            self.build_menu()

        def build_menu(self) -> None:
            # 创建二级菜单
            self.secmenu_setting_files = QMenu("📖配置文件", self.setting_menu.main_window)
            # 创建三级菜单
            action_json = QAction("📄json", self.setting_menu.main_window)
            action_json.triggered.connect(lambda: self.open_selected_file(WORKING_DIRECTORY_PATH + r'\PlayerConfig.json'))
            action_css = QAction("📄css", self.setting_menu.main_window)
            action_css.triggered.connect(lambda: self.open_selected_file(WORKING_DIRECTORY_PATH + r'\PlayerStyle.css'))
            # 将三级菜单添加到二级菜单
            self.secmenu_setting_files.addAction(action_json)
            self.secmenu_setting_files.addAction(action_css)
            # 将二级菜单添加到一级菜单
            self.setting_menu.menu_setting.addMenu(self.secmenu_setting_files)

        def open_selected_file(self, file_path) -> None:
            """ 菜单项的绑定操作,用于打开选中的文件"""
            try:
                # 使用系统默认程序打开文件
                os.startfile(file_path)
            except FileNotFoundError:
                QMessageBox.critical(self.main_window, 'FileNotFoundError', '文件不存在,请检查文件位置', QMessageBox.Ok)

class IsOverMonitor(object):
    """ 子线程--播放完毕检测 """
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.which_play)  # 绑定方法
        self.timer_interval = 1000  # 定时器间隔，单位是毫秒
        self.timer.start(self.timer_interval)
        
    def is_over(self) -> bool:
        """ 播放完成检测 """
        if self.main_window.player.time > self.main_window.file_total_time:
            print("Next")
            return True
        
    def which_play(self) -> None:
        """ 播放完成后播放方式的选择 """
        if self.is_over():
            time.sleep(2)
            if self.main_window.need_cycle:
                self.main_window.play_song()
            else:
                self.main_window.random_play()
            

class KeyboardListener(object):
    """ 
    子线程 --键盘监听操作与键盘快捷方案
    
    QwQ:当前阶段,键盘快捷方式仅用于主UI界面最小化时,或UI界面不在最顶层时.
    """
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        # pynput.keyboard.Listener可以创建新线程,并持续监听键盘
        self.thread_listen = pynput.keyboard.Listener(on_press=self.concentrate_key_press_programme)
        self.thread_listen.daemon = True # 守护线程
        self.thread_listen.name = 'KeyboardListener'
        self.thread_listen.start()

    def concentrate_key_press_programme(self, key, programme=None) -> [None,str]:
        """ 
        管理快捷方案 
        
        return: 仅在选择的快捷方案存在时返回 str.
        """
        programme_map = {
            "1": self.key_press_p1,
            "2": self.key_press_p2,
            "3": self.key_press_p3,
            "4": self.key_press_p4,
        }
        # programme绑定main_window属性,方便类外操作
        programme = self.main_window.key_press_programme
        # 关闭键盘快捷方式
        if programme is None:
            return None
        # 选择存在的快捷方案
        elif programme in programme_map.keys():
            return programme_map.get(f'{programme}')(key)
        # 不存在的快捷方案
        else:
            return None

    def key_press_p1(self, key) -> None:
        """ 键盘快捷键方案1:主键盘 """
        try:
            # 下一首'right'
            if str(key) == 'Key.right':
                print("'right' has been pressed")
                self.main_window.next_play()
            # 上一首'left'
            elif str(key) == 'Key.left':
                print("'left' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'space'
            elif str(key) == 'Key.space':
                print("'space' has been pressed")
                self.main_window.music_pause()
            # 随机播放'r'
            elif key.char == 'r':
                print("'r' has been pressed")
                self.main_window.random_play()
            # 单曲循环'o'
            elif key.char == 'o':
                print("'o' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            # 防止key没有字符/字符串值导致的报错
            pass

    def key_press_p2(self, key) -> None:
        """ 键盘快捷键方案2:Ctrl+主键盘 """
        try:
            # 下一首'Ctrl+d'
            if key.char == '\x04':
                print("'Ctrl+d' has been pressed")
                self.main_window.next_play()
            # 上一首'Ctrl+a'
            elif key.char == '\x01':
                print("'Ctrl+a' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'Ctrl+s'
            elif key.char == '\x13':
                print("'Ctrl+s' has been pressed")
                self.main_window.music_pause()
            # 随机播放'Ctrl+r'
            elif key.char == '\x12':
                print("'Ctrl+r' has been pressed")
                self.main_window.random_play()
            # 单曲循环'Ctrl+q'
            elif key.char == '\x11':
                print("'Ctrl+q' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            # 防止key没有字符值导致的报错
            pass

    def key_press_p3(self, key) -> None:
        """ 键盘快捷键方案3:数字键盘 """
        try:
            # 下一首'6'
            if str(key) == '<102>':
                print("'6' has been pressed")
                self.main_window.next_play()
            # 上一首'4'
            elif str(key) == '<100>':
                print("'4' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'5'
            elif str(key) == '<101>':
                print("'5' has been pressed")
                self.main_window.music_pause()
            # 随机播放'1'
            elif str(key) == '<97>':
                print("'1' has been pressed")
                self.main_window.random_play()
            # 单曲循环'0'
            elif str(key) == '<96>':
                print("'0' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            # 防止key没有字符值导致的报错
            pass

    def key_press_p4(self, key) -> None:
        """ 键盘快捷键方案4:Ctrl+数字键盘(当前使用的第三方库无法区分主键盘数字键与数字键盘的数字键) """
        try:
            # 下一首'Ctrl+6'
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('6'):
                print("'Ctrl+6' has been pressed")
                self.main_window.next_play()
            # 上一首'Ctrl+4'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('4'):
                print("'Ctrl+4' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'Ctrl+5'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('5'):
                print("'Ctrl+5' has been pressed")
                self.main_window.music_pause()
            # 随机播放'Ctrl+1'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('1'):
                print("'Ctrl+1' has been pressed")
                self.main_window.random_play()
            # 单曲循环'Ctrl+0'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('0'):
                print("'Ctrl+0' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            pass


class DataProtector(object):
    """ 子线程 --数据同步与保存 """
    def __init__(self, main_window) -> None:
        #类对象传入
        self.main_window = main_window

        #线程绑定  daemon=True 设置该线程为守护线程,随主线程结束而退出
        self.thread_data_protector = threading.Thread( target= self.callbackfunc, daemon=True, name='DataProtector')
        self.thread_data_protector.start()
  
    
    def synchronous_data(self) -> None:
        """ 同步数据到 config_js <class 'dict'> """
        try:
            config_js['music_folder_path'] = self.main_window.music_folder_path
            config_js['current_music_number'] = self.main_window.current_music_number
            config_js['file_total_time'] = self.main_window.file_total_time
            config_js['current_position'] = self.main_window.player.time
            config_js['need_cycle'] = self.main_window.need_cycle
            config_js['key_press_programme'] = self.main_window.key_press_programme
            config_js['play_dict'] = self.main_window.play_dict
            config_js['current_music_name'] = os.path.basename(
                self.main_window.play_dict.get(f'{self.main_window.current_music_number}'.replace('*', ''))
            ).replace('.mp3', '')
            
        except AttributeError:
            # 忽略部分属性不存在时带来的报错
            print("AttributeError!")
        except TypeError:
            # 或略配置文件中数据的类型变化,保证在配置文件更改后DataProtector继续运行
            print("TypeError!")
        self.save_data()
    
    def callbackfunc(self) -> None:
        """ 线程绑定操作 """
        while(True):
            self.synchronous_data()
            time.sleep(1)
            
    def save_data(self) -> None:
        """ 保存数据到 PlayerConfig.json """
        try:
            # 打开json文件
            with open(WORKING_DIRECTORY_PATH + r'\PlayerConfig.json', 'w', encoding='utf-8') as config_json:
                # json文件写入 ensure_ascii=False禁用Unicode转义确保写入的文件包含原始的非ASCII字符。
                json.dump(config_js, config_json, ensure_ascii=False, indent=4) 
        except NameError:
            print("NameError!: 请检查json文件的位置.")


def main():
    app = QApplication(sys.argv) # 可操作命令行参数
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
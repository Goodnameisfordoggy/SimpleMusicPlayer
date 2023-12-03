'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2023-11-12 14:48:16
version: 2.0.0
FilePath: \python\py.1求道境\音乐随机播放器\LocalMusicPlayer.py
Description: 
此代码实现的是一个基于Python与本地储存的mp3文件的本地播放器.
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
# 需要cmd安装
import pyglet
import pynput.keyboard
import keyboard
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QPushButton, QLabel, QLineEdit, QTreeWidget, QTreeWidgetItem, 
    QHeaderView, QMessageBox, QMenu, QAction, QDesktopWidget
    )
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QRect, QTimer

# os.path.dirname(os.path.abspath(__file__))获取当前文件所在目录的绝对路径
with open(
    os.path.dirname(os.path.abspath(__file__)) + r'\PlayerConfig.json', 
    'r', encoding='utf-8'
) as configjson:
    jsdate = json.load(configjson)

class ApplicationWindow(QMainWindow):

    def __init__(self, width=1236, height=764) -> None:
        super().__init__()
        # 一级UI设置
        self.setWindowTitle("Music Player")
        self.setWindowIcon(
            QIcon(r"D:\Users\vscode\python\实验与验证2\音乐播放器图标.png")
        )
        #self.setWindowFlag(Qt.WindowStaysOnTopHint, True)# 一级UI界面的层次设置, False置于最底部, True置顶
        self.setFixedSize(width, height)  # 禁止修改窗口大小

        # 重要组件
        #self.button_pause_or_begin = None  # 暂停/开始按钮
        #self.button_cycle = None  # 单曲循环按钮
        #self.current_play_label = None  # 当前播放项展示标签
        #self.menuBar = None  # 菜单栏

        # 方法绑定
        self.build_platform()
        self.center()

        # 底层变量
        self.player = pyglet.media.Player()  # 播放器
        self.music_folder_path = jsdate['music_folder_path'] # 获取音乐文件夹的绝对路径
        self.play_dict = jsdate['play_dict']  # 播放字典
        self.current_music_number = ( # 当前播放的音乐文件序号
            jsdate['current_music_number'] 
            if not isinstance(jsdate['current_music_number'], int) 
            else f'*{jsdate['current_music_number']}*'
        )  
        self.current_position = jsdate['current_position']  # 当前(文件的)播放位置
        self.need_cycle = jsdate['need_cycle']  # 是否循环播放的标志
        self.file_total_time = jsdate['file_total_time']  # 音乐文件总时长
        self.key_press_programme = jsdate['key_press_programme'] # 键盘快捷方案序号

        #绑定线程
        self.is_over_monitor = IsOverMonitor(self)
        self.listener = KeyboardListener(self)
        self.dateprotector = DateProtector(self)

    
    # 更新音乐列表
    def update_song_list(self) -> None:
        # 创建一个空字典
        self.play_dict = {}
        # 导入音乐文件夹
        music_file_path = self.music_folder_path
        # 获取全部mp3文件的路径列表
        mp3_files_list = glob.glob(os.path.join(music_file_path, '*.mp3'))
        # 创建播放字典
        for music_number, music_path in enumerate(mp3_files_list, start=1):
            self.play_dict[f'{music_number}'] = f'{music_path}'

    # 播放音乐
    def play_song(self, music_position=0) -> None:
        # 加载音乐文件
        music_file_path = self.play_dict.get(f'{self.current_music_number}')
        # 根据文件创建music对象
        music = pyglet.media.load(music_file_path)
        # 获取音频文件总时长
        self.file_total_time = int(music.duration)
        # 创建播放器
        self.player = pyglet.media.Player()
        # 将music对象添加到播放器(player)
        self.player.queue(music)
        # 调整播放位置
        self.player.seek(music_position)
        # 开始播放
        self.player.play()

    # 更改当前播放内容(标签绑定操作)
    def change_current_play_label(self) -> None:

        music_file_path = self.play_dict.get(f'{self.current_music_number}')
        music_file_name = os.path.basename(music_file_path)
        self.current_play_label.setText(music_file_name.replace('.mp3', ''))

    # 随机播放(按钮绑定操作)
    def random_play(self) -> None:
        if self.current_music_number is not None:
            self.player.pause()
            self.player.delete()
        if isinstance(self.current_music_number, str):  # 确保解密/确保对象类型为int
            self.current_music_number = int(
                self.current_music_number.replace('*', '')
            )
        self.current_music_number = random.randint(1, len(self.play_dict))
        self.change_current_play_label()
        self.play_song()
        # 按钮文本显示为"暂停"
        self.button_pause_or_begin.setText('暂停')

    # 上一首(按钮绑定操作)
    def previous_play(self) -> None:
        if self.current_music_number is None:
            QMessageBox.critical(self, '错误', '请点击开始播放')
        else:
            self.player.pause()
            self.player.delete()
            if isinstance(self.current_music_number, str):  # 确保解密/确保对象类型为int
                self.current_music_number = int(
                    self.current_music_number.replace('*', '')
                )
            self.current_music_number -= 1
            if self.current_music_number == 0:
                self.current_music_number = len(self.play_dict)
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

    # 下一首(按钮绑定操作)
    def next_play(self) -> None:
        if self.current_music_number is None:
            QMessageBox.critical(self, '错误', '请点击开始播放')
        else:
            self.player.pause()
            self.player.delete()
            if isinstance(self.current_music_number, str):  # 确保解密/确保对象类型为int
                self.current_music_number = int(
                    self.current_music_number.replace('*', '')
                )
            self.current_music_number += 1
            if self.current_music_number > len(self.play_dict):
                self.current_music_number = 1
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

    # 暂停||开始(按钮绑定操作)
    def music_pause(self) -> None:
        # 开始路径1:如果之前无播放内容,则随机播放  QwQ:克服选择困难症
        if self.current_music_number is None:
            self.random_play()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

        # 开始路径2:之前有播放内容被暂停,点击按钮继续播放
        elif isinstance(self.current_music_number, str):  # QwQ:通过类型的转化来区分路径
            self.current_music_number = int(
                self.current_music_number.replace('*', '')
            )
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

    # 单曲循环(按钮绑定操作)
    def single_cycle_play(self) -> None:
        if self.current_music_number is None:
            QMessageBox.critical(self, '错误', '请点击开始播放')
        else:
            # 点击开始循环
            if not self.need_cycle:
                self.need_cycle = True
                # 将文本更改为"cycling",按钮显示为凹陷
                self.button_cycle.setText('cycling')
                self.button_cycle.setStyleSheet("color: rosybrown;")
                                                
            elif self.need_cycle:
                self.need_cycle = False
                # 将文本更改为"单曲循环",按钮显示为凸起
                self.button_cycle.setText('单曲循环')
                self.button_cycle.setStyleSheet("color: black;")
                
    # 确认退出(按钮绑定操作)
    def confirm_to_quit(self) -> None:
        reply = QMessageBox.question(
            self, 
            '温馨提示', '记得给 作者:HDJ 一颗小星星', 
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()  # 使用close方法来关闭窗口

    # UI搭建(使用绝对布局,写死UI界面)
    def build_platform(self) -> None:

        # 创建主体文字标签
        text_label = QLabel('Q*& 私人专属音乐播放工具 Qwq', parent=self)
        text_label.setFont(QFont("楷体", 24))
        text_label.setStyleSheet('color: red; font-weight: bold;')
        text_label.setWordWrap(False)
        text_label.setGeometry(180, 50, 1000, 100)
            

        # F1 创建当前正在播放内容的显示器
        # "正在播放"标签
        self.current_play_text = QLabel(text='正在播放:', parent=self)
        self.current_play_text.setStyleSheet("color: gray;")
        self.current_play_text.setFont(QFont("宋体", 16))
        self.current_play_text.setWordWrap(False) # 禁止自动换行
        self.current_play_text.setGeometry(200, 200, 200, 60)
        # 显示当先正在播放歌曲名称的标签
        self.current_play_label = QLabel(
            text=jsdate['current_music_name'], parent=self
        )
        self.current_play_label.setStyleSheet("color: gray;")
        self.current_play_label.setFont(QFont("楷体", 10))
        self.current_play_label.setWordWrap(True) # 允许自动换行 QwQ:这个很重要
        self.current_play_label.setGeometry(410, 175, 700, 120)
        self.current_play_label.setTextInteractionFlags( # 允许鼠标,键盘与标签文本交互
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard
        )
        # F2
        #上一首按钮
        self.button_previous = QPushButton(text='上一首', parent=self)
        self.button_previous.clicked.connect(self.previous_play)
        self.button_previous.setGeometry(400, 600, 150, 80)
        self.button_previous.setFocusPolicy(Qt.NoFocus) # 阻止按钮获得键盘焦点
        #下一首按钮
        self.button_next = QPushButton(text='下一首', parent=self)
        self.button_next.clicked.connect(self.next_play)
        self.button_next.setGeometry(700, 600, 150, 80)
        self.button_next.setFocusPolicy(Qt.NoFocus) # 阻止按钮获得键盘焦点
        #开始/暂停按钮
        self.button_pause_or_begin = QPushButton(text='开始', parent=self)
        self.button_pause_or_begin.clicked.connect(self.music_pause)
        self.button_pause_or_begin.setGeometry(550, 600, 150, 80)
        self.button_pause_or_begin.setFocusPolicy(Qt.NoFocus) # 阻止按钮获得键盘焦点

        # F3
        # 随机播放按钮
        self.button_shuffle = QPushButton(text='随机播放', parent=self)
        self.button_shuffle.setGeometry(475, 520, 150, 80)
        self.button_shuffle.clicked.connect(self.random_play)
        self.button_shuffle.setFocusPolicy(Qt.NoFocus) # 阻止按钮获得键盘焦点
        # 单曲循环按钮
        self.button_cycle = QPushButton(          
            text=('单曲循环' if jsdate['need_cycle'] is False else 'cycling'), 
            parent=self
        )
        self.button_cycle.clicked.connect(self.single_cycle_play)
        self.button_cycle.setStyleSheet( # 注意setStyleSheet只接受一个字符串
            ("color: black;" if jsdate['need_cycle'] is False 
            else "color: rosybrown;"
            ) 
            #("border: 1px solid black;" if jsdate['need_cycle'] is False else "border: 1px solid rosybrown;")            
        )
        self.button_cycle.setGeometry(625, 520, 150, 80)
        self.button_cycle.setFocusPolicy(Qt.NoFocus) # 阻止按钮获得键盘焦点
 
        # F4
        # 退出按钮
        self.button_quit = QPushButton(text='退出', parent=self)
        self.button_quit.clicked.connect(self.confirm_to_quit)
        self.button_quit.setGeometry(0, 735, 50, 30)
        self.button_quit.setFocusPolicy(Qt.NoFocus) # 阻止按钮获得键盘焦点
        # 提示标签
        self.label_warning = QLabel(
            '请不要点击过快,UI响应需要时间!此工具仅用于学术交流!',
            parent=self
        )
        self.label_warning.setFont(QFont("楷体", 10))
        self.label_warning.setStyleSheet('color: blue;')
        self.label_warning.setWordWrap(False) # 禁止自动换行
        self.label_warning.setGeometry(250, 680, 800, 100)

        # 菜单设置
        # 菜单栏
        self.menuBar = self.menuBar()  # 创建菜单栏对象
        self.menuBar.setFixedHeight(40)

        #一级菜单创建操作

        menu_chang_folder_path = ChangeFolderMenu(self)

        menu_search_for_target_song = SearchUI(self)
        
        menu_change_key_press_programme = ChangeKeyPressProgramme(self)

    # 主UI界面窗口位置居中
    def center(self) -> None:
        frame_geometry = self.frameGeometry()
        desktop_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(desktop_center)
        self.move(frame_geometry.topLeft())

# 菜单--更改文件夹操作
class ChangeFolderMenu(object):


    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window
        # 方法绑定
        self.build_menu()
        # 底层变量
        self.menu_change_folder_path = None  # 一级菜单对象

    def build_menu(self) -> None:
        # 一级菜单
        self.menu_change_folder_path = QMenu('更改文件夹', self.main_window)

        # 二级菜单
        self_path = QMenu('自定义歌单', self.main_window)
        singer_path = QMenu('按歌手分类', self.main_window)

        # 三级下拉菜单(项) 
        self_path_action_1 = QAction(
            jsdate['music_folders_path']['folder1']['name'], 
            self.main_window)
        self_path_action_1.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder1']['path']))
        self_path_action_2 = QAction(
            jsdate['music_folders_path']['folder2']['name'], 
            self.main_window)
        self_path_action_2.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder2']['path']))


        singer_path_action_1 = QAction(
            jsdate['music_folders_path']['folder3']['name'], 
            self.main_window)
        singer_path_action_1.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder3']['path']))
        singer_path_action_2 = QAction(
            jsdate['music_folders_path']['folder4']['name'], 
            self.main_window)
        singer_path_action_2.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder4']['path']))
        singer_path_action_3 = QAction(
            jsdate['music_folders_path']['folder5']['name'], 
            self.main_window)
        singer_path_action_3.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder5']['path']))
        singer_path_action_4 = QAction(
            jsdate['music_folders_path']['folder6']['name'], 
            self.main_window)
        singer_path_action_4.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder6']['path']))
        singer_path_action_5 = QAction(
            jsdate['music_folders_path']['folder7']['name'], 
            self.main_window)
        singer_path_action_5.triggered.connect(
            lambda: self.change_music_path(
                jsdate['music_folders_path']['folder7']['path']))
        
        # 向二级菜单添加三级菜单(action)
        self_path.addAction(self_path_action_1)
        self_path.addAction(self_path_action_2)
        singer_path.addAction(singer_path_action_1)
        singer_path.addAction(singer_path_action_2)
        singer_path.addAction(singer_path_action_3)
        singer_path.addAction(singer_path_action_4)
        singer_path.addAction(singer_path_action_5)
        # 向一级菜单添加二级菜单
        self.menu_change_folder_path.addMenu(self_path)
        self.menu_change_folder_path.addMenu(singer_path)
        # 向菜单栏添加一级菜单
        self.main_window.menuBar.addMenu(self.menu_change_folder_path)
    # 更改文件夹(菜单项绑定操作)
    def change_music_path(self, path) -> None:
        self.main_window.music_folder_path = path
        self.main_window.update_song_list()

# 歌曲搜索界面
class SearchUI(QDialog):

    def __init__(self, main_window, width=1250, height=950) -> None:
        super().__init__()
        #一级UI对象传入
        self.main_window = main_window

        # 设置二级UI
        self.setWindowTitle("歌曲查询中...")
        self.setFixedSize(width, height)  # 禁止修改窗口大小

        # 方法绑定
        self.build_search_platform()
        self.build_menu()
        self.center()
        
        # 重要组件
        #self.menu_search_for_target_song = None # 一级菜单对象
        #self.song_name_qlineEdit = None  # 输入歌曲查找信息的单行文本输入框
        #self.input_song_name = None # 输入框的内容
        #self.treeview_search_result = None  # 展示搜索结果的树型图

        # 底层变量
        self.onclick_song_number = None  # 鼠标选中的序号


    # 创建菜单
    def build_menu(self) -> None:
        # 一级菜单
        self.menu_search_for_target_song = QMenu('查询界面', self.main_window)

        # 二级菜单
        entry_action = QAction('打开查询界面', self.main_window)
        entry_action.triggered.connect(lambda: self.exec_rewrite())

        # 向一级菜单添加二级菜单(action)
        self.menu_search_for_target_song.addAction(entry_action)

        # 向菜单栏添加一级菜单
        self.main_window.menuBar.addMenu(self.menu_search_for_target_song)

    def exec_rewrite(self):
        self.label_current_folder.setText(
            os.path.basename(jsdate['music_folder_path'])
        )
        self.show()
        self.main_window.showMinimized()
        
    # 二级UI窗口居中
    def center(self) -> None:
        frame_geometry = self.frameGeometry()
        desktop_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(desktop_center)
        self.move(frame_geometry.topLeft())

    # 搜索(二级UI按钮绑定操作)
    def searching(self, input_song_name) -> None:  
        input_song_name = self.song_name_qlineEdit.text()
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
                        os.path.basename(
                            self.main_window.play_dict[key]
                        ).replace(".mp3", '').split("--")[0],
                        f'{singer_name}'
                    )                                                     
            if num <= 0:
                QMessageBox.warning(
                    self, 
                    '搜素结束', '很抱歉,没有找到歌曲', 
                    QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok
                )
        else:
            QMessageBox.critical(
                self, 
                'ERROR', '您未输入需查询的歌曲, 请输入后搜索!', 
                QMessageBox.Retry | QMessageBox.Abort, QMessageBox.Retry
            )
    
    # (添加项目)树形图方法
    def add_tree_item(self, text1, text2, text3) -> None:
        item = QTreeWidgetItem(self.treeview_search_result)
        item.setText(0, text1)
        item.setText(1, text2)
        item.setText(2, text3)

    # 鼠标单击点击(二级UI树型视图绑定操作)
    def onclick(self, item, column) -> None: 
        # 获取树型视图被点击行中第一列的信息(获取歌曲序号)
        self.onclick_song_number = int(item.text(0))
            
        if self.onclick_song_number is not None:
            self.main_window.current_music_number = self.onclick_song_number
        else:
            QMessageBox.critical(
                self, 
                'ERROR', '请点击歌曲进行选定!', 
                QMessageBox.Retry | QMessageBox.Abort, QMessageBox.Retry
            )

    # 播放(二级UI按钮绑定操作)
    def search_ui_play(self) -> None:
        if self.onclick_song_number is None or isinstance(
            self.main_window.current_music_number, str
        ):
            QMessageBox.warning(
                self, 
                'Warning', '您未选定歌曲', 
                QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok
            )
        else:
            if self.main_window.current_music_number is not None:
                self.main_window.player.pause()
                self.main_window.player.delete()
            self.main_window.change_current_play_label()
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
        # 主体标签设置
        main_label = QLabel(text='@ 歌曲查找界面 #', parent=self)
        main_label.setFont(QFont("楷体", 20))
        main_label.setStyleSheet('color: red; font-weight: bold;')
        main_label.setGeometry(400, 0, 1000, 100)
    
        # F1
        label_folder_attention = QLabel(text='当前文件夹(库名):', parent=self)
        label_folder_attention.setFont(QFont("楷体", 10))
        label_folder_attention.setStyleSheet('color: gray; font-weight: bold;')
        label_folder_attention.setGeometry(150, 100, 250, 60)

        self.label_current_folder = QLabel(
            text=os.path.basename(jsdate['music_folder_path']), parent=self
        )
        self.label_current_folder.setWordWrap(True)
        self.label_current_folder.setFont(QFont("宋体", 14))
        self.label_current_folder.setStyleSheet('color: gray; font-weight: bold;')
        self.label_current_folder.setGeometry(400, 100, 600, 60)

        label_input_reminder = QLabel(text='请输入歌曲/歌手名称:', parent=self)
        label_input_reminder.setFont(QFont("宋体", 12))
        label_input_reminder.setStyleSheet('color: black; font-weight: bold;')
        label_input_reminder.setGeometry(100, 160, 350, 60)

        # 输入框
        self.song_name_qlineEdit = QLineEdit(parent=self)
        self.song_name_qlineEdit.setPlaceholderText('输入信息,点击搜素') 
        self.song_name_qlineEdit.setGeometry(450, 160, 450, 60) 

        # "搜索"按钮
        button_searching = QPushButton(text='搜索', parent=self)
        button_searching.setFont(QFont('宋体', 20))
        button_searching.setStyleSheet("color: purple;")
        button_searching.setGeometry(900, 160, 100, 60)
        button_searching.clicked.connect(
            lambda: self.searching(self.song_name_qlineEdit.text())
        )
        # F2 (树形图)
        self.treeview_search_result = QTreeWidget(self)    
        self.treeview_search_result.setGeometry(100, 250, 1000, 300)
        # 树型视图表头文本设置
        self.treeview_search_result.setHeaderLabels(["序号", "歌曲名称", "歌手"])
        # 禁止拖拽表头
        self.treeview_search_result.header().setSectionsMovable(False)
        # 禁止拉伸表头
        self.treeview_search_result.header().setSectionResizeMode(0, QHeaderView.Fixed)
        self.treeview_search_result.header().setSectionResizeMode(1, QHeaderView.Fixed)
        self.treeview_search_result.header().setSectionResizeMode(2, QHeaderView.Fixed)
        # 设置列宽
        self.treeview_search_result.setColumnWidth(0, 120)
        self.treeview_search_result.setColumnWidth(1, 600)
        self.treeview_search_result.setColumnWidth(2, 340)

        # 鼠标单击(点击操作绑定)
        self.treeview_search_result.itemClicked.connect(self.onclick)


        # "播放"按钮
        button_play = QPushButton(text='播放', parent=self)
        button_play.setFont(QFont('宋体', 20))
        button_play.setStyleSheet("color: purple;")
        button_play.setGeometry(570, 550, 100, 60)
        button_play.clicked.connect(self.search_ui_play)        

        # F3
        label_use_attention = QLabel(
            text='注意事项:'
            '\n1.该功能仅限于在所添加的文件夹中搜索歌曲(序号按文件夹内顺序),而非爬虫!'
            '\n2.该搜索功能仅进行宽泛搜索,罗列,并不能精确导向.'
            '\n3.使用步骤: 输入搜索内容,点击所搜按钮,在所罗列的内容中用\n'
            '鼠标左键单击选定需要播放的歌曲,点击播放按钮即可.'
            '\n4.点击播放后,该搜索界面会自动关闭,如有二次需求请重新进入.'
            '\n5.并不是所有的音乐文件名都符合规范,为了好的体验请保持文件名格式为:'
            '\n歌曲名(歌曲信息)--歌手1&歌手2...(歌手信息).mp3',
            parent=self
        )
        label_use_attention.setFont(QFont("楷体", 8))
        label_use_attention.setStyleSheet('color: blue; font-weight: bold;')
        label_use_attention.setAlignment(Qt.AlignLeft)
        label_use_attention.setGeometry(110, 650, 1200, 300)

    # 二级UI窗口关闭方法重写
    def closeEvent(self, event) -> None:
        print("closeEvent")
        # 将一级UI界面还原到上一次最小化前的位置
        self.main_window.showNormal()
        # 调用父类的 closeEvent 方法，确保原有的行为能够正常执行
        super().closeEvent(event)


class ChangeKeyPressProgramme(object):

    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window

        self.menu_change_key_press_programme = None
        # 方法绑定
        self.build_menu()

    def build_menu(self) -> None:
        #一级菜单
        self.menu_change_key_press_programme = QMenu('快捷方式', self.main_window)

        # 二级菜单
        default_action_1 = QAction('关闭快捷方式', self.main_window)
        default_action_1.triggered.connect(
            lambda: setattr(self.main_window, 'key_press_programme', None))
        default_action_2 = QAction('主键盘+方向键', self.main_window)
        default_action_2.triggered.connect(
            lambda: setattr(self.main_window, 'key_press_programme', '1'))
        default_action_3 = QAction('Ctrl+主键盘', self.main_window)
        default_action_3.triggered.connect(
            lambda: setattr(self.main_window, 'key_press_programme', '2'))
        default_action_4 = QAction('数字键盘', self.main_window)
        default_action_4.triggered.connect(
            lambda: setattr(self.main_window, 'key_press_programme', '3'))
        default_action_5 = QAction('Ctrl+数字键盘', self.main_window)
        default_action_5.triggered.connect(
            lambda: setattr(self.main_window, 'key_press_programme', '4'))
        
        # 向一级菜单添加二级菜单(action)
        self.menu_change_key_press_programme.addAction(default_action_1)
        self.menu_change_key_press_programme.addAction(default_action_2)
        self.menu_change_key_press_programme.addAction(default_action_3)
        self.menu_change_key_press_programme.addAction(default_action_4)
        self.menu_change_key_press_programme.addAction(default_action_5)

        #向菜单栏添加一级菜单
        self.main_window.menuBar.addMenu(self.menu_change_key_press_programme)

        #绑定操作(可以被setattr()替换)
    #def change_key_press_programme(self, programme_number):
        #self.main_window.key_press_programme = programme_number


# 子线程 --播放完毕检测
class IsOverMonitor(object):
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.is_over)  # 定时器触发时更新 UI
        self.timer_interval = 1000  # 定时器间隔，单位是毫秒
        self.timer.start(self.timer_interval)
        
    # 播放完成检测
    def is_over(self) -> None:
        if self.main_window.player.time > self.main_window.file_total_time:
            print("Next")
            time.sleep(2)
            if self.main_window.need_cycle:
                self.main_window.play_song()
            else:
                self.main_window.random_play()
            


# 子线程 --键盘监听操作与键盘快捷方案
class KeyboardListener(object):

    def __init__(self, main_window) -> None:
        self.main_window = main_window
        # pynput.keyboard.Listener可以创建新线程,并持续监听键盘
        self.thread_listen = pynput.keyboard.Listener(
            on_press=self.change_key_press_programme
        )
        self.thread_listen.daemon = True # 守护线程
        self.thread_listen.name = 'KeyboardListener'
        self.thread_listen.start()

    # QwQ:当前阶段,键盘快捷方式仅用于主UI界面最小化时,或UI界面不在最顶层时.
    def change_key_press_programme(self, key, programme=None):
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

    # 键盘快捷键方案1:主键盘
    def key_press_p1(self, key) -> None:
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

    # 键盘快捷键方案2:Ctrl+主键盘
    def key_press_p2(self, key) -> None:
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

    # 键盘快捷键方案3:数字键盘
    def key_press_p3(self, key) -> None:
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

    # 键盘快捷键方案4:Ctrl+数字键盘(当前使用的第三方库无法区分主键盘与数字键盘的数字键)
    def key_press_p4(self, key) -> None:
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


# 子线程 --数据同步与保存
class DateProtector(object):

    def __init__(self, main_window) -> None:
        #类对象传入
        self.main_window = main_window

        #线程绑定  
        self.thread_date_protector = threading.Thread( # daemon=True 设置该线程为守护线程,随主线程结束而退出
            target= self.callbackfunc, daemon=True, name='DateProtector'
        )
        self.thread_date_protector.start()
  
    
    #同步数据到 jsdate <class 'dict'>
    def synchronous_data(self) -> None:
        try:
            # jsdate[''] = 
            jsdate['music_folder_path'] = self.main_window.music_folder_path
            jsdate['current_music_number'] = self.main_window.current_music_number
            jsdate['file_total_time'] = self.main_window.file_total_time
            jsdate['current_position'] = self.main_window.player.time
            jsdate['need_cycle'] = self.main_window.need_cycle
            jsdate['key_press_programme'] = self.main_window.key_press_programme
            jsdate['play_dict'] = self.main_window.play_dict
            jsdate['current_music_name'] = os.path.basename(
                self.main_window.play_dict.get(
                    f'{self.main_window.current_music_number}'.replace('*', '')
                )
            ).replace('.mp3', '')
        except AttributeError:
            # 忽略部分属性不存在时带来的报错
            pass
        except TypeError:
            # 保证在配置文件更改后程序继续运行
            print("TypeError!")
        self.save_date()
    
    def callbackfunc(self) -> None:
        while(True):
            self.synchronous_data()
            time.sleep(1)
    #保存数据到 PlayerConfig.json
    def save_date(self) -> None:
        try:
            # 打开json文件
            with open(
                os.path.dirname(os.path.abspath(__file__)) + r'\PlayerConfig.json', 
                'w', encoding='utf-8'
            ) as configjson:
                # json文件写入 ensure_ascii=False禁用Unicode转义确保写入的文件包含原始的非ASCII字符。
                json.dump(jsdate, configjson, ensure_ascii=False, indent=4) 
        except NameError:
            print("NameError!: __file__ 不存在,请检查json文件的位置.")


if __name__ == '__main__':
    app = QApplication(sys.argv) # 可操作命令行参数
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())
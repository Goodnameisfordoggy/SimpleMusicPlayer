'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-03-14 23:25:30
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\ApplicationWindow.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) ${2024} by ${HDJ}, All Rights Reserved. 
'''
import glob
import os
import random
import pyglet
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Simple_Qt import Label, PushButton, PackingModificationMethod
from SearchUI import SearchUI
from IsOverMonitor import IsOverMonitor
from KeyboardListener import KeyboardListener
from DataProtector import DataProtector
from SettingUI import SettingUI
from DataProtector import config_js, style_js, style_css


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
        self.setWindowIcon(QIcon(config_js['ApplicationWindowIcon']))
        PackingModificationMethod.set_background_image(
            self, config_js['ApplicationWindowBackGround'])
        PackingModificationMethod.set_desktop_center(self)
        # 一级UI界面的层次设置, False置于最底部, True置顶
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        # self.setWindowFlag(Qt.FramelessWindowHint) # 移除程序窗框饰条

        # 方法绑定
        self.build_platform()

        # 底层变量
        self.player = pyglet.media.Player()  # 播放器
        self.music_folder_path = config_js['music_folder_path']  # 获取音乐文件夹的绝对路径
        self.play_dict = config_js['play_dict']  # 播放字典
        self.current_music_number = (  # 当前播放的音乐文件序号
            config_js['current_music_number']
            if not isinstance(config_js['current_music_number'], int)
            else f'*{config_js['current_music_number']}*'
        )
        self.current_position = config_js['current_position']  # 当前(文件的)播放位置
        self.need_cycle = config_js['need_cycle']  # 是否循环播放的标志
        self.file_total_time = config_js['file_total_time']  # 音乐文件总时长
        self.key_press_programme = config_js['key_press_programme']  # 键盘快捷方案序号

        # 绑定线程
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
            # 记录播放歌曲所属的歌单
            config_js['foregoing_songlist'] = os.path.dirname(
                self.play_dict.get(f'{self.current_music_number}'.replace('*', '')))

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
        if not self.current_music_number:
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
        if not self.current_music_number:
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
        if not self.current_music_number:
            self.random_play()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.setText('暂停')

        # 开始路径2:之前有播放内容被暂停,点击按钮继续播放
        elif isinstance(self.current_music_number, str):  # QwQ:通过类型的转化来区分路径
            #对比暂停前的歌单与当前歌单是否一致，来决定是否初始化播放序号与位置
            if config_js['foregoing_songlist'] != config_js['music_folder_path']:
                # 此路径下,切换歌单后继续播放,则从歌单的第一首的0秒开始播放
                self.current_music_number = 1
                self.current_position = 0.0
                self.play_song(self.current_position)
            else:
                # 未切换歌单, 从上次位置继续播放
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
        if not self.current_music_number:
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
        self.label_MainWindow_main_text = Label.create(
            parent=self, text='Q*& 私人专属音乐播放工具 Qwq',
            Alignment=Qt.AlignHCenter | Qt.AlignBottom,
            Geometry=(18, 30, 1200, 100),
            ObjectName=style_js["label_MainWindow_main_text"],
            StyleSheet=style_css
        )

        # F1 创建当前正在播放内容的显示器
        # "正在播放"标签
        self.label_current_play_text = Label.create(
            parent=self, text='正在\n播放',
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter,
            Geometry=(270, 290, 100, 100),
            ObjectName=style_js["label_current_play_text"],
            StyleSheet=style_css
        )

        # 显示当先正在播放歌曲名称的标签
        self.label_current_play_content = Label.create(
            parent=self, text=config_js['current_music_name'],
            WordWrap=True,  # 允许自动换行 QwQ:这个很重要
            Alignment=Qt.AlignVCenter | Qt.AlignLeft,
            TextInteractionFlags=Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard,  # 允许鼠标,键盘与标签文本交互
            Geometry=(410, 265, 650, 150),
            ObjectName=style_js["label_current_play_content"],
            StyleSheet=style_css
        )

        # 上一首按钮
        self.button_previous = PushButton.create(
            parent=self, text='上一首',
            clicked_callback=self.previous_play,
            Geometry=(400, 600, 150, 80),
            ObjectName=style_js["button_previous"],
            StyleSheet=style_css
        )

        # 下一首按钮
        self.button_next = PushButton.create(
            parent=self, text='下一首',
            clicked_callback=self.next_play,
            Geometry=(700, 600, 150, 80),
            ObjectName=style_js["button_next"],
            StyleSheet=style_css
        )

        # 开始/暂停按钮
        self.button_pause_or_begin = PushButton.create(
            self, text='开始',
            clicked_callback=self.music_pause,
            Geometry=(550, 600, 150, 80),
            ObjectName=style_js["button_pause_or_begin"],
            StyleSheet=style_css
        )

        # F3
        # 随机播放按钮
        self.button_shuffle_play = PushButton.create(
            parent=self, text='随机播放',
            clicked_callback=self.random_play,
            Geometry=(475, 520, 150, 80),
            ObjectName=style_js["button_shuffle_play"],
            StyleSheet=style_css
        )

        # 单曲循环按钮
        self.button_single_loop = PushButton.create(
            parent=self, text=(
                '单曲循环' if config_js['need_cycle'] is False else 'cycling'),
            clicked_callback=self.single_cycle_play,
            Geometry=(625, 520, 150, 80),
            ObjectName=style_js["button_single_loop"],
            StyleSheet=style_css
        )

        # F4
        # 退出按钮
        self.button_quit = PushButton.create(
            parent=self, text='退出',
            clicked_callback=self.confirm_to_quit,
            Geometry=(0, 735, 50, 30),
            ObjectName=style_js["button_quit"],
            StyleSheet=style_css
        )

        # 警告标签
        self.label_warning_text = Label.create(
            parent=self, text='请不要点击过快,UI响应需要时间!此工具仅用于学术交流!',
            Alignment=Qt.AlignCenter,
            Geometry=(250, 680, 800, 100),
            ObjectName=style_js["label_warning_text"],
            StyleSheet=style_css
        )

        # 菜单设置
        # 菜单栏
        self.menubar = self.menuBar()  # 创建菜单栏对象
        self.menubar.setFixedHeight(40)
        self.menubar.setObjectName('menubar--1')
        self.menubar.setStyleSheet(style_css)

        # 一级菜单创建操作
        menu_setting = SettingUI(app=self)

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

    def closeEvent(self, event) -> None:
        """ 一级UI窗口关闭事件 """
        # 调用父类的 closeEvent 方法，确保原有的行为能够正常执行
        super().closeEvent(event)
        QApplication.closeAllWindows()

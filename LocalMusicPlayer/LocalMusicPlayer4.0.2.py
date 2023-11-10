'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2023-11-10 12:30:28
version: 4.0.2
FilePath: \python\py.1求道境\音乐随机播放器\LocalMusicPlayer.py
Description: 
此代码实现的是一个基于Python与本地储存的mp3文件的本地播放器.
在323行下可以添加或更改自己的音乐文件夹路径(仅需配置一次,可更改).
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
import tkinter
import tkinter.messagebox
from tkinter import ttk
import glob
import os
import random
import re
import threading
import json
# 需要cmd安装
import pyglet
import pynput.keyboard
import keyboard


# os.path.dirname(os.path.abspath(__file__))获取当前文件所在目录的绝对路径
with open(
    os.path.dirname(os.path.abspath(__file__)) + r'\PlayerConfig.json', 'r', encoding='utf-8'
) as configjson:
    jsdate = json.load(configjson)

class App(object):

    def __init__(self, width=309, height=191):
        # 主UI设置
        self.ui_width = width
        self.ui_height = height
        self.ui_title = '音乐播放器'
        # 创建一个名称为self._ui_titled的窗口
        self.ui_root = tkinter.Tk(className=self.ui_title)
        # 一级UI界面的层次设置, False置于最底部, True置顶
        self.ui_root.attributes('-topmost', False)
        self.button_pause_or_begin = tkinter.Button()  # 暂停/开始按钮
        #self.button_cycle = tkinter.Button()  # 单曲循环按钮
        self.current_play_label = tkinter.Label()  # 当前播放项展示标签
        self.menu = tkinter.Menu()  # 菜单栏
        self.build_platform()
        self.ui_root.resizable(False, False)  # 禁止修改窗口大小
        self.center()
        # 底层变量
        self.player = pyglet.media.Player()  # 播放器
        self.play_dict = jsdate['play_dict']  # 播放字典
        self.current_music_number = (
            jsdate['current_music_number'] 
            if type(jsdate['current_music_number'])!=int 
            else '*{}*'.format(jsdate['current_music_number'])
        )  # 当前播放的音乐文件序号
        self.current_position = jsdate['current_position']  # 当前(文件的)播放位置
        self.need_cycle = jsdate['need_cycle']  # 是否循环播放的标志
        self.file_total_time = jsdate['file_total_time']  # 音乐文件总时长
        self.key_press_programme = jsdate['key_press_programme'] # 键盘快捷方案序号
        #绑定线程
        self.is_over_monitor = IsOverMonitor(self)
        self.listener = KeyboardListener(self)
        self.dateprotector = DateProtector(self)

        # 获取音乐文件夹的绝对路径
        self.music_folder_path = jsdate['music_folder_path']
    # 更新音乐列表
    def update_song_list(self):
        # 创建一个空字典
        self.play_dict = {}
        # 导入音乐文件夹
        music_file_path = self.music_folder_path
        # 获取全部mp3文件的路径列表
        mp3_files_list = glob.glob(os.path.join(music_file_path, '*.mp3'))
        # 创建播放字典
        for music_number, music_path in enumerate(mp3_files_list, start=1):
            self.play_dict[f'{music_number}'] = f'{music_path}'
            # self.random_play()  # 程序打开,自动随机播放(已禁用)

    # 播放音乐
    def play_song(self, music_position=0):
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
    def change_current_play_label(self):

        music_file_path = self.play_dict.get(f'{self.current_music_number}')
        music_file_name = os.path.basename(music_file_path)
        self.current_play_label.config(text=music_file_name.replace('.mp3', ''))

    # 随机播放(按钮绑定操作)
    def random_play(self):
        if self.current_music_number is not None:
            self.player.pause()
            self.player.delete()
        if type(self.current_music_number) == str:  # 确保解密/确保对象类型为int
            self.current_music_number = int(self.current_music_number.replace('*', ''))
        self.current_music_number = random.randint(1, len(self.play_dict))
        self.change_current_play_label()
        self.play_song()
        # 按钮文本显示为"暂停"
        self.button_pause_or_begin.config(text='暂停')

    # 上一首(按钮绑定操作)
    def previous_play(self):
        if self.current_music_number is None:
            tkinter.messagebox.showerror(title='错误', message='请点击开始播放')
        else:
            self.player.pause()
            self.player.delete()
            if type(self.current_music_number) == str:  # 确保解密/确保对象类型为int
                self.current_music_number = int(
                    self.current_music_number.replace('*', ''))
            self.current_music_number -= 1
            if self.current_music_number == 0:
                self.current_music_number = len(self.play_dict)
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.config(text='暂停')

    # 下一首(按钮绑定操作)
    def next_play(self):
        if self.current_music_number is None:
            tkinter.messagebox.showerror(title='错误', message='请点击开始播放')
        else:
            self.player.pause()
            self.player.delete()
            if type(self.current_music_number) == str:  # 确保解密/确保对象类型为int
                self.current_music_number = int(self.current_music_number.replace('*', ''))
            self.current_music_number += 1
            if self.current_music_number > len(self.play_dict):
                self.current_music_number = 1
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.config(text='暂停')

    # 暂停||开始(按钮绑定操作)
    def music_pause(self):
        # 开始路径1:如果之前无播放内容,则随机播放  QwQ:克服选择困难症
        if self.current_music_number is None:
            self.random_play()
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.config(text='暂停')

        # 开始路径2:之前有播放内容被暂停,点击按钮继续播放
        elif type(self.current_music_number) == str:  # QwQ:通过类型的转化来区分路径
            self.current_music_number = int(self.current_music_number.replace('*', ''))
            self.play_song(self.current_position)
            self.current_position = 0.0
            # 按钮文本显示为"暂停"
            self.button_pause_or_begin.config(text='暂停')

        # 当前有文件正在播放,点击按钮暂停
        else:
            self.current_position = self.player.time
            self.player.pause()
            # QwQ将当前播放序号在转类型的时候稍微加密
            self.current_music_number = f'*{self.current_music_number}*'
            # 按钮文本显示为"开始"
            self.button_pause_or_begin.config(text='开始')

    # 单曲循环(按钮绑定操作)
    def single_cycle_play(self):
        if self.current_music_number is None:
            tkinter.messagebox.showerror(title='错误', message='请点击开始播放')
        else:
            # 点击开始循环
            if not self.need_cycle:
                self.need_cycle = True
                # 将文本更改为"cycling",按钮显示为凹陷
                self.button_cycle.config(text='cycling', fg='rosybrown', relief=tkinter.SUNKEN)
            elif self.need_cycle:
                self.need_cycle = False
                # 将文本更改为"单曲循环",按钮显示为凸起
                self.button_cycle.config(text='单曲循环', fg='black', relief=tkinter.RAISED)

    # 确认退出(按钮绑定操作)
    def confirm_to_quit(self):
        if tkinter.messagebox.askokcancel('温馨提示', '记得给 作者:HDJ 一颗小星星'):
            self.ui_root.quit()

    # UI搭建
    def build_platform(self):
        # 创建主体文字标签
        text_label = tkinter.Label(
            self.ui_root, text='Q*& 私人专属音乐播放工具 Qwq', font=("楷体", 16), fg='red')
        text_label.pack(expand=True)

        # 控件设置
        # 框架
        frame0 = tkinter.Frame(self.ui_root)
        frame0.pack()
        frame1 = tkinter.Frame(self.ui_root)
        frame1.pack()
        frame2 = tkinter.Frame(self.ui_root)
        frame2.pack()
        frame3 = tkinter.Frame(self.ui_root)
        frame3.pack()

        # f0 创建当前正在播放内容的显示器
        current_play_text = tkinter.Label(frame0, text='正在播放', 
                                          wraplength=30, font=("宋体", 10), fg='gray')
        current_play_text.pack(expand=True, side='left')
        self.current_play_label = tkinter.Label(frame0, text=jsdate['current_music_name'], 
                                                wraplength=270, font=("楷体", 10), fg='gray')
        self.current_play_label.pack(expand=True, side='right', )

        # f1
        button_previous = tkinter.Button(frame1, text='上一首', command=self.previous_play)
        button_previous.pack(side='left')
        button_next = tkinter.Button(frame1, text='下一首', command=self.next_play)
        button_next.pack(side='right')
        self.button_pause_or_begin = tkinter.Button(frame1, text='开始', command=self.music_pause)
        self.button_pause_or_begin.pack(side='top')
        # f2
        button_shuffle = tkinter.Button(frame2, text='随机播放', command=self.random_play)
        button_shuffle.pack(side='left')
        self.button_cycle = tkinter.Button(
            frame2, 
            text=('单曲循环' if jsdate['need_cycle'] is False else 'cycling'), 
            relief=(tkinter.RAISED if jsdate['need_cycle'] is False else tkinter.SUNKEN),
            fg=('black' if jsdate['need_cycle'] is False else 'rosybrown'),
            command=self.single_cycle_play
        )
        self.button_cycle.pack(side='right')
        
        # f3
        button_quit = tkinter.Button(frame3, text='退出', command=self.confirm_to_quit)
        button_quit.pack()
        label_explain = tkinter.Label(
            frame3, 
            text='请不要点击过快,UI响应需要时间!\n此工具仅用于学术交流!', 
            font=("楷体", 10), fg='blue'
        )
        label_explain.pack()

        # 菜单设置
        # 菜单栏
        self.menu = tkinter.Menu(self.ui_root)  # 创建菜单栏对象
        self.ui_root.config(menu=self.menu)  # 将菜单栏对象添加到UI界面中

        #菜单创建操作

        # 一级菜单(更改文件夹) QwQ:将一级菜单(更改文件夹)作为对象(包含菜单的创建操作)
        # 将App类对象传递给ChangeFolderMenu的构造函数来创建ChangeFolderMenu类对象
        menu_chang_folder = ChangeFolderMenu(self)

        # 一级菜单(查找歌曲) QwQ:将一级菜单(查找歌曲)所绑定的二级UI作为对象(不包含二级菜单的创建操作)
        menu_search_for_target_song = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='查找歌曲', menu=menu_search_for_target_song)
        # 打开二级UI(歌曲查询界面)
        def open_search_ui():
            self.ui_root.iconify()  # 将一级UI最小化到任务栏
            # 将App类对象传递给SearchUI的构造函数来创建SearchUI类对象
            self.search_ui = SearchUI(self)
        # 歌曲查询界面的菜单入口
        menu_search_for_target_song.add_command(label='打开查询界面', command=open_search_ui)
        
        #一级菜单(更改键盘快捷方式)
        menu_change_key_press_programme = ChangeKeyPressProgramme(self)

    # 主UI界面窗口位置居中
    def center(self):
        ws = self.ui_root.winfo_screenwidth()
        hs = self.ui_root.winfo_screenheight()
        x = int((ws / 2) - (self.ui_width / 2))
        y = int((hs / 2) - (self.ui_height / 2))
        self.ui_root.geometry(
            '{}x{}+{}+{}'.format(self.ui_width, self.ui_height, x, y))


# 菜单--更改文件夹操作
class ChangeFolderMenu(object):


    def __init__(self, app):
        self.app = app
        self.menu_change_folder_path = tkinter.Menu()  # 一级菜单对象
        self.build_menu()

    def build_menu(self):
        # 一级菜单(更改文件夹)
        # QwQ: 语法格式:Menu()中菜单参数为上一级菜单 #tearoff=0禁用了撕开菜单的功能
        self.menu_change_folder_path = tkinter.Menu(self.app.menu, tearoff=0)
        # QwQ: 语法格式:上一级菜单.add_cascade(, 下一级菜单)
        self.app.menu.add_cascade(label='更改文件夹', menu=self.menu_change_folder_path)

        # 二级菜单
        self_path = tkinter.Menu(self.menu_change_folder_path, tearoff=0)
        self.menu_change_folder_path.add_cascade(label='自定义歌单', menu=self_path)
        singer_path = tkinter.Menu(self.menu_change_folder_path, tearoff=0)
        self.menu_change_folder_path.add_cascade(label='按歌手分类', menu=singer_path)

        # 三级下拉菜单(项) #在r后""中直接添加路径即可(以下为配置实例) QwQ: label为菜单项文本,语法格式:上一级菜单.add_command(这一级菜单的属性)
        self_path.add_command(label=jsdate['music_folders_path']['folder1']['name'],
                              command=lambda: self.change_music_path(jsdate['music_folders_path']['folder1']['path']))
        self_path.add_command(label=jsdate['music_folders_path']['folder2']['name'],
                              command=lambda: self.change_music_path(jsdate['music_folders_path']['folder2']['path']))
        singer_path.add_command(label=jsdate['music_folders_path']['folder3']['name'],
                                command=lambda: self.change_music_path(jsdate['music_folders_path']['folder3']['path']))
        singer_path.add_command(label=jsdate['music_folders_path']['folder4']['name'],
                                command=lambda: self.change_music_path(jsdate['music_folders_path']['folder4']['path']))
        singer_path.add_command(label=jsdate['music_folders_path']['folder5']['name'],
                                command=lambda: self.change_music_path(jsdate['music_folders_path']['folder5']['path']))
        singer_path.add_command(label=jsdate['music_folders_path']['folder6']['name'],
                                command=lambda: self.change_music_path(jsdate['music_folders_path']['folder6']['path']))
        singer_path.add_command(label=jsdate['music_folders_path']['folder7']['name'],
                                command=lambda: self.change_music_path(jsdate['music_folders_path']['folder7']['path']))

    
    # 更改文件夹(菜单项绑定操作)
    def change_music_path(self, path):
        self.app.music_folder_path = path
        self.app.update_song_list()


# 歌曲搜索界面
class SearchUI(object):

    def __init__(self, app, width=650, height=450):
        # 设置二级UI窗口基础数值
        self.app = app
        self.search_ui_width, self.search_ui_height = width, height
        self.search_ui_root = tkinter.Toplevel(self.app.ui_root, width=width, height=height)
        self.search_ui_root.title("歌曲查询中...")
        self.song_name = tkinter.StringVar()  # 获取输入框文本的对象
        self.treeview_search_result = ttk.Treeview()  # 展示搜索结果的树型图
        self.search_ui_root.resizable(False, False)  # 禁止修改窗口大小
        self.build_search_platform()
        self.center()
        # 底层变量
        self.onclick_song_number = None  # 鼠标选中的序号

    # 二级UI窗口居中
    def center(self):
        ws = self.search_ui_root.winfo_screenwidth()
        hs = self.search_ui_root.winfo_screenheight()
        x = int((ws / 2) - (self.search_ui_width / 2))
        y = int((hs / 2) - (self.search_ui_height / 2))
        self.search_ui_root.geometry('{}x{}+{}+{}'.format(self.search_ui_width, self.search_ui_height, x, y))

    # 搜索(二级UI按钮绑定操作)
    def searching(self, song_name):  # QwQ: 此处song_name接收的参数的类型将是StringVar(tkinter模块中自带的数据类型)
        if len(song_name.get()) > 0:  # 需要使用get()方法获取StringVar中的String(字符串)数据
            self.treeview_search_result.delete(*self.treeview_search_result.get_children())  # 清除图表所有行内容
            num = 0
            for key, value in self.app.play_dict.items():  # 在循环中处理键和值,items()方法将返回 包含字典中的键值对的 可迭代对象
                if song_name.get() in os.path.basename(value):  # 判断用户输入内容与文件名是否有重叠
                    num += 1
                    # 用正则表达式来提取歌手的名字
                    singer_name = "暂无"
                    pattern = r"--(.+?)\.mp3"
                    result = re.search(pattern, os.path.basename(value))
                    if result:
                        singer_name = result.group().replace("--", '').replace(".mp3", '')
                    # 将搜索内容显示到图表中
                    # i = 0 #i表示图表的第几行,注意:第0行不是表头,而是表头下的第一行  # i若启用则为倒序展示搜索结果
                    self.treeview_search_result.insert(
                        '', 'end',  # QwQ: end表示每次添加到末尾,在此可视为正序展示搜索结果
                        values=(
                            key,
                            # 保留"--"前面的歌曲名
                            os.path.basename(self.app.play_dict[key]).replace(".mp3", '').split("--")[0],
                            singer_name))
                    # i += 1
            if num <= 0:
                tkinter.messagebox.showwarning(title='搜素结束', message='很抱歉,没有找到歌曲')
        else:
            tkinter.messagebox.showerror(title='错误', message='您未输入需查询的歌曲, 请输入后搜索!')

    # 鼠标单击点击(二级UI树型视图绑定操作)
    def onclick(self, event):  # QwQ:根据错误类型,此处必须有一个参数,否则点击时报错,尚不清楚原因
        # treeview中的左键单击
        for item in self.treeview_search_result.selection():
            # 获取树型视图被点击行的全部信息
            item_text = self.treeview_search_result.item(item, "values")
            # 获取树型视图被点击行中第一列的信息(获取歌曲序号)
            self.onclick_song_number = int(item_text[0])
            if self.onclick_song_number is not None:
                self.app.current_music_number = self.onclick_song_number
            else:
                tkinter.messagebox.showerror(title='错误', message='请点击歌曲进行选定')

    # 播放(二级UI按钮绑定操作)
    def search_ui_play(self):
        if self.onclick_song_number is None or type(self.app.current_music_number) == str:
            tkinter.messagebox.showwarning(title='warning', message='您未选定歌曲')
        else:
            if self.app.current_music_number is not None:
                self.app.player.pause()
                self.app.player.delete()
            self.app.change_current_play_label()
            self.app.play_song()
            # 按钮文本显示为"暂停"
            self.app.button_pause_or_begin.config(text='暂停')
            # 摧毁二级UI释放资源
            self.search_ui_root.destroy()
            # 将一级UI界面还原到上一次最小化前的位置
            self.app.ui_root.deiconify()
            # 将鼠标获取到的序号清除
            self.onclick_song_number = None

    def build_search_platform(self):
        # 主体标签设置
        main_label = tkinter.Label(self.search_ui_root, text='@ 歌曲查找界面 #', font=("楷体", 16), fg='red')
        main_label.pack()

        # 框架
        second_frame1 = tkinter.Frame(self.search_ui_root)
        second_frame1.pack()
        second_frame2 = tkinter.Frame(self.search_ui_root)
        second_frame2.pack()
        second_frame3 = tkinter.Frame(self.search_ui_root)
        second_frame3.pack()

        # second_f1
        label_folder_attention = tkinter.Label(second_frame1, text='当前文件夹(名):', font=("楷体", 10), fg='black')
        label_folder_attention.grid(row=0, column=0)
        label_current_folder = tkinter.Label(second_frame1, text=os.path.basename(self.app.music_folder_path),
                                             font=("宋体", 14), fg='gray', anchor='w')
        label_current_folder.grid(row=0, column=1)
        label_input_reminder = tkinter.Label(second_frame1, text='请输入歌曲/歌手名称:', font=("宋体", 12), fg='black')
        label_input_reminder.grid(row=1, column=0)  # QwQ: 用grid来使控件在同一行
        label_blank_left = tkinter.Label(second_frame1, text=' ')
        label_blank_left.grid(row=1, column=1)
        entry = tkinter.Entry(second_frame1, textvariable=self.song_name, highlightcolor='Fuchsia',
                              highlightthickness=1,
                              width=40)  # QwQ: highlightcolor--输入框被点击时边框的颜色, highlightthickness--输入框边框的宽度
        entry.grid(row=1, column=2)
        label_blank_right = tkinter.Label(second_frame1, text=' ')
        label_blank_right.grid(row=1, column=3)
        button_searching = tkinter.Button(second_frame1, text='搜索', command=lambda: self.searching(self.song_name))
        button_searching.grid(row=1, column=4)

        # second_f2
        # 树型视图表头设置 QwQ: #加一个整数表示索引,从左到右索引从1开始
        columns = ("#1序号", "#2歌曲名称", "#3歌手")
        self.treeview_search_result = ttk.Treeview(second_frame2, height=5, show="headings", columns=columns)
        # QwQ: show="headings" 指定了树状视图只显示表头，而不显示默认的第一列。
        # 树型视图表头文本设置
        self.treeview_search_result.heading("#1序号", text='序号')
        self.treeview_search_result.heading("#2歌曲名称", text='歌曲名称')
        self.treeview_search_result.heading("#3歌手", text='歌手')
        # 树型视图列设置
        self.treeview_search_result.column("#1序号", width=40, anchor='center')
        self.treeview_search_result.column("#2歌曲名称", width=400, anchor='center')
        self.treeview_search_result.column("#3歌手", width=200, anchor='center')
        self.treeview_search_result.pack()
        # 鼠标单击(点击操作绑定)
        self.treeview_search_result.bind('<ButtonRelease-1>', self.onclick)
        # 播放按钮
        button_play = tkinter.Button(second_frame2, text='播放', font=('宋体', 20), fg='purple', width=3,
                                     height=1, padx=20, pady=1, command=self.search_ui_play)
        button_play.pack()

        # second_f3
        label_use_attention = tkinter.Label(
            second_frame3,
            text='注意事项:'
            '\n1.该功能仅限于在所添加的文件夹中搜索歌曲(序号按文件夹内顺序),而非爬虫!'
            '\n2.该搜索功能仅进行宽泛搜索,罗列,并不能精确导向.'
            '\n3.使用步骤: 输入搜索内容,点击所搜按钮,在所罗列的内容中用\n'
            '鼠标左键单击选定需要播放的歌曲,点击播放按钮即可.'
            '\n4.点击播放后,该搜索界面会自动关闭,如有二次需求请重新进入.'
            '\n5.并不是所有的音乐文件名都符合规范,为了好的体验请保持文件名格式为:'
            '\n歌曲名(歌曲信息)--歌手1&歌手2...(歌手信息).mp3',
            font=("楷体", 12), fg='blue', anchor='w'
        )
        label_use_attention.pack()

        # 二级UI窗口关闭协议
        def search_ui_root_protocol():
            # 摧毁二级UI释放资源
            self.search_ui_root.destroy()
            # 将一级UI界面还原到上一次最小化前的位置
            self.app.ui_root.deiconify()
        self.search_ui_root.protocol("WM_DELETE_WINDOW", search_ui_root_protocol)  # 窗口关闭事件的操作绑定


# 菜单--更改键盘快捷方案
class ChangeKeyPressProgramme(object):

    def __init__(self, app) -> None:
        self.app = app
        self.menu_change_key_press_programme = tkinter.Menu()
        self.build_menu()

    def build_menu(self) -> None:
        #一级菜单
        self.menu_change_key_press_programme = tkinter.Menu(self.app.menu, tearoff=0)
        self.app.menu.add_cascade(label='快捷方式', menu=self.menu_change_key_press_programme)

        # 二级菜单
        self.menu_change_key_press_programme.add_command(label='关闭快捷方式', 
                                                         command=lambda: setattr(self.app, 'key_press_programme', None))
        self.menu_change_key_press_programme.add_command(label='主键盘+方向键', 
                                                         command=lambda: setattr(self.app, 'key_press_programme', '1'))
        self.menu_change_key_press_programme.add_command(label='Ctrl+主键盘', 
                                                         command=lambda: setattr(self.app, 'key_press_programme', '2'))
        self.menu_change_key_press_programme.add_command(label='数字键盘', 
                                                         command=lambda: setattr(self.app, 'key_press_programme', '3'))
        self.menu_change_key_press_programme.add_command(label='Ctrl+数字键盘', 
                                                         command=lambda: setattr(self.app, 'key_press_programme', '4'))
 
        #绑定操作(可以被setattr()替换)
    #def change_key_press_programme(self, programme_number):
        #self.app.key_press_programme = programme_number


# 子线程 1 --播放完毕检测
class IsOverMonitor(object):
    def __init__(self, app) -> None:
        self.app = app
        self.thread_monitor = threading.Thread(target=self.is_over, daemon=True, name='IsOverMonitor')
        self.thread_monitor.start()

    # 播放完成检测
    def is_over(self) -> None:
        if self.app.player.time > self.app.file_total_time:
            print("Next")
            time.sleep(2)
            if self.app.need_cycle:
                self.app.play_song()
            else:
                self.app.random_play()
        # 按照一定时间间隔递归
        self.app.ui_root.after(3000, self.is_over)


# 子线程 2 --键盘监听操作与键盘快捷方案
class KeyboardListener(object):

    def __init__(self, app) -> None:
        self.app = app
        # pynput.keyboard.Listener可以创建新线程,并持续监听键盘
        self.thread_listen = pynput.keyboard.Listener(on_press=self.change_key_press_programme)
        self.thread_listen.daemon = True # 守护线程
        self.thread_listen.start()

    # QwQ:当前阶段,键盘快捷方式仅用于主UI界面最小化时,或UI界面不在最顶层时.
    def change_key_press_programme(self, key, programme=None):
        programme_map = {
            "1": self.key_press_p1,
            "2": self.key_press_p2,
            "3": self.key_press_p3,
            "4": self.key_press_p4,
        }
        # programme绑定App属性,方便类外操作
        programme = self.app.key_press_programme
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
                self.app.next_play()
            # 上一首'left'
            elif str(key) == 'Key.left':
                print("'left' has been pressed")
                self.app.previous_play()
            # 暂停/开始'space'
            elif str(key) == 'Key.space':
                print("'space' has been pressed")
                self.app.music_pause()
            # 随机播放'r'
            elif key.char == 'r':
                print("'r' has been pressed")
                self.app.random_play()
            # 单曲循环'o'
            elif key.char == 'o':
                print("'o' has been pressed")
                self.app.single_cycle_play()
        except AttributeError:
            # 防止key没有字符/字符串值导致的报错
            pass

    # 键盘快捷键方案2:Ctrl+主键盘
    def key_press_p2(self, key) -> None:
        try:
            # 下一首'Ctrl+d'
            if key.char == '\x04':
                print("'Ctrl+d' has been pressed")
                self.app.next_play()
            # 上一首'Ctrl+a'
            elif key.char == '\x01':
                print("'Ctrl+a' has been pressed")
                self.app.previous_play()
            # 暂停/开始'Ctrl+s'
            elif key.char == '\x13':
                print("'Ctrl+s' has been pressed")
                self.app.music_pause()
            # 随机播放'Ctrl+r'
            elif key.char == '\x12':
                print("'Ctrl+r' has been pressed")
                self.app.random_play()
            # 单曲循环'Ctrl+q'
            elif key.char == '\x11':
                print("'Ctrl+q' has been pressed")
                self.app.single_cycle_play()
        except AttributeError:
            # 防止key没有字符值导致的报错
            pass

    # 键盘快捷键方案3:数字键盘
    def key_press_p3(self, key) -> None:
        try:
            # 下一首'6'
            if str(key) == '<102>':
                print("'6' has been pressed")
                self.app.next_play()
            # 上一首'4'
            elif str(key) == '<100>':
                print("'4' has been pressed")
                self.app.previous_play()
            # 暂停/开始'5'
            elif str(key) == '<101>':
                print("'5' has been pressed")
                self.app.music_pause()
            # 随机播放'1'
            elif str(key) == '<97>':
                print("'1' has been pressed")
                self.app.random_play()
            # 单曲循环'0'
            elif str(key) == '<96>':
                print("'0' has been pressed")
                self.app.single_cycle_play()
        except AttributeError:
            # 防止key没有字符值导致的报错
            pass

    # 键盘快捷键方案4:Ctrl+数字键盘(当前使用的第三方库无法区分主键盘与数字键盘的数字键)
    def key_press_p4(self, key) -> None:
        try:
            # 下一首'Ctrl+6'
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('6'):
                print("'Ctrl+6' has been pressed")
                self.app.next_play()
            # 上一首'Ctrl+4'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('4'):
                print("'Ctrl+4' has been pressed")
                self.app.previous_play()
            # 暂停/开始'Ctrl+5'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('5'):
                print("'Ctrl+5' has been pressed")
                self.app.music_pause()
            # 随机播放'Ctrl+1'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('1'):
                print("'Ctrl+1' has been pressed")
                self.app.random_play()
            # 单曲循环'Ctrl+0'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('0'):
                print("'Ctrl+0' has been pressed")
                self.app.single_cycle_play()
        except AttributeError:
            pass


# 子线程 3 --数据同步与保存
class DateProtector(object):

    def __init__(self, app) -> None:
        #类对象传入
        self.app = app

        #线程绑定  daemon=True 设置该线程为保护线程,随主线程结束而退出
        self.thread_date_protector = threading.Thread(target= self.callbackfunc, daemon=True, name='DateProtector')
        self.thread_date_protector.start()
  
    
    #同步数据到 jsdate <class 'dict'>
    def synchronous_data(self):
        try:
            # jsdate[''] = 
            jsdate['music_folder_path'] = self.app.music_folder_path
            jsdate['current_music_number'] = self.app.current_music_number
            jsdate['file_total_time'] = self.app.file_total_time
            jsdate['current_position'] = self.app.player.time
            jsdate['need_cycle'] = self.app.need_cycle
            jsdate['key_press_programme'] = self.app.key_press_programme
            jsdate['play_dict'] = self.app.play_dict
            jsdate['current_music_name'] = os.path.basename(
                self.app.play_dict.get(f'{self.app.current_music_number}'.replace('*', ''))).replace('.mp3', '')
        except AttributeError:
            #忽略部分属性不存在时带来的报错
            pass
        except TypeError:
            print("TypeError!")
        self.save_date()
    
    def callbackfunc(self):
        while(True):
            self.synchronous_data()
            time.sleep(1)
    #保存数据到 PlayerConfig.json
    def save_date(self):
        try:
            # 打开json文件
            with open(os.path.dirname(os.path.abspath(__file__)) + r'\PlayerConfig.json', 'w', encoding='utf-8') as configjson:
                # json文件写入 ensure_ascii=False禁用Unicode转义确保写入的文件包含原始的非ASCII字符。
                json.dump(jsdate, configjson, ensure_ascii=False, indent=4) 
        except NameError:
            print("NameError!: __file__ 不存在,请检查json文件的位置.")


def main():
    app = App()
    app.ui_root.mainloop()


# 查看播放列表
# def get_dict():
    # app = App()
    # app.update_song_list()
    # print(app.play_dict)


if __name__ == '__main__':
    main()
    # get_dict()

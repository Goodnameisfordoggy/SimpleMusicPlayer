"""
Maker: HDJ
Start at: 2023/7/9
Last modified date: 2023/7/10
version: 3.0
使用须知:
此代码实现的是一个基于Python与本地储存的mp3文件的本地播放器.
在47行下可添加开始时的默认文件夹(非必须,若不设置请在菜单"更改文件夹"进行选定后点击播放),
在330行下可以添加或更改自己的音乐文件夹路径(使用前必填).
其余参数可根据注释,慎重更改.
"""
import time
import tkinter
import tkinter.messagebox
from tkinter import ttk
import glob
import os
import random
import pyglet
import re


class App(object):

    def __init__(self, width=309, height=191):
        self._ui_width = width
        self._ui_height = height
        self._ui_title = '音乐播放器'
        self._ui_root = tkinter.Tk(className=self._ui_title)#创建一个名称为self._ui_titled的窗口
        self._ui_root.attributes('-topmost', False)#一级UI界面的层次设置, False置于最底部, True置顶
        self._second_ui_root = None#二级UI对象
        self._button_pause_or_begin = tkinter.Button() #暂停/开始按钮
        self._button_cycle = tkinter.Button()#单曲循环按钮
        self._current_play_label = tkinter.Label()#当前播放项展示标签
        self._song_name = tkinter.StringVar()#获取输入框文本的对象
        self._treeview_search_result = ttk.Treeview()#展示搜索结果的树型图
        self._player = pyglet.media.Player()#播放器
        self._play_dict = {}#播放字典
        self._current_music_number = None#当前播放的音乐文件序号
        self.onclick_song_number = None#鼠标选中的序号
        self._current_position = None#当前(文件的)播放位置
        self._need_cycle = False#是否循环播放的标志
        self._file_total_time = 0#音乐文件总时长
        self.build_platform()
        self.center()
        self.num = 0
        #此处修改默认的音乐文件夹的绝对路径
        self.music_folder_path = "C:\\Users\\HDJ\\Music\\歌曲\\♥️"

    @property
    def root(self):
        return self._ui_root

    @property
    def play_dict(self):
        return self._play_dict

    def set_play_dict(self, key, value):
        self._play_dict[key] = value

    @property
    def current_music_number(self):
        return self._current_music_number

    @current_music_number.setter
    def current_music_number(self, number):
        self._current_music_number = number

    #更新音乐列表
    def update_song_list(self):
        # 创建一个空字典
        self._play_dict = {}
        # 导入音乐文件夹
        music_file_path = self.music_folder_path
        # 获取全部mp3文件的路径列表
        mp3_files_list = glob.glob(os.path.join(music_file_path, '*.mp3'))
        # 创建播放字典
        for music_number, music_path in enumerate(mp3_files_list, start=1):
            self._play_dict[f'{music_number}'] = f'{music_path}'
            #self.random_play()  # 程序打开,自动随机播放

    # 播放音乐
    def play_song(self, music_position=0):
        # 加载音乐文件
        music_file_path = self._play_dict.get(f'{self._current_music_number}')
        # 根据文件创建music对象
        music = pyglet.media.load(music_file_path)
        # 获取音频文件总时长
        self._file_total_time = int(music.duration)
        # 创建播放器
        self._player = pyglet.media.Player()
        # 将music对象添加到播放器(player)
        self._player.queue(music)
        # 调整播放位置
        self._player.seek(music_position)
        # 开始播放
        self._player.play()

    #播放完成检测
    def is_over(self):
        print(self._player.time)
        print(self._file_total_time)
        self.num += 1
        print(f"递归次数:{self.num}")
        if self._player.time > self._file_total_time:
            print("Next")
            time.sleep(2)
            if self._need_cycle:
                self.play_song()
            else:
                self.random_play()
        self._ui_root.after(3000, self.is_over)

    # 更改当前播放内容(标签绑定操作)
    def change_current_play_label(self):

        music_file_path = self._play_dict.get(f'{self._current_music_number}')
        music_file_name = os.path.basename(music_file_path)
        self._current_play_label.config(text=music_file_name.replace('.mp3', ''))

    # 随机播放(按钮绑定操作)
    def random_play(self):
        if self._current_music_number is not None:
            self._player.pause()
            self._player.delete()
        if type(self._current_music_number) == str:#确保解密/确保对象类型为int
            self._current_music_number = int(self._current_music_number.replace('*', ''))
        self._current_music_number = random.randint(1, len(self._play_dict))
        self.change_current_play_label()
        self.play_song()
        # 按钮文本显示为"暂停"
        self._button_pause_or_begin.config(text='暂停')

    # 上一首(按钮绑定操作)
    def previous_play(self):
        if self._current_music_number is None:
            tkinter.messagebox.showerror(title='错误', message='请点击开始播放')
        else:
            self._player.pause()
            self._player.delete()
            if type(self._current_music_number) == str:  # 确保解密/确保对象类型为int
                self._current_music_number = int(self._current_music_number.replace('*', ''))
            self._current_music_number -= 1
            if self._current_music_number == 0:
                self._current_music_number = len(self._play_dict)
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self._button_pause_or_begin.config(text='暂停')

    # 下一首(按钮绑定操作)
    def next_play(self):
        if self._current_music_number is None:
            tkinter.messagebox.showerror(title='错误', message='请点击开始播放')
        else:
            self._player.pause()
            self._player.delete()
            if type(self._current_music_number) == str:  # 确保解密/确保对象类型为int
                self._current_music_number = int(self._current_music_number.replace('*', ''))
            self._current_music_number += 1
            if self._current_music_number > len(self._play_dict):
                self._current_music_number = 1
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self._button_pause_or_begin.config(text='暂停')

    # 暂停||开始(按钮绑定操作)
    def music_pause(self):
        # 开始路径1:如果之前无播放内容,则随机播放  QwQ:克服选择困难症
        if self._current_music_number is None:
            self.random_play()
            #按钮文本显示为"暂停"
            self._button_pause_or_begin.config(text='暂停')

        # 开始路径2:之前有播放内容被暂停,点击按钮继续播放
        elif type(self._current_music_number) == str:# QwQ:通过类型的转化来区分路径
            self._current_music_number = int(self._current_music_number.replace('*', ''))
            self.play_song(self._current_position)
            self._current_position = None
            # 按钮文本显示为"暂停"
            self._button_pause_or_begin.config(text='暂停')

        # 当前有文件正在播放,点击按钮暂停
        else:
            self._current_position = self._player.time
            self._player.pause()
            self._current_music_number = f'*{self._current_music_number}*'# QwQ将当前播放序号在转类型的时候稍微加密
            # 按钮文本显示为"开始"
            self._button_pause_or_begin.config(text='开始')

    #单曲循环(按钮绑定操作)
    def single_cycle_play(self):
        if self._current_music_number is None:
            tkinter.messagebox.showerror(title='错误', message='请点击开始播放')
        else:
            # 点击开始循环
            if not self._need_cycle:
                self._need_cycle = True
                # 将文本更改为"cycling",按钮显示为凹陷
                self._button_cycle.config(text='cycling', fg='rosybrown', relief=tkinter.SUNKEN)
            elif self._need_cycle:
                self._need_cycle = False
                # 将文本更改为"单曲循环",按钮显示为凸起
                self._button_cycle.config(text='单曲循环', fg='black', relief=tkinter.RAISED)

    # 确认退出(按钮绑定操作)
    def confirm_to_quit(self):
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
            self._ui_root.quit()

    # 更改文件夹(菜单项绑定操作)
    def change_music_path(self, path):
        self.music_folder_path = path
        self.update_song_list()

    # 搜索(二级UI按钮绑定操作)
    def searching(self, song_name): #QwQ: 此处song_name接收的参数的类型将是StringVar(tkinter模块中自带的数据类型)
        if len(song_name.get()) > 0:    # 需要使用get()方法获取StringVar中的String(字符串)数据
            self._treeview_search_result.delete(*self._treeview_search_result.get_children())#清除图表所有行内容
            num = 0
            for key, value in self._play_dict.items():#在循环中处理键和值,items()方法将返回 包含字典中的键值对的 可迭代对象
                if song_name.get() in os.path.basename(value):#判断用户输入内容与文件名是否有重叠
                    num += 1
                    # 用正则表达式来提取歌手的名字
                    singer_name = "暂无"
                    pattern = r"--(.+?)\.mp3"
                    result = re.search(pattern, os.path.basename(value))
                    if result:
                        singer_name = result.group().replace("--", '').replace(".mp3", '')
                    # 将搜索内容显示到图表中
                    #i = 0 #i表示图表的第几行,注意:第0行不是表头,而是表头下的第一行  # i若启用则为倒序展示搜索结果
                    self._treeview_search_result.insert(
                        '', 'end',# QwQ: end表示每次添加到末尾,在此可视为正序展示搜索结果
                        values=(key,
                                os.path.basename(self._play_dict[key]).replace(".mp3", '').split("--")[0],#保留"--"前面的歌曲名
                                singer_name))
                    #i += 1
            if num <= 0:
                tkinter.messagebox.showwarning(title='搜素结束', message='很抱歉,没有找到歌曲')
        else:
            tkinter.messagebox.showerror(title='错误', message='您未输入需查询的歌曲, 请输入后搜索!')

    # 鼠标单击点击(二级UI树型视图绑定操作)
    def onclick(self, event): #QwQ:根据错误类型,此处必须有一个参数,否则点击时报错,尚不清楚原因
        # treeview中的左键单击
        for item in self._treeview_search_result.selection():
            # 获取树型视图被点击行的全部信息
            item_text = self._treeview_search_result.item(item, "values")
            # 获取树型视图被点击行中第一列的信息(获取歌曲序号)
            self.onclick_song_number = int(item_text[0])
            if self.onclick_song_number is not None:
                self._current_music_number = self.onclick_song_number
            else:
                tkinter.messagebox.showerror(title='错误', message='请点击歌曲进行选定')

    # 播放(二级UI按钮绑定操作)
    def second_ui_play(self):
        if self.onclick_song_number is None or type(self._current_music_number) == str:
            tkinter.messagebox.showwarning(title='warning', message='您未选定歌曲')
        else:
            if self._current_music_number is not None:
                self._player.pause()
                self._player.delete()
            self.change_current_play_label()
            self.play_song()
            # 按钮文本显示为"暂停"
            self._button_pause_or_begin.config(text='暂停')
            # 摧毁二级UI释放资源
            self._second_ui_root.destroy()
            # 将一级UI界面还原到上一次最小化前的位置
            self._ui_root.deiconify()
            # 将鼠标获取到的序号清除
            self.onclick_song_number = None

    # UI搭建
    def build_platform(self):
        # 创建主体文字标签
        text_label = tkinter.Label(self._ui_root, text='Q*& 私人专属音乐播放工具 Qwq', font=("楷体", 16), fg='red')
        text_label.pack(expand=True)

        # 控件设置
        # 框架
        frame0 = tkinter.Frame(self._ui_root)
        frame0.pack()
        frame1 = tkinter.Frame(self._ui_root)
        frame1.pack()
        frame2 = tkinter.Frame(self._ui_root)
        frame2.pack()
        frame3 = tkinter.Frame(self._ui_root)
        frame3.pack()

        # f0 创建当前正在播放内容的显示器
        current_play_text = tkinter.Label(frame0, text='正在播放', wraplength=30, font=("宋体", 10), fg='gray')
        current_play_text.pack(expand=True, side='left')
        self._current_play_label = tkinter.Label(frame0, text='请点击开始播放', wraplength=270, font=("楷体", 10), fg='gray')
        self._current_play_label.pack(expand=True, side='right', )

        # f1
        button_previous = tkinter.Button(frame1, text='上一首', command=self.previous_play)
        button_previous.pack(side='left')
        button_next = tkinter.Button(frame1, text='下一首', command=self.next_play)
        button_next.pack(side='right')
        self._button_pause_or_begin = tkinter.Button(frame1, text='开始', command=self.music_pause)
        self._button_pause_or_begin.pack(side='top')
        # f2
        button_shuffle = tkinter.Button(frame2, text='随机播放', command=self.random_play)
        button_shuffle.pack(side='left')
        self._button_cycle = tkinter.Button(frame2, text='单曲循环', command=self.single_cycle_play)
        self._button_cycle.pack(side='right')

        # f3
        button_quit = tkinter.Button(frame3, text='退出', command=self.confirm_to_quit)
        button_quit.pack()
        label_explain = tkinter.Label(frame3, text='请不要点击过快,UI响应需要时间!\n此工具仅用于学术交流!', font=("楷体", 10), fg='blue')
        label_explain.pack()

        # 菜单设置
        # 菜单栏
        menu = tkinter.Menu(self._ui_root)#创建菜单栏对象
        self._ui_root.config(menu=menu)#将菜单栏对象添加到UI界面中
        # 一级菜单(更改文件夹)
        menu_change_music_path = tkinter.Menu(menu, tearoff=0)# QwQ: 语法格式:Menu()中菜单参数为上一级菜单
        menu.add_cascade(label='更改文件夹', menu=menu_change_music_path)# QwQ: 语法格式:上一级菜单.add_cascade(, 下一级菜单)
        # 二级菜单
        self_path = tkinter.Menu(menu_change_music_path, tearoff=0)#tearoff=0禁用了撕开菜单的功能
        menu_change_music_path.add_cascade(label='自定义歌单', menu=self_path)
        singer_path = tkinter.Menu(menu_change_music_path, tearoff=0)
        menu_change_music_path.add_cascade(label='按歌手分类', menu=singer_path)
        # 三级下拉菜单(项)  QwQ: 语法格式:上一级菜单.add_command(这一级菜单的属性)
        self_path.add_command(label='♥️',
                              command=lambda: self.change_music_path("C:\\Users\\霍东君\\Music\\歌曲\\♥️"))
        self_path.add_command(label='总库',
                              command=lambda: self.change_music_path("C:\\Users\\霍东君\\Music\\歌曲\\总库"))
        singer_path.add_command(label='薛之谦',
                                command=lambda: self.change_music_path("C:\\Users\\霍东君\\Music\\歌曲\\歌手\\薛之谦"))
        singer_path.add_command(label='周杰伦',
                                command=lambda: self.change_music_path("C:\\Users\\霍东君\\Music\\歌曲\\歌手\\周杰伦"))
        singer_path.add_command(label='林俊杰',
                                command=lambda: self.change_music_path("C:\\Users\\霍东君\\Music\\歌曲\\歌手\\林俊杰"))
        singer_path.add_command(label='Taylor Swift',
                                command=lambda: self.change_music_path("C:\\Users\\霍东君\\Music\\歌曲\\歌手\\Taylor Swift"))

        # 一级菜单(查找歌曲)
        menu_search_for_target_song = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label='查找歌曲', menu=menu_search_for_target_song)

        # 创建二级UI(歌曲查询界面)
        def open_search_ui():
            # 将一级UI最小化到任务栏
            self._ui_root.iconify()
            # 设置二级UI窗口基础数值
            width, height = 650, 450
            self._second_ui_root = tkinter.Toplevel(self._ui_root, width=width, height=height)
            self._second_ui_root.title("歌曲查询中...")
            # 禁止修改窗口大小
            self._second_ui_root.resizable(False, False)
            # 窗口居中
            ws = self._second_ui_root.winfo_screenwidth()
            hs = self._second_ui_root.winfo_screenheight()
            x = int((ws/2) - (width/2))
            y = int((hs/2) - (height/2))
            self._second_ui_root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

            # 二级UI窗口关闭协议
            def second_ui_root_protocol():
                # 摧毁二级UI释放资源
                self._second_ui_root.destroy()
                # 将一级UI界面还原到上一次最小化前的位置
                self._ui_root.deiconify()

            self._second_ui_root.protocol("WM_DELETE_WINDOW", second_ui_root_protocol)#窗口关闭事件的操作绑定
            # 主体标签设置
            main_label = tkinter.Label(self._second_ui_root, text='@ 歌曲查找界面 #', font=("楷体", 16), fg='red')
            main_label.pack()

            # 框架
            second_frame1 = tkinter.Frame(self._second_ui_root)
            second_frame1.pack()
            second_frame2 = tkinter.Frame(self._second_ui_root)
            second_frame2.pack()
            second_frame3 = tkinter.Frame(self._second_ui_root)
            second_frame3.pack()

            # second_f1
            label_folder_attention = tkinter.Label(second_frame1, text='当前文件夹(名):', font=("楷体", 10), fg='black')
            label_folder_attention.grid(row=0, column=0)
            label_current_folder = tkinter.Label(second_frame1, text=os.path.basename(self.music_folder_path),
                                                 font=("宋体", 14), fg='gray', anchor='w')
            label_current_folder.grid(row=0, column=1)
            label_input_reminder = tkinter.Label(second_frame1, text='请输入歌曲/歌手名称:', font=("宋体", 12), fg='black')
            label_input_reminder.grid(row=1, column=0)#QwQ: 用grid来使控件在同一行
            label_blank_left = tkinter.Label(second_frame1, text=' ')
            label_blank_left.grid(row=1, column=1)
            entry = tkinter.Entry(second_frame1, textvariable=self._song_name, highlightcolor='Fuchsia',
                                  highlightthickness=1, width=40) #QwQ: highlightcolor--输入框被点击时边框的颜色, highlightthickness--输入框边框的宽度
            entry.grid(row=1, column=2)
            label_blank_right = tkinter.Label(second_frame1, text=' ')
            label_blank_right.grid(row=1, column=3)
            button_searching = tkinter.Button(second_frame1, text='搜索', command=lambda: self.searching(self._song_name))
            button_searching.grid(row=1, column=4)

            # second_f2
            columns = ("#1序号", "#2歌曲名称", "#3歌手") #树型视图表头设置 QwQ: #加一个整数表示索引,从左到右索引从1开始
            self._treeview_search_result = ttk.Treeview(second_frame2, height=5, show="headings", columns=columns)
            #QwQ: show="headings" 指定了树状视图只显示表头，而不显示默认的第一列。
            # 树型视图表头文本设置
            self._treeview_search_result.heading("#1序号", text='序号')
            self._treeview_search_result.heading("#2歌曲名称", text='歌曲名称')
            self._treeview_search_result.heading("#3歌手", text='歌手')
            # 树型视图列设置
            self._treeview_search_result.column("#1序号", width=40, anchor='center')
            self._treeview_search_result.column("#2歌曲名称", width=400, anchor='center')
            self._treeview_search_result.column("#3歌手", width=200, anchor='center')
            self._treeview_search_result.pack()
            # 鼠标单击(点击操作绑定)
            self._treeview_search_result.bind('<ButtonRelease-1>', self.onclick)

            button_play = tkinter.Button(second_frame2, text='播放', font=('宋体', 20), fg='purple', width=3, height=1,
                                         padx=20, pady=1, command=self.second_ui_play)
            button_play.pack()

            # second_f3
            label_use_attention = tkinter.Label(second_frame3,
                                                text='注意事项:'
                                                     '\n1.该功能仅限于在所添加的文件夹中搜索歌曲(序号按文件夹内顺序),而非爬虫!'
                                                     '\n2.该搜索功能仅进行宽泛搜索,罗列,并不能精确导向.'
                                                     '\n3.使用步骤: 输入搜索内容,点击所搜按钮,在所罗列的内容中用\n'
                                                     '鼠标左键单击选定需要播放的歌曲,点击播放按钮即可.'
                                                     '\n4.点击播放后,该搜索界面会自动关闭,如有二次需求请重新进入.'
                                                     '\n5.并不是所有的音乐文件名都符合规范,为了好的体验请保持文件名格式为:'
                                                     '\n歌曲名(歌曲信息)--歌手1&歌手2...(歌手信息).mp3',
                                                font=("楷体", 12), fg='blue', anchor='w')
            label_use_attention.pack()
        # 歌曲查询界面的菜单入口
        menu_search_for_target_song.add_command(label='打开查询界面', command=open_search_ui)

    # 主UI界面窗口位置居中,大小固定
    def center(self):
        self._ui_root.resizable(False, False)#禁止修改窗口大小
        ws = self._ui_root.winfo_screenwidth()
        hs = self._ui_root.winfo_screenheight()
        x = int((ws / 2) - (self._ui_width / 2))
        y = int((hs / 2) - (self._ui_height / 2))
        self._ui_root.geometry('{}x{}+{}+{}'.format(self._ui_width, self._ui_height, x, y))


def main():
    app = App()
    app.update_song_list()
    app.is_over()
    app.root.mainloop()


#查看播放列表
#def get_dict():
    #app = App()
    #app.update_song_list()
    #print(app.play_dict)


if __name__ == '__main__':
    main()
    #get_dict()


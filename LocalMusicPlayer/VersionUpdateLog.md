#版本更新日志

Update log:
project start at 2023/6/14

fix issues:
    2023/6/20 ~ 2023/6/25
      1.1.1.添加了"暂停|开始"控件与"随机播放"控件在点击时对应的"暂停|开始"控件的文本变化,并修改了"暂停|开始"控件的作用域,为APP(<class 'type'>)全局.
      1.1.2.修复了播放状态下,点击"暂停"控件后再点击"上一首"控件或"下一首"控件时出现的异常.
      1.1.3.为每个具有播放功能的控件添加了 #确保解密/确保对象类型为int 的操作.
      1.1.4.更改了 update_song_list() 的部分代码描述.
      1.1.5.将UI窗口搭建(build_platform()) 与 窗口居中且固定大小(center()) 的调用默认到APP(<class 'type'>)对象的创建(__init__)中.
      1.1.6.在update_song_list()中添加了随机播放操作,使得程序打开即可播放.(在2.0版本中暂时取消)
    2023/7/9 ~ 2023/7/10
      3.0.1.为上一首(按钮操作)与下一首(按钮操作)添加了错误提示.
add function:
    2023/6/14 ~ 2023/6/19
      1.0.0.has been finished
    2023/7/2 ~ 2023/7/3
      2.0.1.添加了主UI菜单"更改文件夹",来选择自己喜欢的播放列表.
            原理: 多级菜单,下拉菜单项与目标文件夹路径的绑定.
      2.0.2.添加了主UI界面中对当前播放的音乐文件名称显示的功能.
            原理: 标签(_current_play_label) 跟随 self._current_music_number 的动态变化.
    2023/7/4 ~ 2023/7/6
      2.1.1.添加了查找歌曲进行定向播放的功能,即菜单"查找歌曲"中的二级UI界面.
            原理: 主要体现为 文本输入框(entry由tkinter.Entry创建), 搜索按钮(searching()), 树型图表的显示(self._treeview_search_result),树型图表内鼠标事件(onclick()), 播放按钮(second_ui_play()), 关闭协议(second_ui_root_protocol()) 的组合与应用.
    2023/7/9 ~ 2023/7/10
      3.0.2.添加了播放完成检测操作,来保证良好的听歌体验.
            原理: 在App启动时将开启一个新的子线程 递归函数(is_over()) 来监测文件的播放进度,当文件播放至结尾时将进行一系列操作(如随机播放下一首),该函数将持续到App关闭.当前 递归函数(is_over()) 的递归间隔为3000ms,自动切歌时比较比较流畅.
      3.0.3.添加了单曲循环功能按钮.
            原理: 通过按钮来改变 循环标志(self._need_cycle) ,依此来切换 播放完成检测(is_over()) 中的播放方法(play_song()|random_play())




""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """
1.0版本源码 QwQ:该版本现已无法正常运行,仅将其置于此作为纪念
"""
Maker: HDJ
Start at: 2023/6/14
Last modified date: 2023/6/18
"""
import tkinter
import tkinter.messagebox
import glob
import os
import random
import pyglet


class App(object):

    def __init__(self, width=500, height=400):
        self._ui_width = width
        self._ui_height = height
        self._ui_title = '音乐播放器'
        self._ui_root = tkinter.Tk(className=self._ui_title)#创建一个名称为self._ui_titled的窗口
        self._play_dict = {}
        self._current_music_number = None
        self._player = None#播放器
        self._current_position = None#当前(文件的)播放位置
        #此处修改音乐文件夹的绝对路径
        self.music_file_path = '\\py.1求道境\\1.tkinter模块\\音乐随机播放器\\music'

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
        # 音乐文件夹
        music_file_path = self.music_file_path
        # 获取mp3路径列表
        mp3_files_list = glob.glob(os.path.join(music_file_path, '*.mp3'))
        # 创建播放字典
        for music_number, music_path in enumerate(mp3_files_list, start=1):
            self._play_dict[f'{music_number}'] = f'{music_path}'

    #播放音乐
    def play_song(self, music_position=0):
        #加载音乐文件
        music_file_path = self._play_dict.get(f'{self._current_music_number}')
        #根据文件创建music对象
        music = pyglet.media.load(music_file_path)
        #创建播放器
        self._player = pyglet.media.Player()
        #将music对象添加到播放器(player)
        self._player.queue(music)
        #调整播放位置
        self._player.seek(music_position)
        #开始播放
        self._player.play()

    # 随机播放(按钮操作)
    def random_play(self):
        if self._current_music_number is not None:
            self._player.pause()
            self._player.delete()
        self._current_music_number = random.randint(0, 8)
        self.play_song()

    # 上一首(按钮操作)
    def previous_play(self):
        self._player.pause()
        self._player.delete()
        self._current_music_number -= 1
        if self._current_music_number == 0:
            self._current_music_number = len(self._play_dict)
        self.play_song()

    # 下一首(按钮操作)
    def next_play(self):
        self._player.pause()
        self._player.delete()
        self._current_music_number += 1
        if self._current_music_number > len(self._play_dict):
            self._current_music_number = 1
        self.play_song()

    #暂停||开始(按钮操作)
    def music_pause(self):
        # 开始路径1:如果之前无播放内容,则随机播放  QwQ:克服选择困难症
        if self._current_music_number is None:
            self.random_play()
            #按钮文本显示为"暂停"

        # 开始路径2:之前有播放内容被暂停,点击按钮继续播放
        elif type(self._current_music_number) == str:# QwQ:通过类型的转化来区分路径
            self._current_music_number = int(self.current_music_number.replace('*', ''))
            self.play_song(self._current_position)
            self._current_position = None

        # 当前有文件正在播放,点击按钮暂停
        else:
            self._current_position = self._player.time
            self._player.pause()
            self._current_music_number = f'*{self._current_music_number}'# QwQ将当前播放序号在转类型的时候稍微加密
            # 按钮文本显示为"开始"

    # 确认退出(按钮操作)
    def confirm_to_quit(self):
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
            self._ui_root.quit()

    # UI搭建
    def build_platform(self):
        # 创建一个主体文字标签
        text_label = tkinter.Label(self._ui_root, text='Q*& 私人专属音乐播放工具 Qwq', font=("楷体", 16), fg='red')
        text_label.pack(expand=1)

        # 控件设置
        # 框架
        frame1 = tkinter.Frame(self._ui_root)
        frame1.pack()
        frame2 = tkinter.Frame(self._ui_root)
        frame2.pack()
        frame3 = tkinter.Frame(self._ui_root)
        frame3.pack()

        # f1
        button_previous = tkinter.Button(frame1, text='上一首', command=self.previous_play)
        button_previous.pack(side='left')
        button_next = tkinter.Button(frame1, text='下一首', command=self.next_play)
        button_next.pack(side='right')
        button_pause = tkinter.Button(frame1, text='暂停', command=self.music_pause)
        button_pause.pack(side='top')
        # f2
        button_shuffle = tkinter.Button(frame2, text='随机播放', command=self.random_play)
        button_shuffle.pack()
        button_quit = tkinter.Button(frame2, text='退出', command=self.confirm_to_quit)
        button_quit.pack()
        # f3
        label_explain = tkinter.Label(frame3, text='此工具仅用于学术交流!', font=("楷体", 10), fg='blue')
        label_explain.pack()

    #窗口位置居中,大小固定
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
    app.build_platform()
    app.center()
    app.root.mainloop()


#查看播放列表
def get_dict():
    app = App()
    app.update_song_list()
    print(app.play_dict)


if __name__ == '__main__':
    main()
    #get_dict()

""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """


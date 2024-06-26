# 项目简介

## 功能说明
- 该项目是一个基于文件资源管理器与本地音频文件的基础音乐播放器,具有简单的样式美化,简单的文件管理功能以及简单的播放功能.
 
## 使用说明

#### 运行
1. 直接运行打包好的exe文件
2. 导入播放列表
   - 在**设置-歌单界面**点击"初始化播放列表"按钮,选择符合要求的目录作为播放列表.
   - 播放列表(目录)应当是一个**三级目录**,且符合:总目录->歌单分组->歌单(歌曲列表).仅歌单(歌曲列表)这一级目录储存音频文件(其余级目录下的音频将无法加载).
3. 选择歌单(歌曲列表)
   - 导入成功后,在**设置-歌单界面**先选择歌单分组,再选择歌单(歌曲列表),然后就可以进行播放了.
  
#### 打包
- 一般通过将入口文件(main)打包为exe文件, 将所需要的资源文件/目录添加到运行环境(目录)即可正常运行.

    |资源文件|资源目录|
    |:---:|:---:|
    | 暂无|source, profiles, phbimage|

#### 使用的包
- python版本: 3.12.0
- 部分包为较新版本,但不代表低版本不可用.

    |包名|版本|
    |:-|:-|
    keyboard                  |0.13.5
    numpy                     |1.26.4
    pinyin                    |0.4.0
    pyglet                    |2.0.10
    pynput                    |1.7.6
    PyQt5                     |5.15.10

## GUI展

#### APP主界面:
<center>
<img src="phbimage/GUI_presentation/GUI1.png" alt="GUI1" width="300" height="200">
</center>

#### 歌曲搜索界面:
<center>
<img src="phbimage/GUI_presentation/GUI2.png" alt="GUI2" width="300" height="200">
</center>

#### 设置-歌单界面:
<center>
<img src="phbimage/GUI_presentation/GUI3.png" alt="GUI3" width="300" height="200">
</center>


<center>
<img src="phbimage/GUI_presentation/GUI4.png" alt="GUI4" width="300" height="200">
</center>

#### 设置-背景图界面:
<center>
<img src="phbimage/GUI_presentation/GUI5.png" alt="GUI5" width="300" height="200">
</center>

#### 设置-快捷键界面:
<center>
<img src="phbimage/GUI_presentation/GUI6.png" alt="GUI6" width="300" height="200">
</center>

<center>
<img src="phbimage/GUI_presentation/GUI7.png" alt="GUI7" width="300" height="200">
</center>

#### 设置-配置文件界面:
<center>
<img src="phbimage/GUI_presentation/GUI8.png" alt="GUI8" width="300" height="200">
</center>

# Update log:

## 2024/4↓

#### 2.16.21
1. 修复了自2.14.19版本由于代码复用导致设置-歌单界面,"移动到其他歌单","复制到其他歌单"两个按钮无法正常使用的问题.
2. 修复了自2.15.19版本由于自定义快捷键方案的初始化后,用户未添加快捷键但启用自定义方案时触发异常的问题.
3. 去除了部分冗余代码.
4. 将所有弹出窗口的标题设置为APP标题.
5. 优化了设置-歌单界面"创建新歌单","创建新歌单"两个按钮的方法: 添加了部分情况的提示窗.
6. QwQ:项目阶段性打包.

#### 2.16.20
1. 为了便于本地打包项目,将程序入口(main)置于源码包(source)外.
2. 优化了部分数据初始化方法.
3. 优化了设置-配置文件界面"打开文件"按钮的方法(动态获取绝对路径).

#### 2.16.19
1. 在设置-背景图界面添加了初始化按钮,用于将全部可更改的图片图标恢复默认设置.
2. 为设置-背景图界面的"更改图片", "更改图标"按钮同样追加了预览图片/图标刷新的方法.

#### 2.15.19
1. 在设置-快捷键界面添加了初始化按钮,用于清空快捷键设置.
2. 添加了配置数据的初始化检测方法.

#### 2.14.19
1. 在设置-歌单界面添加了初始化按钮,用于播放列表的导入.

#### 2.13.19
1. 修复了设置-歌单界面,"移动到其他歌单","复制到其他歌单"两个按钮操作的逻辑问题.

#### 2.13.18
1. 在设置-歌单界面添加了"创建新歌单","创建新歌单"两个按钮.
2. 进行了代码规范--对部分变量名进行调整.

## 2024/3↓

#### 2.12.18
1. 优化了代码结构,使用包结构管理.

#### 2.11.18
1. 优化了歌曲搜索过程, 以及歌曲搜索界面树形图与APP界面的文本显示规则.
2. QwQ:项目阶段性打包.

#### 2.11.17
1. 修复了切换歌单后, 播放序号与位置异常的情况.现改为从切换后的歌单第一首的第0秒开始.

#### 2.11.16
1. 修复了部分情况下,歌单设置界面歌单项下拉列表不显示文本的问题.
2. 修复了部分音频类型的文件无法显示和播放的问题.

#### 2.11.15
1. 将歌单的切换功能移动至设置UI界面,新增了歌单的显示.

#### 2.11.14
1. 新增了自定义快捷键界面组件可选中性的的变化.

## 2024/2↓

#### 2.10.14
1. 将歌曲查询界面的入口移动到设置菜单下.

#### 2.10.13
1. 将键盘快捷方式的切换移至设置UI界面, 新增了自定义快捷键功能, 仅能够储存一套自定义方案.

#### 2.9.13
1. 将配置文件的打开操作移至设置UI界面.

#### 2.9.12
1. 添加了设置UI界面, 并新增更换窗口背景图/图标功能. 其余部分功能将逐步移入设置UI.

#### 2.8.12
1. 将MyWidgetMethod.py模块名变更为Simple_Qt.py,更改了部分方法名称,并优化了部分方法实现以及描述.
2. 添加了对布局(Layout)的简单集成.
3. 同时,Simple_Qt.py模块的维护更新将独立出该项目,且不再出现在日志中.

## 2024/1 ↓

#### 2.8.11
1. 将整个项目拆分为多个文件管理
   
    |拆分后的文件名|
    |---|
    MusicPlayer.py
    ApplicationWindow.py
    DataProtector.py
    IsOverMonitor.py
    KeyboardListener.py
    SearchUI.py
    SettingMenu.py
    SongListMenu.py

## 2023/12 ↓

#### 2.7.11
1. 优化了所有级菜单的创建过程.
    原理: 在模块`MyWidgetMethod.py`, 新增内容:
    - PackingCreateMethod <class 'type'>
    - my_menu()
    - my_action()
2. QwQ:项目阶段性打包.

#### 2.6.11
1. 为全部菜单添加了基础样式,为部分菜单项添加了图标.

#### 2.6.10
1. 添加了一个新的全局变量.
原理: 使用`os.path.dirname(os.path.abspath(__file__)) + r'\phbimage'` 获取图片文件夹路径保存到 *IMAGE_FOLDER_PATH*.

#### 2.6.9
1. 优化了部分代码 
主要变动: 简化了QMessageBox各类消息框的按键内容;将不必要,不常变动的代码换行取消 

#### 2.6.8
1. 优化了界面布局. 
主要变动: 更改了部分组件的大小,位置,以及文本对齐方式. 

#### 2.6.7
1. 添加了一个自定义模块,增强了可维护性,实现了部分代码的复用.
原理: 新增模块名 `MyWidgetMethod.py`, 新增内容:
   - PackingCreateMethod <class 'type'>
     - my_label()
     - my_button()
   - PackingModificationMethod <class 'type'>
     - set_desktop_center() 
     - set_background_image()

#### 2.5.7
1. 优化了代码格式,名称.
主要变动: 所有类,类方法的注释置于声明下方;将快捷键方案管理函数名称 *change_key_press_programme* 改为 *concentrate_key_press_programme*

#### 2.5.6
1. 优化了代码结构.
原理: 将访问配置文件的相关操作封装到 *ConfigurationFilesMenu <class 'type'>* (*SettingMenu <class 'type'>* 的内部类)

#### 2.4.6
1. 统一了类名,菜单相关操作类: __Menu
主要变动: 将 *ChangeKeyPressProgramme* 改为 *ChangeKeyPressProgrammeMenu* .

#### 2.4.5
1. 更改了部分逻辑.
原理: 将原播放完成检测功能拆分为两个函数 *is_over() <IsOverMonitor 'method'>* (用于检测播放是否完成并返回布尔值) 和 *which_play() <IsOverMonitor 'method'>* (用于在播放完成需进行继续播放时切换播放方式)

## 2023/11 ↓

#### 2.4.4
1. 设置了一个全局变量.
原理: 使用 `os.path.dirname(os.path.abspath(__file__))` 获取工作目录路径保存到 *WORKING_DIRECTORY_PATH*.

#### 2.4.3
1. 添加了设置菜单,并添加了配置文件的访问.
原理: 相关操作封装到*SettingMenu <class 'type'>*, 通过系统默认的程序打开文件.
目前仅两个文件: *.json* *.css*

#### 2.3.3
1. 更改了部分逻辑.
主要变动: *change_label_current_play_content()<ApplicationWindow 'method'>* 方法将通过 *play_song()<ApplicationWindow 'method'>* 方法调用.保证标签的正确显示.

#### 2.3.2
1. 删除了一些冗余代码.
主要变动: 移除了对 *Player()<class 'pyglet.media.player.Player'>* 对象的所有 *delete()* 操作.

#### 2.3.1
1. 修复一项重大问题.
BUG描述: 歌曲正在播放时切换文件夹后连续点击 *开始/暂停按钮* 两次对当前歌曲进行继续播放,当切换后的文件夹文件数*较(切换前)多*时错误的播放切换后文件夹中的内容,当切换后文件夹文件数*较(切换前)少*时导致程序卡顿退出.
前者通2.3.3.已修复,后者在 *play_song() <ApplicationWindow 'method'>* 方法通过异常处理机制,在底层变量类型错误时抛出错误提示,引导使用者进行正确操作.

#### 2.3.0
1. 优化了 *更改文件夹* 菜单的创建过程
主要变动: 修改了 *PlayerConfig.json* 中设置文件夹名称与路径项(*music_folders_path*) 的储存方式,即使用三层嵌套列表来控制菜单结构.并且,菜单创建时使用嵌套循环来减少重复的代码.

#### 2.2.0
1. 添加了基本的样式设置.
原理: 使用 *PlayerStyle.css* 文件进行样式的配置.目前样式的更改仅通过修改CSS文件.

#### 2.1.0
1. 将部分组件的名称规范化,最终名称如下: 
   
    |用途|名称|
    :--|:--
    一级UI主体标签|*label_MainWindow_main_text*
    "正在播放"标签|*label_current_play_text*
    显示当先正在播放歌曲名称的标签|*label_current_play_content*
    上一首按钮|*button_previous*
    下一首按钮|*button_next*
    开始/暂停按钮|*button_pause_or_begin*
    随机播放按钮|*button_shuffle_play*
    单曲循环按钮|*button_single_loop*
    退出按钮|*button_quit*
    提示标签|*label_warning_text*
    菜单栏|*menubar*
    SearchUI主体标签设置|*label_SearchUI_main_text*
    "当前文件夹(库名):"标签|*label_folder_path_text*
    显示当前文件夹路径的标签|*label_current_folder*
    输入提示文本标签|*label_input_reminder_text*
    输入框|*lineEdit_input_song_title*
    搜索按钮|*button_searching*
    用于显示搜索结果的树形图|*treeview_search_result*
    播放所选歌曲按钮|*button_play_selected_song*
    注意事项文本标签|*label_use_attention_text*

#### 2.0.0
1. 对UI界面进行了重构
主要变动: 使用PyQt5模块在保持原功能不变的基础上重新构建了所有UI界面.类名 *APP* 改为 *ApplicationWindow*

#### 1.14.10
1. 将本地音乐文件夹路径配置设置在 *PlayerConfig.json* 文件
主要变动: 

    |新增key|
    |---|
    |  *"music_folders_path"*  |
2. QwQ:项目阶段性打包.

## 2023/10 ↓

#### 1.14.9
1. 添加了本地数据保存功能.
原理: 使用 *PlayerConfig.json* 文件进行部分底层数据的初始化,以及一些关键数据的储存.

    | 新增key|
    |----|
    |  *"music_folder_path"*  |
    |  *"current_music_number"*  |
    |  *"file_total_time"*  |
    |  *"current_position"*  |
    |  *"need_cycle"*  |
    |  *"key_press_programme"*  |
    |  *"current_music_name"*  |
    |  *"play_dict"*  |

#### 1.13.9
1. 优化了代码格式
主要变动: 将全部抽象的代码简单化,格式化.

## 2023/9 ↓

#### 1.13.8更改了一类冗余写法.
1. 主要变动: 将r"xx\xx\xx".replace('\\', '\\\\')的写法简化成r"xx\xx\xx" 

#### 1.13.7
1. 解决了一个编码隐患.
主要变动: 弃用非UTF-8编码的'♥️',启用UTF-8编码的'❤️'.

#### 1.13.6
1. 添加了主UI菜单"快捷方式".
原理: 将键盘快捷方案的切换关联到该菜单.详见 *ChangeKeyPressProgramme <class 'type'>* ;

#### 1.12.6
1. 添加了快捷键方案管理函数.
原理: 详见 *change_key_press_programme() <KeyboardListener 'method'>* 

#### 1.12.5
1. 添加了新的键盘快捷键方案.
原理: 键盘快捷键方案( *key_press_p3() <KeyboardListener 'method'>* :数字键盘, *key_press_p4() <KeyboardListener 'method'>* :Ctrl+数字键盘(方案4当前使用的第三方库无法区分主键盘与数字键盘的数字键))

#### 1.11.5
1. 添加了新功能:键盘快捷键.
原理: 在App启动时将开启一个新的子线程(所有相关操作封装到 *KeyboardListener <class 'type'>*) 来监听键盘事件;可以在播放器UI界面最小化时更便捷的进行一些基本操作(下一首,上一首,暂停/开始,随机播放,单曲循环).
2. 提供了2套键盘快捷键方案( *key_press_p1() <KeyboardListener 'method'>* :主键盘+方向键, *key_press_p2() <KeyboardListener 'method'>* :Ctrl+主键盘)

#### 1.10.5
1. 优化了代码结构
主要变动: 将 播放完毕检测功能 的所有实例与方法从 *APP <class 'type'>* 中剥离,并整合到一个新的局部类 *IsOverMonitor <class 'type'>* 中.

## 2023/7 ↓

#### 1.9.5
1. 优化了代码结构
主要变动: 将一级菜单 *更改文件夹* 的所有属性与方法从 *APP <class 'type'>* 中剥离,并整合到一个新的局部类 *ChangeFolderMenu <class 'type'>* 中.

#### 1.8.5
1. 优化了代码结构
主要变动: 将所有变量的保护属性移除;将 *歌曲搜索界面* 的所有属性与方法从 *APP <class 'type'>* 中剥离,并整合到一个新的局部类 *SearchUI <class 'type'>* 中,增强代码可读性,便于代码查找,修改与增添.

#### 1.7.5
1. 添加了单曲循环功能按钮.
原理: 通过按钮来改变 循环标志 *self._need_cycle* ,依此来切换 播放完成检测 *is_over() <APP 'method'>* 中的播放方法 *play_song() <APP 'method'>* | *random_play() <APP 'method'>* 

#### 1.6.5
1. 添加了播放完成检测操作,来保证良好的听歌体验.
原理: 在App启动时将开启一个新的子线程 递归函数 *is_over() <APP 'method'>* 来监测文件的播放进度,当文件播放至结尾时将进行一系列操作(如随机播放下一首),该函数将持续到App关闭.当前,递归函数的递归间隔为3000ms,自动切歌时比较比较流畅.

#### 1.5.5
1. 为上一首(按钮操作)与下一首(按钮操作)添加了错误提示.

#### 1.5.4
1. 添加了查找歌曲进行定向播放的功能,即菜单"查找歌曲"中的二级UI界面.
原理: 主要体现为下述实例与方法的组合应用 文本输入框 *entry*由*tkinter.Entry* 创建, 搜索按钮 *searching()* , 树型图表的显示 *self._treeview_search_result* ,树型图表内鼠标事件 *onclick() <APP 'method'>* , 播放按钮绑定 *second_ui_play() <APP 'method'>* , 关闭协议 *second_ui_root_protocol() <APP 'method'>* .

#### 1.4.4
1. 添加了主UI界面中对当前播放的音乐文件名称显示的功能.
原理: 标签 *_current_play_label* 跟随 *self._current_music_number* 的动态变化.

#### 1.3.4
1. 添加了主UI菜单 *更改文件夹* ,来选择自己喜欢的播放列表.
原理: 多级菜单,下拉菜单项与目标文件夹路径的绑定.

## 2023/6 ↓

#### 1.2.4
1. 将UI窗口搭建 *build_platform() <APP 'method'>* 与窗口居中且固定大小 *center() <APP 'method'>* 的调用绑定到 *APP <class 'type'>* 对象的构造函数中. 

#### 1.2.3
1. 更改了 *update_song_list() <APP 'method'>* 的部分代码描述.

#### 1.2.2
1. 为每个具有播放功能的控件添加了 #确保解密/确保对象类型为int 的操作.

#### 1.1.2
1. 修复了播放状态下,点击"暂停"控件后再点击"上一首"控件或"下一首"控件时出现的异常.

#### 1.1.1
1. 修改了"暂停|开始"控件的作用域,为 *APP <class 'type'>* 全局.

#### 1.1.0
1. 添加了"暂停|开始"控件与"随机播放"控件在点击时对应的"暂停|开始"控件的文本变化.

#### 1.0.0.
- 1.0.0.has been finished 
  
#### start
- project start at 2023/6/14



""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """
#### 1.0版本源码 QwQ:该版本现已无法正常运行,仅将其置于此作为纪念
```
# code block
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
```
""" """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """ """


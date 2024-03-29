'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-03-15 22:29:09
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\SettingPages.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import os
import sys
import time
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QGroupBox, QLineEdit, QFileDialog, 
QMessageBox, QSpacerItem, QSizePolicy, QFrame, QComboBox, QCheckBox, QLabel, QListWidget)
from PyQt5.QtGui import QPixmap
from Simple_Qt import Label, PushButton, Layout
from DataProtector import config_js
from ShortcutEditer import ShortcutEditer, DEFAULT_STYLE

class PageSongList(QScrollArea):

    def __init__(self, parent: QWidget | None = None, app = None) -> None:
            super().__init__(parent)
            self.app = app
            self.setStyleSheet("QScrollArea { border: transparent; }")
            self.setWidgetResizable(True) # 组件可调整大小属性
            self.fst_items_name = [sub_list[0] for sub_list in config_js['music_folders_path'] if isinstance(sub_list[0], str)]
            self.current_sec_items_name = []
            self.selected_subitem_AP = None
            self.construct()


    def construct(self) -> None:
        """ 页面UI搭建 """
        # 主布局
        # 中心组件
        self.central_widget = QGroupBox(None, self)
        self.central_widget.setStyleSheet("QGroupBox { border: none; }")
        self.central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))# 设置中心组件拉伸限制
        
        main_layout = Layout.create(name="QVBoxLayout", parent=self, children=[self.central_widget])

        # 中心组件布局
        widget1 = QGroupBox(self.central_widget)
        widget1.setStyleSheet("QGroupBox { background-color: #fdfdfd; }")
        
        widget2 = QGroupBox(self.central_widget)
        widget2.setStyleSheet("QGroupBox { background-color: #fdfdfd; }")

        central_widget_layout = Layout.create(
            name="QVBoxLayout", parent=self.central_widget, 
            children=[widget1, widget2])
        
        # widget1布局
        label1 = Label.create(
            parent=self.central_widget, text="歌单分组", 
            StyleSheet=
            """
            QLabel { font-family: 楷体; font-size: 38px; font-weight: bold;} 
            """
        )

        label2 = Label.create(
            parent=self.central_widget, text="歌单", 
            StyleSheet=
            """
            QLabel { font-family: 楷体; font-size: 38px; font-weight: bold;} 
            """
        )

        self.comboBox1 = QComboBox()
        self.comboBox1.addItems(self.fst_items_name)
        self.comboBox1.currentIndexChanged.connect(self.comboBoxIndexChanged1)
        self.comboBox1.installEventFilter(self)

        self.comboBox2 = QComboBox()
        for fst_items in config_js['music_folders_path']:
            if fst_items[0] == config_js['current_playlist_category']:
                self.current_sec_items_name = [sub_list[0] for sub_list in fst_items if isinstance(sub_list, list)]
        self.comboBox2.addItems(self.current_sec_items_name)
        self.comboBox2.currentIndexChanged.connect(self.comboBoxIndexChanged2)
        self.comboBox2.installEventFilter(self)
        
        self.comboBox1.setCurrentText(config_js['current_playlist_category']) # 设置下拉列表1的初始状态
        self.comboBox2.setCurrentText(os.path.basename(config_js['music_folder_path'])) # 设置下拉列表2的初始状态
        
        widget1_layout = Layout.create(
            name="QVBoxLayout", parent=widget1, 
            children=[label1, self.comboBox1, label2, self.comboBox2])
        
        # widget2布局
        button1 = PushButton.create(
            parent=widget2, text="移动到其他歌单", clicked_callback=self.move_to_other_playlist)
        button2 = PushButton.create(
            parent=widget2, text="复制到其他歌单", clicked_callback=self.copy_to_other_playlist)
        button3 = PushButton.create(
            parent=widget2, text="从当前歌单移除", clicked_callback=self.removed_from_the_current_playlist)

        layout1 = Layout.create(name='QHBoxLayout', children=[button1, button2, button3])

        self.listWidget = QListWidget(widget2)
        self.listWidget.setStyleSheet(" QListWidget { min-height: 350px; border: none; } ")
        self.listWidget.addItems(self.get_all_audio_files_in_folder(config_js['music_folder_path']))
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        widget2_layout = Layout.create(name="QVBoxLayout", parent=widget2, children=[layout1, self.listWidget])

        # 将中心组件设置为滚动内容
        self.setWidget(self.central_widget)

    def on_item_clicked(self, item):
        file_name = item.text()
        self.selected_subitem_AP = os.path.join(config_js['music_folder_path'], file_name) # 获取选中子项对应文件的绝对路径
    
    def move_to_other_playlist(self) -> None:
        """移动到其他目录"""
        if self.selected_subitem_AP:
            # 检测选中的子项对应的文件是否存在
            if os.path.exists(self.selected_subitem_AP):
                object_file_name = os.path.basename(self.selected_subitem_AP)  # 目标文件名
                # 文件对话框设置
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog  # 使用Qt的文件对话框，而不是本地对话框
                file_dialog = QFileDialog()
                file_dialog.setOptions(options)
                file_dialog.setDirectory(os.path.dirname(config_js['music_folder_path'])) # 设置文件对话框的初始位置为当前歌单的上级目录
                # 打开文件对话框,获取用户所选目录绝对路径
                folder_path = file_dialog.getExistingDirectory(self, '选择目标歌单')
                # 检查目标目录是否存在同名文件
                if os.path.exists(os.path.join(folder_path, object_file_name)):
                    # 弹出提示框询问用户是否覆盖文件
                    response = QMessageBox.question(
                        self,
                        '文件已存在',
                        '目标目录中已存在同名文件，是否要覆盖?',
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if response == QMessageBox.No:
                        return  # 如果用户选择不覆盖，则结束操作
                # 读取目标文件内容
                with open(self.selected_subitem_AP, 'rb') as file:
                    content = file.read()
                # 将目标文件添加到目标目录
                with open(os.path.join(folder_path, object_file_name), 'wb') as file:
                    file.write(content)
                # 删除文件
                os.remove(self.selected_subitem_AP)
                # 将选中状态置空
                self.selected_subitem_AP = None
                # 完成提示
                items_to_delete = self.listWidget.findItems(object_file_name, Qt.MatchExactly) # 查找包含目标文件名的项
                # 如果找到匹配的项，删除第一个匹配项
                if items_to_delete:
                    item = items_to_delete[0]
                    row = self.listWidget.row(item)
                    self.listWidget.takeItem(row)
            else:
                QMessageBox.critical(self, 'FileNotFoundError', '文件不存在!', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'warning', '未选中文件!', QMessageBox.Ok)

    def copy_to_other_playlist(self) -> None:
        """复制到其他目录"""
        if self.selected_subitem_AP:
            # 检测选中的子项对应的文件是否存在
            if os.path.exists(self.selected_subitem_AP):
                object_file_name = os.path.basename(self.selected_subitem_AP)  # 目标文件名
                # 文件对话框设置
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog  # 使用Qt的文件对话框，而不是本地对话框
                file_dialog = QFileDialog()
                file_dialog.setOptions(options)
                file_dialog.setDirectory(os.path.dirname(config_js['music_folder_path'])) # 设置文件对话框的初始位置为当前歌单的上级目录
                # 打开文件对话框,获取用户所选目录绝对路径
                folder_path = file_dialog.getExistingDirectory(self, '选择目标歌单')
                # 检查目标目录是否存在同名文件
                if os.path.exists(os.path.join(folder_path, object_file_name)):
                    # 弹出提示框询问用户是否覆盖文件
                    response = QMessageBox.question(
                        self,
                        '文件已存在',
                        '目标目录中已存在同名文件，是否要覆盖?',
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if response == QMessageBox.No:
                        return  # 如果用户选择不覆盖，则结束操作
                # 读取目标文件内容
                with open(self.selected_subitem_AP, 'rb') as file:
                    content = file.read()
                # 将目标文件添加到目标目录
                with open(os.path.join(folder_path, object_file_name), 'wb') as file:
                    file.write(content)
                # 将选中状态置空
                self.selected_subitem_AP = None
                # 完成提示
                QMessageBox.information(self, 'information', "复制成功")
            else:
                QMessageBox.critical(self, 'FileNotFoundError', "文件不存在!", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'warning', "未选中文件!", QMessageBox.Ok)
            
    def removed_from_the_current_playlist(self) ->None:
        """从当前文件夹删除目标文件, 并添加到"最近删除"目录"""
        if self.selected_subitem_AP:
            song_library_path = os.path.dirname(config_js['music_folder_path']) # 获取曲库路径
            recently_deleted_directory_path = os.path.join(song_library_path, "最近删除") # "最近删除"目录路径

            # 检测曲库中是否有"最近删除"目录, 如果不存在，则创建"最近删除"目录
            if not os.path.exists(recently_deleted_directory_path):
                os.makedirs(recently_deleted_directory_path)
            else:
                # 检测选中的子项对应的文件是否存在
                if os.path.exists(self.selected_subitem_AP):
                    object_file_name = os.path.basename(self.selected_subitem_AP)  # 目标文件名
                    # 检查是否已存在相同文件名的文件
                    existing_files = [f for f in os.listdir(recently_deleted_directory_path) if f.startswith(object_file_name)]
                    count = 1
                    new_file_name = object_file_name
                    # 若目标目录存在目标文件名,则使用"目标文件名(1)"依此类推
                    while new_file_name in existing_files:
                        count += 1
                        base_name, extension = os.path.splitext(object_file_name)
                        new_file_name = f"{base_name}({count}){extension}"
                    # 读取目标文件内容
                    with open(self.selected_subitem_AP, 'rb') as file:
                        content = file.read()
                    # 将要删除的文件添加到"最近删除"目录
                    with open(os.path.join(recently_deleted_directory_path, new_file_name), 'wb') as file:
                        file.write(content)
                    # 删除文件
                    os.remove(self.selected_subitem_AP)
                    # 将选中状态置空
                    self.selected_subitem_AP = None
                    # 完成提示
                    items_to_delete = self.listWidget.findItems(object_file_name, Qt.MatchExactly) # 查找包含目标文件名的项
                    # 如果找到匹配的项，删除第一个匹配项
                    if items_to_delete:
                        item = items_to_delete[0]
                        row = self.listWidget.row(item)
                        self.listWidget.takeItem(row)
                else:
                    QMessageBox.critical(self, 'FileNotFoundError', "文件不存在!", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'warning', "未选中文件!", QMessageBox.Ok)

    def get_all_audio_files_in_folder(self, folder_path: str) -> list:
        """获取所选文件夹下的全部音频文件名称"""
        audio_files = []
        
        if folder_path:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path): # 判断file_path指向的是否为文件
                    base_name, file_extension = os.path.splitext(file_name) # 分离文件名基本部分与拓展名
                    if file_extension.lower() in config_js['audio_file_suffix']: # 检查文件的小写拓展名是否符合要求
                        audio_files.append(file_name)

        return audio_files


    def comboBoxIndexChanged1(self, index) -> None:
        """处理下拉列表选择变化事件1"""
        combo_box = self.central_widget.sender()  # 获取发射信号的对象
        selected_item = combo_box.currentText()# 获取选定选项的文本内容
        config_js['current_playlist_category'] = selected_item
        for fst_item_name in self.fst_items_name:
            # 在歌单分组名中查找选中项文本
            if fst_item_name == selected_item:
                self.comboBox2.clear()
                # 根据匹配的歌单分组名在歌单分组名列表中的索引,获取该歌单分组下的全部歌单名称
                sec_items = [sub_folder[0] for sub_folder in config_js['music_folders_path'][self.fst_items_name.index(fst_item_name)][1:]]
                self.comboBox2.addItems(sec_items)
    
    def comboBoxIndexChanged2(self, index) -> None:
        """ 处理下拉列表选择变化事件2 """
        combo_box = self.central_widget.sender()  # 获取发射信号的对象
        selected_item = combo_box.currentText()# 获取选定选项的文本内容
        # 获取当前歌单组在music_folders_path歌单结构中的索引
        for fst_item_name in self.fst_items_name:
            if fst_item_name == config_js['current_playlist_category']:
                fst_index = self.fst_items_name.index(fst_item_name)
        # 逐个获取当前歌单组下的歌单的路径
        for sec_item_path in [sub_folder[1] for sub_folder in config_js['music_folders_path'][fst_index][1:]]:
            # 找到下拉列表所选择的歌单名称, 将其对应的路径赋给app属性
            if os.path.basename(sec_item_path) == selected_item:
                self.app.music_folder_path = sec_item_path
                self.app.update_song_list()
                if hasattr(self, 'listWidget'):
                    self.listWidget.clear()
                    self.listWidget.addItems(self.get_all_audio_files_in_folder(sec_item_path))
        
    def eventFilter(self, obj, event):
        """事件过滤器"""
        if isinstance(obj, QComboBox) and event.type() == QEvent.Wheel:
            # 捕获滚轮事件并忽略
            return True
        # 其他事件正常继承
        return super().eventFilter(obj, event)
        
class PageImageSetting(QScrollArea):
    """ 背景图片/图标设置页面 """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: transparent; }")
        self.setWidgetResizable(True) # 组件可调整大小属性
        self.construct()
    
    def construct(self) -> None:
        """ 页面UI搭建 """
        # 主布局
        # 中心组件
        central_widget = QGroupBox(None, self)
        central_widget.setStyleSheet("QGroupBox { background-color: #fdfdfd; }")
        central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))# 设置中心组件拉伸限制

        main_layout = Layout.create(name='QVBoxLayout', parent=self, children=[central_widget])
        
        # 中心组件布局
        # 容器1
        group_box_1 = QGroupBox("主窗口", central_widget)
        group_box_1.setStyleSheet("QGroupBox { color: gray; }")
        # 分隔线
        line1 = QFrame(self)
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("QFrame { color: #f0f0f0; }")
        # 容器2
        group_box_2 = QGroupBox("歌曲搜素窗口", central_widget)
        group_box_2.setStyleSheet("QGroupBox { color: gray; }")
        # 空白项
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        central_widget_layout = Layout.create(
            name='QVBoxLayout', parent=central_widget, 
            children=[group_box_1, line1, group_box_2, spacer_item]
        )
        
        # 容器1布局
        # 1-1
        label1 = Label.create(parent=group_box_1, text="背景图片: ", StyleSheet="font-size: 30px;")

        label2 = Label.create(parent=group_box_1, Pixmap=QPixmap(config_js['ApplicationWindowBackGround']).scaledToWidth(120))
        # 1-2
        lineEdit1 = QLineEdit(group_box_1)
        lineEdit1.setPlaceholderText(config_js['ApplicationWindowBackGround'])

        button1 = PushButton.create(
            parent=group_box_1, text="更改图片",
            clicked_callback=lambda: self.select_a_file('ApplicationWindowBackGround'),
            StyleSheet="font-size: 30px;"
        )

        layout1 = Layout.create(name='QHBoxLayout', children=[lineEdit1, button1])   
        # 1-3
        label3 = Label.create(parent=group_box_1, text="窗口图标: ", StyleSheet="font-size: 30px;")
        # 1-4
        label4 = Label.create(parent=group_box_1, Pixmap=QPixmap(config_js['ApplicationWindowIcon']).scaledToWidth(80))
       
        lineEdit2 = QLineEdit(group_box_1)
        lineEdit2.setPlaceholderText(config_js['ApplicationWindowIcon'])

        button2 = PushButton.create(
            parent=group_box_1, text="更改图标",
            clicked_callback=lambda: self.select_a_file('ApplicationWindowIcon'),
            StyleSheet="font-size: 30px;"
        )

        layout2 = Layout.create(name='QHBoxLayout', children=[lineEdit2, button2])

        group_box_1_layout =  Layout.create(
            name='QVBoxLayout', parent=group_box_1, 
            children=[label1, label2, layout1, label3, label4, layout2]
        )

        # 容器2布局
        # 2-1
        label5 = Label.create(parent=group_box_2, text="背景图片: ", StyleSheet="font-size: 30px;")

        label6 = Label.create(parent=group_box_2, Pixmap=QPixmap(config_js['SearchUIBackGround']).scaledToWidth(120))
        # 2-2
        lineEdit3 = QLineEdit(group_box_2)
        lineEdit3.setPlaceholderText(config_js['SearchUIBackGround'])

        button3 = PushButton.create(
            parent=group_box_2, text="更改图片",
            clicked_callback=lambda: self.select_a_file('SearchUIBackGround'),
            StyleSheet="font-size: 30px;"
        )

        layout3 = Layout.create(name='QHBoxLayout', children=[lineEdit3, button3])   
        # 2-3
        label7 = Label.create(parent=group_box_2, text="窗口图标: ", StyleSheet="font-size: 30px;")

        label8 = Label.create(parent=group_box_2, Pixmap=QPixmap(config_js['SearchUIIcon']).scaledToWidth(80))
        # 2-4
        lineEdit4 = QLineEdit(group_box_2)
        lineEdit4.setPlaceholderText(config_js['SearchUIIcon'])

        button4 = PushButton.create(
            parent=group_box_2, text="更改图标",
            clicked_callback=lambda: self.select_a_file('SearchUIIcon'),
            StyleSheet="font-size: 30px;"
        )

        layout4 = Layout.create(name='QHBoxLayout', children=[lineEdit4, button4])

        group_box_2_layout =  Layout.create(
            name='QVBoxLayout', parent=group_box_2, 
            children=[label5, label6, layout3, label7, label8, layout4]
        )

        # 将中心组件设置为滚动内容
        self.setWidget(central_widget)
    
    def select_a_file(self, config_js_key) -> None:
         # 创建文件对话框
        file_dialog = QFileDialog()
        # 设置文件对话框的模式为选择文件
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        # 明确指定允许的 MIME 类型为图片
        mime_types = ["image/png", "image/jpeg", "image/bmp", "image/gif"]
        file_dialog.setMimeTypeFilters(mime_types)
        # 显示文件对话框
        file_path, _ = file_dialog.getOpenFileName(None, "选择图片文件")
        # 更改配置文件中的路径
        if file_path:
            # 将新的图片文件路径储存到配置文件
            config_js[config_js_key] = file_path
            time.sleep(0.2)
            reply = QMessageBox.question(self, '', '该操作将在APP关闭后完成,是否立即重启?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 获取当前执行的文件路径
                current_file = sys.argv[0]
                # 重启程序
                os.execv(sys.executable, ['python3', current_file])
            else:
                QMessageBox.information(self, '提示', 'APP将在下次启动时使用新图片', QMessageBox.Ok)


class PageShortcutSetting(QScrollArea):
    """快捷键设置页面"""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: transparent; }")
        self.setWidgetResizable(True) # 组件可调整大小属性
        
        self.items = ["不使用", "主键盘+方向键", "Ctrl+主键盘", "数字键盘", "Ctrl+数字键盘"]
        self.shortcut_content = {
            '0': ["播放下一首", "播放上一首", "暂停/开始播放", "随机播放", "循环播放"],
            '1': ['right', 'left', 'space', 'R', 'O'],
            '2': ['Ctrl+D', 'Ctrl+A', 'Ctrl+S', 'Ctrl+R', 'Ctrl+Q'],
            '3': ['6', '4', '5', '1', '0'],
            '4': ['Ctrl+6', 'Ctrl+4', 'Ctrl+5', 'Ctrl+1', 'Ctrl+0']
        }
        self.shortcutEditer_group = []
        self.widget2_optional_neutral = None

        self.construct()
        
    def construct(self) -> None:
        """ 页面UI搭建 """
        # 主布局
        # 中心组件
        central_widget = QGroupBox(None, self)
        central_widget.setStyleSheet("QGroupBox { border: transparent; background-color: #f0f0f0; }")
        central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))# 设置中心组件拉伸限制

        main_layout = Layout.create(name='QVBoxLayout', parent=self, children=[central_widget])
        # 中心组件布局
        label1 = Label.create(
            parent=central_widget, text="内置方案", StyleSheet="font-size: 40px; font-weight: bold;")
        
        self.widget1 = QWidget(central_widget)
        self.widget1.setObjectName("QWidget_1")
        self.widget1.setStyleSheet("#QWidget_1 { background-color: #fdfdfd; border: 1px solid #e5e5e5; }")

        label2 = Label.create(
            parent=central_widget, text="自定义方案", StyleSheet="font-size: 40px; font-weight: bold;")
        
        self.widget2 = QGroupBox(None, central_widget)
        self.widget2.setObjectName("QGroupBox")
        self.widget2.setStyleSheet("#QGroupBox { background-color: #fdfdfd; border: 1px solid #e5e5e5; }")

        central_widget_layout =  Layout.create(
            name='QVBoxLayout', parent=central_widget, children=[label1, self.widget1, label2, self.widget2])
        # widget1布局
        label3 = Label.create(parent=self.widget1, text="选择与键盘适配的方案", StyleSheet="font-size: 30px; ")

        self.combobox = QComboBox(self.widget1)
        self.combobox.addItems(self.items)
        self.combobox.setCurrentText(self.items[int(config_js['key_press_programme'])])
        self.combobox.setStyleSheet("font-size: 30px; ")
        self.combobox.currentIndexChanged.connect(self.comboBoxIndexChanged)
        self.combobox.installEventFilter(self) #安装事件过滤器

        layout1 = Layout.create(name='QHBoxLayout', children=[label3, self.combobox])

        # 分隔线
        self.line1 = QFrame(self)
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label4 = Label.create(parent=self.widget1, text="播放下一首", StyleSheet="font-size: 30px; color: #bbbbbb; ")

        self.label9 = Label.create(
            parent=self.widget1, text=self.shortcut_content[config_js['key_press_programme']][0], 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter, StyleSheet="font-size: 30px; color: #bbbbbb; font-weight: bold; ")

        layout2 = Layout.create(name='QHBoxLayout', children=[self.label4, self.label9])

        self.line2 = QFrame(self)
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label5 = Label.create(parent=self.widget1, text="播放上一首", StyleSheet="font-size: 30px; color: #bbbbbb; ")

        self.label10 = Label.create(
            parent=self.widget1, text=self.shortcut_content[config_js['key_press_programme']][1], 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter, StyleSheet="font-size: 30px; color: #bbbbbb; font-weight: bold; ")

        layout3 = Layout.create(name='QHBoxLayout', children=[self.label5, self.label10])

        self.line3 = QFrame(self)
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label6 = Label.create(parent=self.widget1, text="暂停/开始播放", StyleSheet="font-size: 30px; color: #bbbbbb; ")

        self.label11 = Label.create(
            parent=self.widget1, text=self.shortcut_content[config_js['key_press_programme']][2], 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter, StyleSheet="font-size: 30px; color: #bbbbbb; font-weight: bold; ")

        layout4 = Layout.create(name='QHBoxLayout', children=[self.label6, self.label11])

        self.line4 = QFrame(self)
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label7 = Label.create(parent=self.widget1, text="随机播放", StyleSheet="font-size: 30px; color: #bbbbbb; ")

        self.label12 = Label.create(
            parent=self.widget1, text=self.shortcut_content[config_js['key_press_programme']][3],
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter, StyleSheet="font-size: 30px; color: #bbbbbb; font-weight: bold; ")

        layout5 = Layout.create(name='QHBoxLayout', children=[self.label7, self.label12])

        self.line5 = QFrame(self)
        self.line5.setFrameShape(QFrame.HLine)
        self.line5.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label8 = Label.create(parent=self.widget1, text="循环播放", StyleSheet="font-size: 30px; color: #bbbbbb; ")

        self.label13 = Label.create(
            parent=self.widget1, text=self.shortcut_content[config_js['key_press_programme']][4], 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter, StyleSheet="font-size: 30px; color: #bbbbbb; font-weight: bold; ")

        layout6 = Layout.create(name='QHBoxLayout', children=[self.label8, self.label13])


        self.widget1_layout = Layout.create(
            name='QVBoxLayout', parent=self.widget1, 
            children=[layout1, self.line1, layout2, self.line2, layout3, self.line3, layout4, self.line4,
                    layout5, self.line5, layout6])

        if config_js['key_press_programme'] == '0':
            self.showKeyPressProgramme()

        # widget2布局
        action_list =['next_play', 'previous_play', 'music_pause', 'random_play', 'single_cycle_play']
        for i in range(len(action_list)):
            Editer = ShortcutEditer(
                f'Editer{i + 1}', 
                text= config_js['custom_shortcut_keys'][action_list[i]],
                saveLocation = ['custom_shortcut_keys', action_list[i]],
                group_list = self.shortcutEditer_group)
            self.shortcutEditer_group.append(Editer)

        self.line10 = QFrame(self)
        self.line10.setFrameShape(QFrame.HLine)
        self.line10.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.checkbox = QCheckBox('使用该方案', self.widget2)
        self.checkbox.setStyleSheet("font-weight: bold; ")
        self.checkbox.stateChanged.connect(self.checkboxStateChanged)
        self.checkbox.setFocusPolicy(Qt.NoFocus)# 禁用键盘焦点
        

        self.label14 = Label.create(
            parent=self.widget2, text="播放下一首", Alignment=Qt.AlignVCenter,
            StyleSheet="font-size: 30px; color: #000000; min-height: 55px; ")
        
        layout7 = Layout.create(name='QHBoxLayout', children=[self.label14, self.shortcutEditer_group[0]])
        # 分隔线
        line6 = QFrame(self)
        line6.setFrameShape(QFrame.HLine)
        line6.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label15 = Label.create(
            parent=self.widget2, text="播放上一首", Alignment=Qt.AlignVCenter,
            StyleSheet="font-size: 30px; color: #000000; min-height: 55px; ")
        
        layout8 = Layout.create(name='QHBoxLayout', children=[self.label15, self.shortcutEditer_group[1]])

        # 分隔线
        line7 = QFrame(self)
        line7.setFrameShape(QFrame.HLine)
        line7.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label16 = Label.create(
            parent=self.widget2, text="开始/暂停播放", Alignment=Qt.AlignVCenter,
            StyleSheet="font-size: 30px; color: #000000; min-height: 55px; ")

        layout9 = Layout.create(name='QHBoxLayout', children=[self.label16, self.shortcutEditer_group[2]])

        # 分隔线
        line8 = QFrame(self)
        line8.setFrameShape(QFrame.HLine)
        line8.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label17 = Label.create(
            parent=self.widget2, text="随机播放", Alignment=Qt.AlignVCenter,
            StyleSheet="font-size: 30px; color: #000000; min-height: 55px;")

        layout10 = Layout.create(name='QHBoxLayout', children=[self.label17, self.shortcutEditer_group[3]])

        # 分隔线
        line9 = QFrame(self)
        line9.setFrameShape(QFrame.HLine)
        line9.setStyleSheet("QFrame { color: #f0f0f0; }")

        self.label18 = Label.create(
            parent=self.widget2, text="循环播放", Alignment=Qt.AlignVCenter,
            StyleSheet="font-size: 30px; color: #000000; min-height: 55px; ")

        layout11 = Layout.create(name='QHBoxLayout', children=[self.label18, self.shortcutEditer_group[4]])

        widget2_layout = Layout.create(
            name='QVBoxLayout', parent=self.widget2, children=[self.checkbox, self.line10, layout7, line6, layout8, line7, layout9, line8, 
            layout10, line9, layout11])
        
        # 设置复选框的初始状态
        if config_js['use_custom_shortcut_keys']:
            self.checkbox.setChecked(True)
        else:
            self.customShortcutOptionalNeutrals()   
        # 将中心组件设置为滚动内容
        self.setWidget(central_widget)

    def eventFilter(self, obj, event):
        """事件过滤器"""
        if isinstance(obj, QComboBox) and event.type() == QEvent.Wheel:
            # 捕获滚轮事件并忽略
            return True
        # 其他事件正常继承
        return super().eventFilter(obj, event)
    
    def comboBoxIndexChanged(self, index) -> None:
        """处理下拉框选择变化事件"""
        combo_box = self.widget1.sender()  # 获取发射信号的对象
        selected_item = combo_box.currentText()# 获取选定选项的文本内容
        config_js['key_press_programme'] = f'{self.items.index(selected_item)}'# 将方案对应的序号保存到配置文件
        # 设置用于展示方案组件的可见性
        if selected_item != self.items[0]:
            self.showKeyPressProgramme(visible=True)
            self.checkbox.setChecked(False) 
        else:
            self.showKeyPressProgramme()

    def showKeyPressProgramme(self, programme_index = config_js['key_press_programme'], visible = False) -> None:
        """展示当前所选择的方案内容"""
        # 切换可见性
        self.line1.setVisible(visible)
        self.label4.setVisible(visible)
        self.line2.setVisible(visible)
        self.label5.setVisible(visible)
        self.line3.setVisible(visible)
        self.label6.setVisible(visible)
        self.line4.setVisible(visible)
        self.label7.setVisible(visible)
        self.line5.setVisible(visible)
        self.label8.setVisible(visible)
        self.label9.setVisible(visible)
        self.label10.setVisible(visible)
        self.label11.setVisible(visible)
        self.label12.setVisible(visible)
        self.label13.setVisible(visible)
        # 更换对应方案的文本显示
        if visible:
            self.label9.setText(self.shortcut_content[config_js['key_press_programme']][0])
            self.label10.setText(self.shortcut_content[config_js['key_press_programme']][1])
            self.label11.setText(self.shortcut_content[config_js['key_press_programme']][2])
            self.label12.setText(self.shortcut_content[config_js['key_press_programme']][3])
            self.label13.setText(self.shortcut_content[config_js['key_press_programme']][4])

    def checkboxStateChanged(self, state) -> None:
        """处理复选框状态变化事件"""
        sender = self.sender()  # 获取发射信号的对象
        if state == 2:  # 2 表示复选框被选中
            # 将内置方案置于不使用项
            self.combobox.setCurrentText(self.items[0])
            # 内置方案展示设为不可见
            self.showKeyPressProgramme()
            # 切换方案序号保存到配置文件
            config_js['key_press_programme'] = '0'
            config_js['use_custom_shortcut_keys'] = True
            self.customShortcutOptionalNeutrals(True) # 可选中
        else:
            config_js['use_custom_shortcut_keys'] = False
            self.customShortcutOptionalNeutrals() # 不可选中
    
    def customShortcutOptionalNeutrals(self, isOptional = False) -> None:
        """自定义快捷键界面组件的可选中性"""
        true_style = "font-size: 30px; color: #000000; min-height: 55px;"
        false_style = "font-size: 30px; color: gray; min-height: 55px;"
        # 可选中时的属性
        if isOptional:
            self.widget2_optional_neutral = True
            self.label14.setStyleSheet(true_style)
            self.label15.setStyleSheet(true_style)
            self.label16.setStyleSheet(true_style)
            self.label17.setStyleSheet(true_style)
            self.label18.setStyleSheet(true_style)
            for shortcutEditer in self.shortcutEditer_group:
                shortcutEditer.setFocusPolicy(Qt.ClickFocus)
                shortcutEditer.installEventFilter(shortcutEditer) # 恢复事件过滤器
                shortcutEditer.setStyleSheet(""" QWidget{ min-height: 50px;background-color: white; font-size: 36px; color: black; }""")
        # 不可选中时的属性
        else:
            self.widget2_optional_neutral = False
            self.label14.setStyleSheet(false_style)
            self.label15.setStyleSheet(false_style)
            self.label16.setStyleSheet(false_style)
            self.label17.setStyleSheet(false_style)
            self.label18.setStyleSheet(false_style)
            for shortcutEditer in self.shortcutEditer_group:
                shortcutEditer.setFocusPolicy(Qt.NoFocus)
                shortcutEditer.removeEventFilter(shortcutEditer) # 清除事件过滤器
                shortcutEditer.setStyleSheet("""QWidget{ min-height: 50px; background-color: white; font-size: 36px; color: gray; }""")
                


    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if self.widget2_optional_neutral:
            # 获取鼠标事件的位置
            pos = event.pos()
            # 找到该位置的子部件
            child_widget = self.childAt(pos)
            # 检查列表
            check_list = []
            # 当点击父组件的非shortcutEditer部分时，也还原其样式为默认样式
            for shortcutEditer in self.shortcutEditer_group:
                children = shortcutEditer.findChildren(QLabel)
                check_list.extend(children)
            # 鼠标点击发生在shortcutEditer组件范围之外,恢复其样式为默认样式
            if child_widget not in self.shortcutEditer_group and child_widget not in check_list:
                for shortcutEditer in self.shortcutEditer_group:
                    shortcutEditer.setStyleSheet(DEFAULT_STYLE)
                

class PageConfigFiles(QScrollArea):
    """ 配置文件打开页面 """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: transparent; }")
        self.setWidgetResizable(True) # 组件可调整大小属性
        self.construct()
        

    def construct(self) -> None:
        """ 页面UI搭建 """
        # 主布局
        # 中心组件
        central_widget = QGroupBox(None, self)
        central_widget.setStyleSheet("QGroupBox { border: transparent; background-color: #f0f0f0; }")
        central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))# 设置中心组件拉伸限制

         # 中心组件布局
        main_layout = Layout.create(name='QVBoxLayout', parent=self, children=[central_widget])
       
        label1 = Label.create(
            parent=central_widget, text="设置文件", StyleSheet="font-size: 40px; font-weight: bold;")

        widget1 = QWidget(central_widget)
        widget1.setObjectName("QWidget_1")
        widget1.setStyleSheet("#QWidget_1 { background-color: #fdfdfd; border: 1px solid #e5e5e5; }")

        label2 = Label.create(
            parent=central_widget, text="样式文件", StyleSheet="font-size: 40px; font-weight: bold;")

        widget2 = QWidget(central_widget)
        widget2.setObjectName("QWidget_1")
        widget2.setStyleSheet("#QWidget_1 { background-color: #fdfdfd; border: 1px solid #e5e5e5; }")

        central_widget_layout =  Layout.create(
            name='QVBoxLayout', parent=central_widget, children=[label1, widget1, label2, widget2])
        
        # widget1布局
        label3 = Label.create(
            parent=widget1, text="PlayerConfig.json", 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter,
            StyleSheet="font-size: 30px;")

        button1 = PushButton.create(
            parent=widget1, text="打开文件", 
            clicked_callback=lambda: self.open_selected_file(r'profiles\PlayerConfig.json'),
            StyleSheet="font-size: 30px;"
        )
        button1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        layout1 = Layout.create(name='QHBoxLayout', children=[label3, button1])

        # 分隔线
        line1 = QFrame(self)
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("QFrame { color: #f0f0f0; }")

        label4 = Label.create(
            parent=widget1, text="PlayerStyle.json", 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter,
            StyleSheet="font-size: 30px;"
        )
        
        button2 = PushButton.create(
            parent=widget1, text="打开文件",
            clicked_callback=lambda: self.open_selected_file(r'profiles\PlayerStyle.json'),
            StyleSheet="font-size: 30px;"
        )
        button2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        layout2 = Layout.create(name='QHBoxLayout', children=[label4, button2])
        widget1_layout = Layout.create(name='QVBoxLayout', parent=widget1, children=[layout1, line1, layout2])
        
        # widget2布局
        label5 = Label.create(
            parent=widget2, text="PlayerStyle.css", 
            Alignment=Qt.AlignHCenter | Qt.AlignVCenter,
            StyleSheet="font-size: 30px;"
        )

        button3 = PushButton.create(
            parent=widget2, text="打开文件",
            clicked_callback=lambda: self.open_selected_file(r'profiles\PlayerStyle.css'),
            StyleSheet="font-size: 30px;"
        )
        button3.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        layout3 = Layout.create(name='QHBoxLayout', children=[label5, button3])

        widget2_layout = Layout.create(name='QVBoxLayout', parent=widget2, children=[layout3])
        # 将中心组件设置为滚动内容
        self.setWidget(central_widget)

    def open_selected_file(self, file_path) -> None:
        """ 打开文件操作 """
        try:
            # 使用系统默认程序打开文件
            os.startfile(file_path)
        except FileNotFoundError:
            QMessageBox.critical(self, 'FileNotFoundError', '文件不存在,请检查文件位置', QMessageBox.Ok)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageSongList()
    window.show()
    sys.exit(app.exec_())

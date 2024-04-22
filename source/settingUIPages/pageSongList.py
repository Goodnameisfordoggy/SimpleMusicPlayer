'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-04-20 23:08:59
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\settingUIPages\pageSongList.py
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
import sys
import time
import typing
import threading
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QGroupBox, QFileDialog, QMessageBox, QSizePolicy, QComboBox, QListWidget, 
    QSpacerItem)
from ..Simple_Qt import Label, PushButton, Layout
from .InputWindow import InputWindow
from ..DataProtector import config_js, load_playlist
from ..method import getPath, existSecondLevelDirectory, restartQuery


class PageSongList(QScrollArea):

    def __init__(self, parent: QWidget | None = None, app = None) -> None:
            super().__init__(parent)
            self.app = app
            self.setStyleSheet("QScrollArea { border: transparent; }")
            self.setWidgetResizable(True) # 组件可调整大小属性
            self.fst_items_name = [sub_list[0] for sub_list in config_js['playlist'] if isinstance(sub_list[0], str)]
            self.current_sec_items_name = []
            self.selected_subitem_AP = None # 选中项的绝对路径
            self.construct()


    def construct(self) -> None:
        """ 页面UI搭建 """
        # 主布局
        # 中心组件
        self.central_widget = QGroupBox(None, self)
        self.central_widget.setStyleSheet("QGroupBox { border: none; }")
        # self.central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))# 设置中心组件拉伸限制
        
        main_layout = Layout.create(name="QVBoxLayout", parent=self, children=[self.central_widget])

        # 中心组件布局
        widget1 = QGroupBox(self.central_widget)
        widget1.setStyleSheet("QGroupBox { background-color: #fdfdfd; }")
        
        widget2 = QGroupBox(self.central_widget)
        widget2.setStyleSheet("QGroupBox { background-color: #fdfdfd; }")

        widget3 = QWidget(self.central_widget)

        central_widget_layout = Layout.create(
            name="QVBoxLayout", parent=self.central_widget, 
            children=[widget1, widget2, widget3])
        
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

        button1 = PushButton.create(parent=self, text="创建新分组", clicked_callback=self.wait_for_input_group_name)
        layout1 = Layout.create(name='QHBoxLayout', children=[(self.comboBox1, 3), (button1, 1)])

        self.comboBox2 = QComboBox()
        for fst_items in config_js['playlist']:
            if fst_items[0] == config_js['current_songlist_group']:
                self.current_sec_items_name = [sub_list[0] for sub_list in fst_items if isinstance(sub_list, list)]
        self.comboBox2.addItems(self.current_sec_items_name)
        self.comboBox2.currentIndexChanged.connect(self.comboBoxIndexChanged2)
        self.comboBox2.installEventFilter(self)

        button2 = PushButton.create(parent=self, text="创建新歌单", clicked_callback=self.wait_for_input_songlist_name)

        layout2 = Layout.create(name='QHBoxLayout', children=[(self.comboBox2, 3), (button2, 1)])
        
        self.comboBox1.setCurrentText(config_js['current_songlist_group']) # 设置下拉列表1的初始状态
        self.comboBox2.setCurrentText(os.path.basename(config_js['current_songlist_path'])) # 设置下拉列表2的初始状态
        
        widget1_layout = Layout.create(
            name="QVBoxLayout", parent=widget1, 
            children=[label1, layout1, label2, layout2])
        
        # widget2布局
        button3 = PushButton.create(
            parent=widget2, text="移动到其他歌单", clicked_callback=self.move_to_other_songlist)
        button4 = PushButton.create(
            parent=widget2, text="复制到其他歌单", clicked_callback=self.copy_to_other_songlist)
        button5 = PushButton.create(
            parent=widget2, text="从当前歌单移除", clicked_callback=self.removed_from_the_current_songlist)

        layout3 = Layout.create(name='QHBoxLayout', children=[button3, button4, button5])

        self.listWidget = QListWidget(widget2)
        self.listWidget.setStyleSheet(" QListWidget { min-height: 350px; border: none; } ")
        self.listWidget.addItems(self.get_all_audio_files_in_folder(config_js['current_songlist_path']))
        self.listWidget.itemClicked.connect(self.on_item_clicked)

        widget2_layout = Layout.create(name="QVBoxLayout", parent=widget2, children=[layout3, self.listWidget])

        # widget3布局
        spacer = Label.create(parent=widget3, text='')
        
        self.partial_initial_button = PushButton.create(
            parent=self.central_widget, text="初始化播放列表", 
            clicked_callback=self.partial_init,
            StyleSheet=
            """
            QPushButton {
            color: #ffffff;
            font-size: 30px;
            background-color: #f66c6c;
            border-radius: 5px; 
            min-height: 45px;
            max-width: 230px;
            }
            QPushButton:hover {
                background-color: #f78888; 
            }
            """)
        
        widget3_layout = Layout.create(name="QHBoxLayout", parent=widget3, children=[spacer, self.partial_initial_button])

        # 将中心组件设置为滚动内容
        self.setWidget(self.central_widget)

    
    def wait_for_input_group_name(self) -> None:
        """创建一个窗口用来获取用户输入"""
        self.group_name_inputWindow = InputNewGroupNameWindow(title='请输入新的分组名', text='不能全为数字', button_text='创建')
        self.group_name_inputWindow._show()
        # 启用新线程等待用户输入
        self.thread_create_a_new_group = threading.Thread(target=self.create_a_new_group, daemon=True, name='to_create_a_new_group')
        self.thread_create_a_new_group.start()

    def create_a_new_group(self) -> None:
        """创建新的歌单组"""
        # 获取配置文件中旧的分组
        existing_groups = [group[0]for group in config_js['playlist']]
        while True:
            user_input = self.group_name_inputWindow.user_input
            if self.group_name_inputWindow.is_close:
                # 输入窗口关闭
                # print("窗口关闭")
                break
            elif user_input:
                if user_input in existing_groups:
                    # print("分组名已存在")
                    break
                # 生成新分组目录绝对路径
                new_folder_AP = os.path.join(os.path.dirname(os.path.dirname(config_js['current_songlist_path'])), user_input)
                if os.path.exists(new_folder_AP): 
                    # print("目录已存在")
                    break
                else:
                    # 在配置文件的结构中添加新的分组项
                    new_group_item = [f'{user_input}']
                    config_js['playlist'].append(new_group_item)
                    # 在分组父级目录中创建新目录
                    os.makedirs(new_folder_AP)
                    # print("创建成功")
                    break   
            else:
                time.sleep(0.2)
                # print("pass")
                pass
    
    def wait_for_input_songlist_name(self) -> None:
        """创建一个窗口用来获取用户输入"""
        self.songlist_name_inputWindow = InputNewSonglistNameWindow(title='请输入新的歌单名', text='不能全为数字', button_text='创建')
        self.songlist_name_inputWindow._show()
        # 启用新线程等待用户输入
        self.thread_create_a_new_songlist = threading.Thread(target=self.create_a_new_songlist, daemon=True, name='to_create_a_new_songlist')
        self.thread_create_a_new_songlist.start()

    def create_a_new_songlist(self) -> None:
        """创建新的歌单"""
        # 获取配置文件中旧的分组, 获取当前分组在存储结构中的索引
        existing_groups = [group[0]for group in config_js['playlist']]
        index = existing_groups.index(config_js['current_songlist_group'])
        existing_songlists = [songlist[0] for songlist in config_js['playlist'][index][1:]]
        
        while True:
            user_input = self.songlist_name_inputWindow.user_input
            if self.songlist_name_inputWindow.is_close:
                # 输入窗口关闭
                # print("窗口关闭")
                break
            elif user_input:
                if user_input in existing_groups:
                    # print("歌单名已存在")
                    break
                # 获取主目录路径
                primary_folder_path = ''
                if config_js['current_songlist_path']:
                    primary_folder_path = os.path.dirname(os.path.dirname(config_js['current_songlist_path']))
                elif config_js['foregoing_songlist_path']:
                    primary_folder_path = os.path.dirname(os.path.dirname(config_js['foregoing_songlist_path']))
                if not primary_folder_path:
                    print("主目录路径获取失败!")
                    break
                # 生成新歌单目录绝对路径
                new_folder_AP = f'{primary_folder_path}\\{config_js['current_songlist_group']}\\{user_input}'
                if os.path.exists(new_folder_AP): 
                    # print("目录已存在")
                    break
                else:       
                    # 在配置文件的结构中添加新的歌单项
                    new_songlist_item = [f'{user_input}'] + [new_folder_AP]
                    for group in config_js['playlist']:
                        if group[0] == config_js['current_songlist_group']:
                            group.append(new_songlist_item)
                            break
                    # 在当前分组中创建新歌单目录
                    os.makedirs(new_folder_AP)
                    # print("创建成功")
                    break   
            else:
                time.sleep(0.2)
                # print("pass")
                pass
        
    def on_item_clicked(self, item) -> None:
        file_name = item.text()
        self.selected_subitem_AP = os.path.join(config_js['current_songlist_path'], file_name) # 获取选中子项对应文件的绝对路径
        
    def move_to_other_songlist(self) -> None:
        """移动到其他目录"""
        if self.selected_subitem_AP:
            # 检测选中的子项对应的文件是否存在
            if os.path.exists(self.selected_subitem_AP):
                object_file_name = os.path.basename(self.selected_subitem_AP)  # 目标文件名
                # 获取用户所选目录绝对路径
                folder_path = getPath.get_folder_path(text = '选择目标歌单', initial_position = os.path.dirname(config_js['current_songlist_path']))
                if folder_path:
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

    def copy_to_other_songlist(self) -> None:
        """复制到其他目录"""
        if self.selected_subitem_AP:
            # 检测选中的子项对应的文件是否存在
            if os.path.exists(self.selected_subitem_AP):
                object_file_name = os.path.basename(self.selected_subitem_AP)  # 目标文件名
                # 获取用户所选目录绝对路径
                folder_path = getPath.get_folder_path(text = '选择目标歌单', initial_position = os.path.dirname(config_js['current_songlist_path']))
                if folder_path:
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
            
    def removed_from_the_current_songlist(self) ->None:
        """从当前文件夹删除目标文件, 并添加到"最近删除"目录"""
        if self.selected_subitem_AP:
            song_library_path = os.path.dirname(config_js['current_songlist_path']) # 获取曲库路径
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
                    if file_extension.lower() in config_js['audio_file_suffixes']: # 检查文件的小写拓展名是否符合要求
                        audio_files.append(file_name)

        return audio_files

    def comboBoxIndexChanged1(self, index) -> None:
        """处理下拉列表选择变化事件1"""
        combo_box = self.central_widget.sender()  # 获取发射信号的对象
        selected_item = combo_box.currentText()# 获取选定选项的文本内容
        config_js['current_songlist_group'] = selected_item
        for fst_item_name in self.fst_items_name:
            # 在歌单分组名中查找选中项文本
            if fst_item_name == selected_item:
                self.comboBox2.clear()
                # 根据匹配的歌单分组名在歌单分组名列表中的索引,获取该歌单分组下的全部歌单名称
                sec_items = [sub_folder[0] for sub_folder in config_js['playlist'][self.fst_items_name.index(fst_item_name)][1:]]
                self.comboBox2.addItems(sec_items)
    
    def comboBoxIndexChanged2(self, index) -> None:
        """ 处理下拉列表选择变化事件2 """
        combo_box = self.central_widget.sender()  # 获取发射信号的对象
        selected_item = combo_box.currentText()# 获取选定选项的文本内容
        # 获取当前歌单组在playlist中的索引
        for fst_item_name in self.fst_items_name:
            if fst_item_name == config_js['current_songlist_group']:
                fst_index = self.fst_items_name.index(fst_item_name)
        # 逐个获取当前歌单组下的歌单的路径
        for sec_item_path in [sub_folder[1] for sub_folder in config_js['playlist'][fst_index][1:]]:
            # 找到下拉列表所选择的歌单名称, 将其对应的路径赋给app属性
            if os.path.basename(sec_item_path) == selected_item:
                self.app.current_songlist_path = sec_item_path
                self.app.update_song_list()
                if hasattr(self, 'listWidget'):
                    self.listWidget.clear()
                    self.listWidget.addItems(self.get_all_audio_files_in_folder(sec_item_path))
    
    def partial_init(self) -> None:
        """
        局部初始化:
        初始化播放列表
        """
        # 获取用户选择的目录路径
        folder_path = getPath.get_folder_path(caption="选择播放列表")
        if folder_path:
            if existSecondLevelDirectory.exist_second_level_directory(folder_path):
                config_js['playlist_path'] = folder_path
                config_js['playlist'] = load_playlist(folder_path)
                restartQuery.restart_query(self)
            else:
                QMessageBox.warning(self, 'warning', '存储结构不符合条件!', QMessageBox.Ok)
   
    @typing.override
    def eventFilter(self, obj, event):
        """
        事件过滤器:
        忽略下拉列表框(QComboBox)的鼠标滚轮事件.
        """
        if isinstance(obj, QComboBox) and event.type() == QEvent.Wheel:
            # 捕获滚轮事件并忽略
            return True
        # 其他事件正常继承
        return super().eventFilter(obj, event)
    

class InputNewGroupNameWindow(InputWindow):
    """新的分组名称输入窗口"""
    
    def __init__(self, title: str = 'InputWindow', text: str = '请输入内容：', button_text: str = '确定') -> None:
        super().__init__(title, text, button_text)
    
    @typing.override
    @property
    def user_input(self):
        return self._user_input
    
    @user_input.setter
    def user_input(self, value) -> None:
        if not value.isdigit():
            self._user_input = value
        else:
            QMessageBox.warning(self, 'warning', '分组名不建议全为数字!')

    @typing.override
    def get_input(self) -> None:
        self.user_input = self.input_text.text()
        time.sleep(0.3)
        self.close()
    
    
class InputNewSonglistNameWindow(InputWindow):
    """新的分组名称输入窗口"""
    
    def __init__(self, title: str = 'InputWindow', text: str = '请输入内容：', button_text: str = '确定') -> None:
        super().__init__(title, text, button_text)

    @typing.override
    @property
    def user_input(self):
        return self._user_input
    
    @user_input.setter
    def user_input(self, value) -> None:
        if not value.isdigit():
            self._user_input = value
        else:
            QMessageBox.warning(self, 'warning', '歌单名不建议全为数字!')

    @typing.override
    def get_input(self) -> None:
        self.user_input = self.input_text.text()
        time.sleep(0.3)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageSongList()
    window.show()
    sys.exit(app.exec_())

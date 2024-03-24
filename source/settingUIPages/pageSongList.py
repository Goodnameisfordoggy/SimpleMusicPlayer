'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-03-24 01:09:28
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
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import os
import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QGroupBox, QFileDialog, QMessageBox, QSizePolicy, QComboBox, QListWidget)
from Simple_Qt import Label, PushButton, Layout
from DataProtector import config_js


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
    

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageSongList()
    window.show()
    sys.exit(app.exec_())

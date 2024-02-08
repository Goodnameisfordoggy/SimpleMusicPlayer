'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-02-06 19:08:50
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\SettingUI.py
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
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QWidget, QHBoxLayout, QMainWindow, QVBoxLayout, QStackedLayout
from Simple_Qt import PushButton, Menu, Action
from DataProtector import style_css
from SettingPages import PageSongList, PageImageSetting, PageShortcutSetting, PageConfigFiles

default_button_style = """
    QPushButton { 
        min-height: 60px;      
        text-align: left; 
        font-weight: bold; 
        font-size: 33px; 
        font-family: KaiTi;
        background-color: white;
        border: 2px solid rgb(232, 232, 232);
    }QPushButton:hover {
        min-height: 60px;   
        font-size: 50px; 
        background-color: #eff6ff;
    }
    """
checked_button_style="""
    QPushButton { 
        min-height: 60px;      
        text-align: left; 
        font-weight: bold; 
        font-size: 50px; 
        font-family: KaiTi;
        color: #3388ff;
        background-color: #eff6ff;
        border: 2px solid #3388ff;
    }
    """
class SettingUI(QMainWindow):
    """ 一级菜单--设置 """

    def __init__(self, width=1000, height=650, app = None) -> None:
        super().__init__()
        # 应用程序对象传入
        self.app = app
        # UI设置
        self.setWindowTitle("SettingUI")
        self.resize(width, height)
        # 底层变量
        self.menu_setting = None  # 一级菜单对象
        self.current_index = 0 # 当前页数
        # 方法绑定
        self.InitUI()
        self.build_menu()
        
        
    def build_menu(self) -> None:
        """ 菜单搭建,连接到主窗口"""
        # 创建一级菜单
        self.menu_setting = Menu.create(
            parent=self.app,
            title='⚙️',
            ObjectName='menu--1',
            StyleSheet=style_css,
            superior=self.app.menubar
        )

        action_open_settingUI = Action.create(
            parent=self.app, text="设置", 
            triggered_callback= lambda: self.exec_rewrite(),
            superior=self.menu_setting
        )

    def exec_rewrite(self) -> None:
        """ 自定义的窗口呼出方法 """
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.show()
  
    def InitUI(self) -> None:
        """ UI搭建 """
        # 创建并设置主窗口中央的部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建并设置中央组件的布局
        main_layout = QHBoxLayout(central_widget)        
        
        left_layout = QVBoxLayout()
        self.right_layout = QStackedLayout()
        main_layout.addLayout(left_layout, stretch = 0)
        main_layout.addLayout(self.right_layout, stretch = 1)

        # 左侧列表框
        self.button_list_widget = QListWidget(self)
        self.button_list_widget.setStyleSheet("border: 2px solid transparent; background-color: #f0f0f0")
        left_layout.addWidget(self.button_list_widget)

        # 按钮选项
        button_name_list = ["歌单", "背景图", "快捷键", "配置文件"]
        self.button_group = [] # 按钮组,用于存放按钮实例
        for index, name in enumerate(button_name_list): # 页面顺序与button_name_list内容一致
            button = PushButton.create(
                parent=self.button_list_widget, text=" " + name,
                clicked_callback=[self.button_clicked_callback, index],
                # ObjectName="Button",
                StyleSheet=default_button_style
            )
            self.button_group.append(button)
            item = QListWidgetItem(self.button_list_widget)
            item.setSizeHint(button.sizeHint())  # 将项目大小设置为按钮大小
            self.button_list_widget.setItemWidget(item, button)  # 将按钮关联到项目上

        # 初始化第一个按钮处于选中状态
        self.button_group[0].setStyleSheet(checked_button_style)

        # 右侧堆叠子页
        page_SongList = PageSongList(self)
        self.right_layout.addWidget(page_SongList)
        page_ImageSetting = PageImageSetting(self)
        self.right_layout.addWidget(page_ImageSetting)
        page_ShortcutSetting = PageShortcutSetting(self)
        self.right_layout.addWidget(page_ShortcutSetting)
        page_ConfigFiles = PageConfigFiles(self)
        self.right_layout.addWidget(page_ConfigFiles)

    
    def button_clicked_callback(self, index):
        # 将当前已选中的按钮样式恢复
        self.button_group[self.current_index].setStyleSheet(default_button_style)
        # 储存当前选中的按钮索引
        self.current_index = index
        # 将当前选中的按钮样式改变为选中状态
        self.button_group[index].setStyleSheet(checked_button_style)
        # 堆叠布局换页
        self.right_layout.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = SettingUI()
    window.show()
    sys.exit(app.exec_())

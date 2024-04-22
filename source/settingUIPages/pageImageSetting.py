'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-04-20 23:09:34
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\settingUIPages\pageImageSetting.py
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
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QGroupBox, QLineEdit, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtGui import QPixmap
from ..Simple_Qt import Label, PushButton, Layout
from ..DataProtector import config_js, DataInitializationMethod
from ..method import restartQuery, getPath


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
        self.central_widget = QGroupBox(None, self)
        self.central_widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))# 设置中心组件拉伸限制
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet("QGroupBox#central_widget { border: transparent; }")

        main_layout = Layout.create(name='QVBoxLayout', parent=self, children=[self.central_widget])
        # 中心组件布局
        widget1 = QGroupBox(None, self)
        widget1.setStyleSheet("QGroupBox { background-color: #fdfdfd; }")
        
        widget2 = QWidget(self.central_widget)

        central_widget_layout = Layout.create(
            name='QVBoxLayout', parent=self.central_widget, 
            children=[widget1, widget2]
        )

        # widget1
        # 容器1
        group_box_1 = QGroupBox("主窗口", widget1)
        group_box_1.setStyleSheet("QGroupBox { color: gray; }")
        # 分隔线
        line1 = QFrame(self)
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("QFrame { color: #f0f0f0; }")
        # 容器2
        group_box_2 = QGroupBox("歌曲搜素窗口", widget1)
        group_box_2.setStyleSheet("QGroupBox { color: gray; }")
        # 空白项
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        
        widget1_layout = Layout.create(
            name='QVBoxLayout', parent=widget1, 
            children=[group_box_1, line1, group_box_2, spacer_item]
        )

        
        # 容器1布局
        # 1-1
        label1 = Label.create(parent=group_box_1, text="背景图片: ", StyleSheet="font-size: 30px;")

        self.label_pixmap1 = Label.create(parent=group_box_1, Pixmap=QPixmap(config_js['ApplicationWindowBackGround']).scaledToWidth(120))

        lineEdit1 = QLineEdit(group_box_1)
        lineEdit1.setPlaceholderText(config_js['ApplicationWindowBackGround'])

        button1 = PushButton.create(
            parent=group_box_1, text="更改图片",
            clicked_callback=lambda: self.select_a_file('ApplicationWindowBackGround'),
            StyleSheet="font-size: 30px;"
        )

        layout1 = Layout.create(name='QHBoxLayout', children=[lineEdit1, button1])   
        # 1-2
        label2 = Label.create(parent=group_box_1, text="窗口图标: ", StyleSheet="font-size: 30px;")
        
        self.label_pixmap2 = Label.create(parent=group_box_1, Pixmap=QPixmap(config_js['ApplicationWindowIcon']).scaledToWidth(80))
       
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
            children=[label1, self.label_pixmap1, layout1, label2, self.label_pixmap2, layout2]
        )

        # 容器2布局
        # 2-1
        label3 = Label.create(parent=group_box_2, text="背景图片: ", StyleSheet="font-size: 30px;")

        self.label_pixmap3 = Label.create(parent=group_box_2, Pixmap=QPixmap(config_js['SearchUIBackGround']).scaledToWidth(120))
        
        lineEdit3 = QLineEdit(group_box_2)
        lineEdit3.setPlaceholderText(config_js['SearchUIBackGround'])

        button3 = PushButton.create(
            parent=group_box_2, text="更改图片",
            clicked_callback=lambda: self.select_a_file('SearchUIBackGround'),
            StyleSheet="font-size: 30px;"
        )

        layout3 = Layout.create(name='QHBoxLayout', children=[lineEdit3, button3])   
        # 2-2
        label4 = Label.create(parent=group_box_2, text="窗口图标: ", StyleSheet="font-size: 30px;")

        self.label_pixmap4 = Label.create(parent=group_box_2, Pixmap=QPixmap(config_js['SearchUIIcon']).scaledToWidth(80))
        
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
            children=[label3, self.label_pixmap3, layout3, label4, self.label_pixmap4, layout4]
        )

        # widget2布局
        spacer = Label.create(parent=widget2, text='')
        
        self.partial_initial_button = PushButton.create(
            parent=widget2, text="恢复默认图片图标", 
            clicked_callback=self.partial_init,
            StyleSheet=
            """
            QPushButton {
            color: #ffffff;
            font-size: 30px;
            background-color: #f66c6c;
            border-radius: 5px; 
            min-height: 45px;
            max-width: 250px;
            }
            QPushButton:hover {
                background-color: #f78888; 
            }
            """)
        
        widget3_layout = Layout.create(name="QHBoxLayout", parent=widget2, children=[spacer, self.partial_initial_button])
        

        # 将中心组件设置为滚动内容
        self.setWidget(self.central_widget)
    
    def update_label_pixmap(self) -> None:
        self.label_pixmap1.setPixmap(QPixmap(config_js['ApplicationWindowBackGround']).scaledToWidth(120))
        self.label_pixmap2.setPixmap(QPixmap(config_js['ApplicationWindowIcon']).scaledToWidth(80))
        self.label_pixmap3.setPixmap(QPixmap(config_js['SearchUIBackGround']).scaledToWidth(120))
        self.label_pixmap4.setPixmap(QPixmap(config_js['SearchUIIcon']).scaledToWidth(80))
    
    def select_a_file(self, config_js_key) -> None:
        file_path = getPath.get_file_path(caption="选择图片文件", filter_type='Image')
        # 更改配置文件中的路径
        if file_path:
            # 将新的图片文件路径储存到配置文件
            config_js[config_js_key] = file_path
            self.update_label_pixmap()
            time.sleep(0.2)
            restartQuery.restart_query(self)
    
    def partial_init(self) -> None:
        """
        局部初始化:
        初始化图片/图标设置,并重启APP
        """
        reply = QMessageBox.question(self, None, "确定恢复默认吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            DataInitializationMethod.initialize_image_and_icon_settings()
            self.update_label_pixmap()
            time.sleep(1) # 重启安全间隔, 确保数据同步
            # 获取当前执行的文件路径
            current_file = sys.argv[0]
            # 重启程序
            os.execv(sys.executable, ['python3', current_file])
            
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageImageSetting()
    window.show()
    sys.exit(app.exec_())

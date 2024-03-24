'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-03-24 00:34:00
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\settingUIPages\pageImageSetting.py
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
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QGroupBox, QLineEdit, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtGui import QPixmap
from Simple_Qt import Label, PushButton, Layout
from DataProtector import config_js


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


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageImageSetting()
    window.show()
    sys.exit(app.exec_())

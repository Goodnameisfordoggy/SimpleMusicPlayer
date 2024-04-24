'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-04-23 22:53:48
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\settingUIPages\pageConfigFiles.py
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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QGroupBox, QMessageBox, QSizePolicy, QFrame)
from ..Simple_Qt import Label, PushButton, Layout
                

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

    def open_selected_file(self, file_RP) -> None:
        """ 
        打开文件操作:

        args:
        file_path_RP: 文件的相对路径
        """
        # 获取当前文件所在目录的父级目录
        parent_directory_AP = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # 项目目录
        project_folder_AP = os.path.dirname(parent_directory_AP)
        # 手动添加路径分隔符
        if not project_folder_AP.endswith(os.sep):
            project_folder_AP += os.sep
        try:
            # 使用系统默认程序打开文件
            os.startfile(os.path.join(project_folder_AP, file_RP))
        except FileNotFoundError:
            QMessageBox.critical(self, 'Music Player', '文件不存在,请检查文件位置', QMessageBox.Ok)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageConfigFiles()
    window.show()
    sys.exit(app.exec_())

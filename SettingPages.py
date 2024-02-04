import os
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QGroupBox, QLineEdit, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtGui import QPixmap
from Simple_Qt import Label, PushButton, Layout
from DataProtector import config_js


class PageImageSetting(QScrollArea):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: transparent; }")
        self.setWidgetResizable(True) # 组件可调整大小属性
        self.construct()
    
    def construct(self):
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
    
    def select_a_file(self, config_js_key):
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


class PageSongList(QScrollArea):

    def construct(self):
        """ 页面UI搭建 """
        pass


class PageShortcutSetting(QScrollArea):

    def construct(self):
        """ 页面UI搭建 """
        pass


class PageConfigFiles(QScrollArea):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: transparent; }")
        self.setWidgetResizable(True) # 组件可调整大小属性
        self.construct()
        

    def construct(self):
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
        widget1.setStyleSheet("#QWidget_1 { background-color: #fdfdfd; }")

        label2 = Label.create(
            parent=central_widget, text="样式文件", StyleSheet="font-size: 40px; font-weight: bold;")

        widget2 = QWidget(central_widget)
        widget2.setObjectName("QWidget_2")
        widget2.setStyleSheet("#QWidget_2 { background-color: #fdfdfd; }")

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
        """ 菜单项的绑定操作,用于打开选中的文件"""
        try:
            # 使用系统默认程序打开文件
            os.startfile(file_path)
        except FileNotFoundError:
            QMessageBox.critical(self.main_window, 'FileNotFoundError', '文件不存在,请检查文件位置', QMessageBox.Ok)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageConfigFiles()
    window.show()
    sys.exit(app.exec_())

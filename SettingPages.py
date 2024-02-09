import os
import sys
import time
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QGroupBox, QLineEdit, QFileDialog, 
QMessageBox, QSpacerItem, QSizePolicy, QFrame, QComboBox, QCheckBox, QLabel)
from PyQt5.QtGui import QPixmap
from Simple_Qt import Label, PushButton, Layout
from DataProtector import config_js
from ShortcutEditer import ShortcutEditer, DEFAULT_STYLE


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


class PageSongList(QScrollArea):

    def construct(self) -> None:
        """ 页面UI搭建 """
        pass


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
        for i in range(5):
            action_list =['next_play', 'previous_play', 'music_pause', 'random_play', 'single_cycle_play']
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
        if config_js['use_custom_shortcut_keys']:
            self.checkbox.setChecked(True)

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
        else:
            config_js['use_custom_shortcut_keys'] = False

    def mousePressEvent(self, event):
        """鼠标点击事件"""
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
            QMessageBox.critical(self.main_window, 'FileNotFoundError', '文件不存在,请检查文件位置', QMessageBox.Ok)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageShortcutSetting()
    window.show()
    sys.exit(app.exec_())

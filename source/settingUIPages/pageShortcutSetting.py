'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-04-10 20:44:18
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\settingUIPages\pageShortcutSetting.py
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
import sys
import typing
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QGroupBox, QSizePolicy, QFrame, QComboBox, QCheckBox, QLabel)
from Simple_Qt import Label, Layout
from DataProtector import config_js
from settingUIPages.ShortcutEditer import ShortcutEditer, DEFAULT_STYLE


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
        action_list =['next_play', 'previous_play', 'pause_or_begin', 'random_play', 'single_cycle_play']
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
                
    @typing.override
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


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 可操作命令行参数
    window = PageShortcutSetting()
    window.show()
    sys.exit(app.exec_())

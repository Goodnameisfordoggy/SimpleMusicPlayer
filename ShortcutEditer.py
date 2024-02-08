'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-02-08 22:32:28
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\ShortcutEditer.py
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
import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeySequence, QPainter, QBrush, QColor
from DataProtector import config_js

with open(r"D:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\profiles\PlayerConfig.json", 'r', encoding='utf-8') as config_json:
    config_js = json.load(config_json)

class ShortcutEditer(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget{ 
                min-height: 50px;
                background-color: white; 
                font-size: 36px; 
            }"""
        )
        
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.label = QLabel('Press a shortcut key...')
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setStyleSheet("QLabel { min-height: 60px; font-size: 36px; }")
        layout.addWidget(self.label)

        self.installEventFilter(self)

        self.setLayout(layout)
        self.setWindowTitle('Shortcut Detection')
        self.setGeometry(300, 300, 300, 200)

    def eventFilter(self, obj, event):

        if event.type() == event.MouseButtonPress:
            print("Mouse button pressed in ShortcutEditer")
            self.setStyleSheet(
                """
                QWidget{ 
                    min-height: 50px;
                    background-color: white; 
                    font-size: 36px; 
                    border: 1px solid #3388ff; 
                    color: #3388ff;
                }"""
            )

        if event.type() == QEvent.KeyPress:
            modifiers = event.modifiers()  # 获取修饰键
            key = event.key()
          
            if modifiers != Qt.NoModifier:
                modifier_str = QKeySequence(modifiers).toString(QKeySequence.PortableText)
            else: 
                modifier_str = ""

            if key not in {Qt.Key_Control, Qt.Key_Shift, Qt.Key_Meta, Qt.Key_Alt}:
                key_str = QKeySequence(key).toString(QKeySequence.PortableText)  
            else:
                key_str = ""
                
            if not key_str:
                # config_js['custom_shortcut_keys']['播放下一首'] = modifier_str.rstrip('+')
                self.label.setText(modifier_str.rstrip('+'))
            else:
                # config_js['custom_shortcut_keys']['播放下一首'] = modifier_str + key_str
                self.label.setText(modifier_str + key_str)

            try:
                 # 打开json文件
                with open(r"profiles\PlayerConfig.json", 'w', encoding='utf-8') as config_json:
                    # json文件写入 ensure_ascii=False禁用Unicode转义确保写入的文件包含原始的非ASCII字符。
                    json.dump(config_js, config_json, ensure_ascii=False, indent=4)
            except NameError:
                print("NameError!: 请检查json文件的位置.")

        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShortcutEditer()
    window.show()
    sys.exit(app.exec_())

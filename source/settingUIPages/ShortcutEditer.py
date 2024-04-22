'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-04-17 21:58:48
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\settingUIPages\ShortcutEditer.py
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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeySequence
from ..DataProtector import config_js

DEFAULT_STYLE = """
    QWidget{ 
        min-height: 50px;
        background-color: white; 
        font-size: 36px; 
}"""
   

CHECKED_STYLE = """
    QWidget{ 
        min-height: 50px;
        background-color: white; 
        font-size: 36px; 
        border: 1px solid #3388ff; 
        color: #3388ff;
}"""
            
     
class ShortcutEditer(QWidget):
    """快捷键识别组件"""
    def __init__(self, name = 'ShortcutEditer', text="", saveLocation = None, group_list = []):
        """
        args: 
        saveLocation: 快捷键的保存位置,将存入str
        group_list: 存放多个ShortcutEditer组件的Group_list
        """
        super().__init__()
        self.name = name
        self.text = text
        self.saveLocation = saveLocation
        self.group_list = group_list
        self.setStyleSheet(DEFAULT_STYLE)
        self.setFocusPolicy(Qt.StrongFocus) # 启用键盘焦点
        self.installEventFilter(self) # 安装事件过滤器拦截自身事件
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.label = QLabel(self.text)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setText(self, text):
        """自定义设置文本内容"""
        self.label.setText(text)

    def eventFilter(self, obj, event):
        """事件过滤器"""
        if event.type() == event.MouseButtonPress:
            if self.group_list:
                # 移除组内所有组件的选中样式
                for shortcutEditer in self.group_list:
                    shortcutEditer.setStyleSheet(DEFAULT_STYLE)
            # 为选中组件添加选中样式
            self.setStyleSheet(CHECKED_STYLE)

        if event.type() == QEvent.KeyPress:
            modifiers = event.modifiers()  # 获取修饰键 Control, Shift, Meta(Win), Alt
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
                self.vrt_save('json', modifier_str.rstrip('+'), config_js, self.saveLocation)
                self.label.setText(modifier_str.rstrip('+'))
            else:
                self.vrt_save('json', modifier_str + key_str, config_js, self.saveLocation)
                self.label.setText(modifier_str + key_str)

    

        return super().eventFilter(obj, event)
    
    def vrt_save(self, toType: str | None = None, data = None, structure=..., location_list = []):
        """
        多功能数据保存方法(variety_save)

        args: 

        toType: 保存的形式                  json
        data; 保存的数据                    类型根据保存形式而变
        structure: 保存结构对象             结构通常是读取文件后常用的数据结构,如json->dict
        location_list: 位置列表             用来描述数据保存的具体位置,如['a', 'b']表示{"a": {"b": xx} }
        """
        if not toType:
            raise ValueError('未选择保存类型!')
        elif not data:
            raise ValueError('保存内容不能为空!')
        elif not location_list:
            raise ValueError('保存位置不能为空!')
        
        if toType == 'json':
            if len(location_list) == 1:
                structure[location_list[0]] = data
            elif len(location_list) == 2:
                structure[location_list[0]][location_list[1]] = data
            elif len(location_list) == 3:
                structure[location_list[0]][location_list[1]][location_list[2]] = data
            elif len(location_list) == 4:
                structure[location_list[0]][location_list[1]][location_list[2]][location_list[3]] = data
            else:
                raise ValueError('位置列表长度超出限制')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShortcutEditer()
    window.show()
    sys.exit(app.exec_())

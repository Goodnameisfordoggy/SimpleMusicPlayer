'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-02-04 18:11:57
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\Simple_Qt.py
Description: 对常用组件的属性,方法的简单集成

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
import typing
import functools
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QDesktopWidget, QMenuBar, QMenu, QAction, QLayout, QFormLayout, 
    QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout, QSpacerItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon


class Label():

    @staticmethod
    def create(
        parent: QWidget | None = ..., 
        text: str = '', 
        WordWrap: bool = False,
        Alignment = Qt.Alignment(), 
        TextInteractionFlags = Qt.NoTextInteraction, 
        Pixmap: QPixmap | None = None,
        ContextMenuPolicy = Qt.NoContextMenu,
        Geometry: tuple[int, int, int, int] = (0, 0, 100, 50), 
        ObjectName: str = '',
        StyleSheet: str = ''
    ):
        """ 
        label方法打包 
        
        Args:
            parent: 父组件
            text: 标签文本内容
            WordWrap: 文本是否自动换行
            Alignment: 对齐方式
            TextInteractionFlags: 文本交互标志
            Pixmap: 像素映射
            ContextMenuPolicy: 文本框的菜单交互
            Geometry: 几何信息(x坐标,y坐标,宽度,高度)
            ObjectName: 对象名称
            StyleSheet: 样式表
        """
        label = QLabel(text=text, parent=parent)
        label.setWordWrap(WordWrap)
        label.setAlignment(Alignment)
        label.setTextInteractionFlags(TextInteractionFlags)
        if Pixmap:
            label.setPixmap(Pixmap)
        label.setContextMenuPolicy(ContextMenuPolicy)
        x, y, width, height = Geometry
        label.setGeometry(x, y, width, height)
        label.setObjectName(ObjectName)
        label.setStyleSheet(StyleSheet)
        return label


class PushButton():

    # @typing.overload
    # def create(clicked_callback: typing.Callable) -> QPushButton:...
    # @typing.overload
    # def create(clicked_callback: [typing.Callable, any]) -> QPushButton:...
    @staticmethod
    def create(
        parent: QWidget | None = ..., 
        text: str = '', 
        clicked_callback: typing.Callable | list[typing.Callable, any] = None,
        setFocusPolicy = Qt.NoFocus, # 默认阻止按钮获得键盘焦点
        Geometry: tuple[int, int, int, int] = (0, 0, 100, 50), 
        ObjectName: str = '',
        StyleSheet: str = '',
    ):
        """ 
        push button方法打包 

        Args:
            parent: 父组件
            parentLayout: 父布局
            text: 按钮文本内容
            clicked_callback: 按钮点击回调函数
            setFocusPolicy: 键盘焦点
            Geometry: 几何信息(x坐标,y坐标,宽度,高度)
            ObjectName: 对象名称
            StyleSheet: 样式表
        """
        push_button = QPushButton(text=text, parent=parent)
        if not clicked_callback:
            pass
        elif isinstance(clicked_callback, typing.Callable):
            push_button.clicked.connect(clicked_callback)
        elif isinstance(clicked_callback, list):
            push_button.clicked.connect(lambda clicked, idx=clicked_callback[1]: clicked_callback[0](idx))
            # push_button.clicked.connect(functools.partial(clicked_callback[0], clicked_callback[1]))
        else:
            raise TypeError("参数类型未设置!")
        
        push_button.setFocusPolicy(setFocusPolicy)
        x, y, width, height = Geometry
        push_button.setGeometry(x, y, width, height)
        push_button.setObjectName(ObjectName)
        push_button.setStyleSheet(StyleSheet)
        return push_button
    

class Menu():

    @staticmethod
    def create(
        parent: QWidget | None = ..., 
        title: str = '', 
        ObjectName: str = '',
        StyleSheet: str = '',
        superior: QMenu | QMenuBar= None
    ):
        """ 
        Menu方法打包 
        
        Args:
            parent: 父组件
            parentLayout: 父布局
            title: 菜单文本内容
            ObjectName: 对象名称
            StyleSheet: 样式表
            superior: 上级菜单/菜单栏
        """ 
        menu = QMenu(title=title, parent=parent)
        menu.setObjectName(ObjectName)
        menu.setStyleSheet(StyleSheet)
        if superior:
            superior.addMenu(menu)
        return menu
    

class Action():

    # @typing.overload
    # def create(triggered_callback: typing.Callable) -> QAction:...
    # @typing.overload
    # def create(triggered_callback: [typing.Callable, any]) -> QAction:...
    @staticmethod
    def create(
        parent: QWidget | None = ..., 
        text: str = '', 
        triggered_callback: typing.Callable | list[typing.Callable | any] = ...,
        Icon_path: str = '',
        superior: QMenu = None
    ):
        """
        action 方法打包

        Args:
            parent: 父组件
            parentLayout: 父布局
            text: 文本内容 
            triggered_callback: 触发函数
            Icon_path: 图标路径
            superior: 上级菜单
        """
        action = QAction(text=text, parent=parent)
        if isinstance(triggered_callback, typing.Callable):
            action.triggered.connect(triggered_callback)
        elif isinstance(triggered_callback, list):
            action.triggered.connect(functools.partial(triggered_callback[0], triggered_callback[1]))
        else:
            raise TypeError("参数类型未设置!")
        action.setIcon(QIcon(Icon_path))
        if superior:
            superior.addAction(action)
        return action
    

class Layout():

    @staticmethod
    def create(
        name: str = '',
        parent: QWidget | None = None,
        children: list[QWidget | QLayout | QSpacerItem] = [],
        ):
        """
        name: 布局名称:选择一个(QFormLayout,QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout)
        parent: 父组件, 将此布局设置为其主布局  QWQ:一个组件只能有一个主布局, 不要将同一个组件传给多个SP_Layout.create()
        children: 子组件/子布局/子项等
        
        布局用法:\n
        widget -> 添加父布局 parent_layout.addWidget(widget)\n
               -> 添加主布局 widget.setLayout(main_layout)/main_layout = QLayout(widget)\n
        layout -> 添加父布局 main_layout.addlayout(layout)\n
               -> 添加子布局 layout.addlayout(chlid_layout)\n
        """
        name_dict = {
            'QLayout': QLayout,
            'QFormLayout': QFormLayout,
            'QGridLayout': QGridLayout,
            'QBoxLayout': QBoxLayout,
            'QHBoxLayout': QHBoxLayout,
            'QVBoxLayout': QVBoxLayout
        }
        if name in name_dict:
            layout = name_dict.get(name, QLayout)(parent)
        if children:
            for child in children:
                if isinstance(child, QWidget):
                    layout.addWidget(child)
                elif isinstance(child, QLayout):
                    layout.addLayout(child)
                elif isinstance(child, QSpacerItem):
                    layout.addSpacerItem(child)
                else:
                    raise TypeError("组件类型错误!")
        return layout
        

        
class PackingModificationMethod(object):
    """ 组件属性的修改方法 """

    @staticmethod
    def set_desktop_center(widget):
        """ 将组件位置相对于桌面居中 """

        # 获取窗口的几何信息
        frame_geometry = widget.frameGeometry()
        # 获取桌面矩形的中心点坐标
        desktop_center = QDesktopWidget().availableGeometry().center()
        # 窗口中心设置为桌面矩形中心
        frame_geometry.moveCenter(desktop_center)
        # 设置窗口的初始位置(左顶点位置)
        widget.move(frame_geometry.topLeft())
    
    @staticmethod
    def set_background_image(widget, image_path):
        """ 
        为窗口设置背景图片 
        
        widget: 组件
        image_path: 图片路径
        """
        pixmap = QPixmap(image_path)
        # 或略图片长宽比,平滑地进行缩放
        scaled_pixmap = pixmap.scaled(widget.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = widget.palette()
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        widget.setPalette(palette)
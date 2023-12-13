import typing
from PyQt5.QtWidgets import QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush

class PackingCreateMethod(object):
    """ 组件创建时的方法 """

    @staticmethod
    def my_label(
        parent = ..., 
        text: str = '', 
        WordWrap: bool = False,
        Alignment = Qt.Alignment(), 
        TextInteractionFlags = Qt.NoTextInteraction, 
        ContextMenuPolicy = Qt.NoContextMenu,
        Geometry: typing.Tuple[int, int, int, int] = (0, 0, 100, 50), 
        ObjectName: str = '',
        StyleSheet: str = ''
        ):
        """ 
        label方法打包 
        
        Args:
            parent: 父对象
            text: 标签文本内容
            WordWrap: 文本是否自动换行
            Alignment: 对齐方式
            TextInteractionFlags: 文本交互
            ContextMenuPolicy: 文本框的菜单交互
            Geometry: 几何信息(x坐标,y坐标,宽度,高度)
            ObjectName: 对象名称
            StyleSheet: 样式表
        """
        label = QLabel(text=text, parent=parent)
        label.setWordWrap(WordWrap)
        label.setAlignment(Alignment)
        label.setTextInteractionFlags(TextInteractionFlags)
        label.setContextMenuPolicy(ContextMenuPolicy)
        x, y, width, height = Geometry
        label.setGeometry(x, y, width, height)
        label.setObjectName(ObjectName)
        label.setStyleSheet(StyleSheet)
        return label

    @staticmethod
    def my_button(
        parent = ..., 
        text: str = '', 
        clicked_callback: typing.Callable = ...,
        setFocusPolicy = Qt.NoFocus, # 默认阻止按钮获得键盘焦点
        Geometry: typing.Tuple[int, int, int, int] = (0, 0, 100, 50), 
        ObjectName: str = 'QPushButton',
        StyleSheet: str = '',
        ):
        """ 
        push button方法打包 
        
        Args:
            parent: 父对象
            text: 按钮文本内容
            clicked_callback: 按钮点击回调函数
            setFocusPolicy: 键盘焦点
            Geometry: 几何信息(x坐标,y坐标,宽度,高度)
            ObjectName: 对象名称
            StyleSheet: 样式表
        """
        push_button = QPushButton(text=text, parent=parent)
        push_button.clicked.connect(clicked_callback)
        push_button.setFocusPolicy(setFocusPolicy)
        x, y, width, height = Geometry
        push_button.setGeometry(x, y, width, height)
        push_button.setObjectName(ObjectName)
        push_button.setStyleSheet(StyleSheet)
        return push_button
    

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
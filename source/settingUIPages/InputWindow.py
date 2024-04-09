import sys
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt


class InputWindow(QDialog):
    
    def __init__(self, title: str = 'InputWindow', text: str = '请输入内容：', button_text: str = '确定'):
        super().__init__()
        self._user_input: str = ''
        self._is_close: bool = False
        self._title = title
        self._text = text
        self._button_text =button_text
        self.initUI()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def initUI(self):
        self.setWindowTitle(self._title)
        self.setFixedSize(500, 150)

        layout = QVBoxLayout()

        self.input_label = QLabel(self._text)
        self.input_text = QLineEdit()
        self.input_text.returnPressed.connect(self.get_input)

        self.submit_button = QPushButton(self._button_text)
        self.submit_button.clicked.connect(self.get_input)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, value):
        self._user_input = value
        

    @user_input.deleter
    def user_input(self):
        del self._user_input
    
    @property
    def is_close(self):
        return self._is_close

    @is_close.setter
    def is_close(self, value):
        self._is_close = value

    @is_close.deleter
    def is_close(self):
        del self._is_close

    @abstractmethod
    def get_input(self):
        raise NotImplementedError("该方法需要被重写!")
    
    def _show(self):
        self.show()
    
    def closeEvent(self, event):
        self.is_close = True
        super().closeEvent(event)


# class InputWindow2(InputWindow):
    
#     def __init__(self, title: str = 'InputWindow', text: str = '请输入内容：', button_text: str = '确定'):
#         super().__init__(title, text, button_text)
    
#     def get_input(self):
#         print('InputWindow2')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InputWindow()
    ex.show()
    # ex2 = InputWindow2('InputWindow2')
    # ex2._show()
    sys.exit(app.exec_())

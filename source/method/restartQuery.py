import os
import sys
from PyQt5.QtWidgets import QMessageBox, QWidget

def restart_query(parent: QWidget) -> None:
	"""应用重启询问"""
	reply = QMessageBox.question(
		parent, 
		'Music Player', '新内容将于下次APP启动时应用,是否立即重启?', 
		QMessageBox.Yes | QMessageBox.No, 
		QMessageBox.No
	)
	if reply == QMessageBox.Yes:
		# 获取当前执行的文件路径
		current_file = sys.argv[0]
		# 重启程序
		os.execv(sys.executable, ['python3', current_file])

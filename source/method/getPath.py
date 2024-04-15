import sys
from typing import Literal
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget

def get_folder_path(
        parent: QWidget | None = None, 
        caption: str = "选择目录", 
        directory: str | None = None
    ) -> (str | Literal[False]):
    """
    创建文件对话框,获取用户选择目录的路径:
    如果要使用Qt的文件对话框, parent参数不能为None.
    """
    # 文件对话框的选项
    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog  # 使用Qt的文件对话框，而不是本地对话框
    # options |= QFileDialog.ReadOnly # 使文件对话框只读，用户无法编辑文件或目录名。
    options |= QFileDialog.HideNameFilterDetails # 隐藏文件筛选器下拉菜单中的详细信息。
    options |= QFileDialog.ShowDirsOnly # 仅显示目录，而不显示文件。
    options |= QFileDialog.DontResolveSymlinks # 不解析符号链接，而是显示它们的目标。
    # options |= QFileDialog.DontConfirmOverwrite # 不会提示用户确认覆盖已存在的文件。
    file_dialog = QFileDialog()

    # 打开文件对话框,获取用户所选目录绝对路径
    folder_path = file_dialog.getExistingDirectory(parent, caption, directory, options)
    if folder_path:
        return folder_path
    else:
        return False

def get_file_path(
        parent: QWidget | None = None, 
        caption: str = "选择文件", 
        directory: str | None = None,
        filter: str | None = None,
        filter_type: str | None = None,
        initialFilter: str | None = None
    ) -> (str | Literal[False]):
    """
    创建文件对话框,获取用户选择目录的路径:
    如果要使用Qt的文件对话框, parent参数不能为None.

    Args:
    filter_type: Image,

    """
    filter_type_group = {
        "Image": "Image files (*.jpg *.jpeg *.png *.gif);; JPG (*.jpg);; JPEG (*.jpeg);; PNG (*.png);; GIF (*.gif)",
        "Text": "Text files (*.txt *.doc *.docx *.pdf);; Text (*.txt);; Word (*.doc *.docx);; PDF (*.pdf)",
        "Audio": "Audio files (*.mp3 *.wav *.flac *.m4a);; MP3 (*.mp3);; WAV (*.wav);; FLAC (*.flac);; M4A (*.m4a)",
        "Video": "Video files (*.mp4 *.avi *.mov *.mkv);; MP4 (*.mp4);; AVI (*.avi);; MOV (*.mov);; MKV (*.mkv)",
        "Compressed": "Compressed files (*.zip *.rar *.7z);; ZIP (*.zip);; RAR (*.rar);; 7Z (*.7z)",
        "Spreadsheet": "Spreadsheet files (*.xls *.xlsx *.csv);; Excel (*.xls *.xlsx);; CSV (*.csv)",

    }
    if filter_type and isinstance(filter_type, str):
        filter = filter_type_group[filter_type]
        if initialFilter and isinstance(initialFilter, str) and initialFilter in filter:
            pass
        else:
            initialFilter = filter.split(';;')[0]
        
    # 文件对话框的选项
    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog  # 使用Qt的文件对话框，而不是本地对话框
    # options |= QFileDialog.ReadOnly # 使文件对话框只读，用户无法编辑文件或目录名。
    # options |= QFileDialog.HideNameFilterDetails # 隐藏文件筛选器下拉菜单中的详细信息。
    # options |= QFileDialog.ShowDirsOnly # 仅显示目录，而不显示文件。
    options |= QFileDialog.DontResolveSymlinks # 不解析符号链接，而是显示它们的目标。
    # options |= QFileDialog.DontConfirmOverwrite # 不会提示用户确认覆盖已存在的文件。
    file_dialog = QFileDialog()

    # 显示文件对话框
    file_path, _ = file_dialog.getOpenFileName(parent, caption, directory, filter, initialFilter, options)
    if file_path:
        return file_path
    else:
        return False
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    folder_path = get_folder_path()
    print("选择的文件夹路径:", folder_path)
    sys.exit(app.exec_())

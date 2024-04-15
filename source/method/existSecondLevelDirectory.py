import os

def exist_second_level_directory(directory_path) -> bool:
    """检测一个目录中是否存在二级子目录"""
    for root, dirs, files in os.walk(directory_path):
        if dirs:
            for d in dirs:
                for _, sec_dirs, _ in os.walk(os.path.join(root, d)):
                    if sec_dirs:
                        return True
        else:
            return False
    return False
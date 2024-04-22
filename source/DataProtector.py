'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-04-22 23:24:00
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\DataProtector.py
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
import threading
import json
import os
import time
from pinyin import get_initial


# 声明全局变量
# 获取当前文件所在目录的绝对路径
WORKING_DIRECTORY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 图片文件夹路径
IMAGE_FOLDER_PATH = WORKING_DIRECTORY_PATH + r'\phbimage'
# 配置文件夹路径
CONFIG_FOLDER_PATH = WORKING_DIRECTORY_PATH + r'\profiles'
# 读取 PlayerConfig.json 文件并加载为 JSON 对象
with open(CONFIG_FOLDER_PATH + r'\PlayerConfig.json', 'r', encoding='utf-8') as config_json:
    config_js = json.load(config_json)
# 读取 PlayerStyle.json文件并加载为 JSON 对象
with open(CONFIG_FOLDER_PATH + r'\PlayerStyle.json', 'r', encoding='utf-8') as style_json:
    style_js = json.load(style_json)
# 读取 PlayerStyle.css 文件内容为文本
with open(CONFIG_FOLDER_PATH + r'\PlayerStyle.css', 'r', encoding='utf-8') as player_style_css:
    style_css = player_style_css.read()

class DataProtector(object):
    """ 子线程 --数据同步与保存 """

    def __init__(self, app) -> None:
        # 类对象传入
        self.app = app
        # 线程绑定  daemon=True 设置该线程为守护线程,随主线程结束而退出
        self.thread_data_protector = threading.Thread(target=self.callbackfunc, daemon=True, name='DataProtector')
        self.thread_data_protector.start()
        
    def synchronous_data(self) -> None:
        """ 同步数据到 config_js <class 'dict'> """
        try:
            config_js['current_songlist_path'] = self.app.current_songlist_path
            config_js['current_music_number'] = self.app.current_music_number
            config_js['file_total_time'] = self.app.file_total_time
            config_js['current_position'] = self.app.player.time
            config_js['need_cycle'] = self.app.need_cycle
            config_js['current_songlist'] = self.app.current_songlist
            config_js['current_music_name'] = self.app.current_music_name
            
        except AttributeError:
            # 忽略部分属性不存在时带来的报错
            print("AttributeError!")
        except TypeError:
            # 或略配置文件中数据的类型变化,保证在配置文件更改后DataProtector继续运行
            print("TypeError!")
        self.save_data()

    def callbackfunc(self) -> None:
        """ 线程绑定操作 """
        while (True):
            self.synchronous_data()
            time.sleep(1)

    def save_data(self) -> None:
        """ 保存数据到 PlayerConfig.json """
        try:
            # 打开json文件
            with open(CONFIG_FOLDER_PATH + r'\PlayerConfig.json', 'w', encoding='utf-8') as config_json:
                # json文件写入 ensure_ascii=False禁用Unicode转义确保写入的文件包含原始的非ASCII字符。
                json.dump(config_js, config_json, ensure_ascii=False, indent=4)
        except NameError:
            print("NameError!: 请检查json文件的位置.")
    

class DataInitializationMethod(object):
    """数据初始化方法"""
    
    @staticmethod
    def clear_shortcut_settings():
        """清空自定义快捷方案"""
        config_js['custom_shortcut_keys']['next_play'] = "按下快捷键"
        config_js['custom_shortcut_keys']['previous_play'] = "按下快捷键"
        config_js['custom_shortcut_keys']['pause_or_begin'] = "按下快捷键"
        config_js['custom_shortcut_keys']['random_play'] = "按下快捷键"
        config_js['custom_shortcut_keys']['single_cycle_play'] = "按下快捷键"
    
    @staticmethod
    def initialize_image_and_icon_settings():
        """初始化图片/图标设置"""
        with open(CONFIG_FOLDER_PATH + r'\InitialPlayerConfig.json', 'r', encoding='utf-8') as js_file:
            init_config = json.load(js_file)
        # 获取当前文件所在目录的父级目录
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # 手动添加路径分隔符
        if not parent_directory.endswith(os.sep):
            parent_directory += os.sep
        config_js['ApplicationWindowBackGround'] = os.path.join(parent_directory, init_config['ApplicationWindowBackGround'])
        config_js['ApplicationWindowIcon'] = os.path.join(parent_directory, init_config['ApplicationWindowIcon'])
        config_js['SearchUIBackGround'] = os.path.join(parent_directory, init_config['SearchUIBackGround'])
        config_js['SearchUIIcon'] = os.path.join(parent_directory, init_config['SearchUIIcon'])

    @staticmethod
    def data_initialization_detection():
        """数据初始化检测"""
        if not config_js['playlist']:
            config_js['current_songlist_path'] = ""
            config_js['foregoing_songlist_path'] = ""
            config_js['current_music_number'] = "*0*"
            config_js['file_total_time'] = 0
            config_js['current_position'] = 0.0
            config_js['current_music_name'] = ""
            config_js['current_songlist_group'] = "" 
            config_js['current_songlist'] = ""
        if not config_js['opened_times']:
            DataInitializationMethod.initialize_image_and_icon_settings()
        config_js['opened_times'] += 1

def load_playlist(directory_path) -> list[list]:
            """
            加载播放列表:
            将三级目录结构转化为三级列表结构.

            [
                [
                    "二级目录名称",
                    [
                        "三级目录名称",
                        "三级目录绝对路径"
                    ],
                    [
                        "三级目录名称",
                        "三级目录绝对路径"
                    ]
                ],
                [
                    "二级目录名称",
                    [
                        "三级目录名称",
                        "三级目录绝对路径"
                    ]
                ]
            ]
            """
            playlist = []
            for root, dirs, files in os.walk(directory_path):
                if dirs:
                    # 获取全部分组名称
                    playlist = [[d] for d in sorted(dirs, key=lambda x: get_initial(x)[0])] # 按照拼音首字母排序
                    index = 0
                    for d in sorted(dirs, key=lambda x: get_initial(x)[0]):
                        for sec_root, sec_dirs, _ in os.walk(os.path.join(root, d)): # 一级子目录路径
                            if sec_dirs:
                                for sec_d in sorted(sec_dirs, key=lambda x: get_initial(x)[0]):
                                    sec_list = [sec_d] + [os.path.join(sec_root, sec_d)] # 制作歌单项结构
                                    playlist[index].append(sec_list)
                                break
                            else:
                                break
                        index += 1
                    break
                else:
                    break        
            return playlist
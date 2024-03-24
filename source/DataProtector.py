'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-03-24 21:27:34
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
Copyright (c) 2024 by HDJ, All Rights Reserved. 
'''
import threading
import json
import os
import time


# 声明全局变量
# 获取当前文件所在目录的绝对路径
WORKING_DIRECTORY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 图片文件夹路径
IMAGE_FOLDER_PATH = WORKING_DIRECTORY_PATH + r'\phbimage'
# 配置文件夹路径
CONFIG_FOLDER_PATH = WORKING_DIRECTORY_PATH + r'\profiles'
# 读取 PlayerConfig.json, PlayerStyle.json文件并加载为 JSON 对象
with open(CONFIG_FOLDER_PATH + r'\PlayerConfig.json', 'r', encoding='utf-8') as config_json:
    config_js = json.load(config_json)
with open(CONFIG_FOLDER_PATH + r'\PlayerStyle.json', 'r', encoding='utf-8') as style_json:
    style_js = json.load(style_json)
# 读取 PlayerStyle.css 文件内容为文本
with open(CONFIG_FOLDER_PATH + r'\PlayerStyle.css', 'r', encoding='utf-8') as player_style_css:
    style_css = player_style_css.read()

    
class DataProtector(object):
    """ 子线程 --数据同步与保存 """

    def __init__(self, main_window) -> None:
        # 类对象传入
        self.main_window = main_window

        # 线程绑定  daemon=True 设置该线程为守护线程,随主线程结束而退出
        self.thread_data_protector = threading.Thread(
            target=self.callbackfunc, daemon=True, name='DataProtector')
        self.thread_data_protector.start()

    def synchronous_data(self) -> None:
        """ 同步数据到 config_js <class 'dict'> """
        try:
            config_js['music_folder_path'] = self.main_window.music_folder_path
            config_js['current_music_number'] = self.main_window.current_music_number
            config_js['file_total_time'] = self.main_window.file_total_time
            config_js['current_position'] = self.main_window.player.time
            config_js['need_cycle'] = self.main_window.need_cycle
            config_js['play_dict'] = self.main_window.play_dict
            config_js['current_music_name'] = self.main_window.current_music_name
            
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

'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-03-24 20:55:38
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\KeyboardListener.py
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
import pynput.keyboard
import keyboard
from DataProtector import config_js


class KeyboardListener(object):
    """ 
    子线程 --键盘监听操作与键盘快捷方案
    
    QwQ:当前阶段,键盘快捷方式仅用于主UI界面最小化时,或UI界面不在最顶层时.
    """

    def __init__(self, main_window) -> None:
        self.main_window = main_window
        # pynput.keyboard.Listener可以创建新线程,并持续监听键盘
        self.thread_listen = pynput.keyboard.Listener(
            on_press=self.concentrate_key_press_programme)
        self.thread_listen.daemon = True  # 守护线程
        self.thread_listen.name = 'KeyboardListener'
        self.thread_listen.start()

    def concentrate_key_press_programme(self, key, programme=None) -> None | str:
        """ 
        管理快捷方案 
        
        return: 仅在选择的快捷方案存在时返回 str.
        """
        programme_map = {
            "1": self.key_press_p1,
            "2": self.key_press_p2,
            "3": self.key_press_p3,
            "4": self.key_press_p4,
            "5": self.key_press_p5
        }
        programme = config_js['key_press_programme']
        # 关闭键盘快捷方式
        if programme is None:
            return None
        # 选择存在的快捷方案
        elif programme in programme_map.keys():
            return programme_map.get(f'{programme}')(key)
        elif config_js['use_custom_shortcut_keys']:
            return programme_map.get('5')(key)
        # 不存在的快捷方案
        else:
            return None

    def key_press_p1(self, key) -> None:
        """ 键盘快捷键方案1:主键盘 """
        try:
            # 下一首'right'
            if str(key) == 'Key.right':
                print("'right' has been pressed")
                self.main_window.next_play()
            # 上一首'left'
            elif str(key) == 'Key.left':
                print("'left' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'space'
            elif str(key) == 'Key.space':
                print("'space' has been pressed")
                self.main_window.music_pause()
            # 随机播放'r'
            elif key.char == 'r':
                print("'r' has been pressed")
                self.main_window.random_play()
            # 单曲循环'o'
            elif key.char == 'o':
                print("'o' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            # 防止key没有字符/字符串值导致的报错
            pass

    def key_press_p2(self, key) -> None:
        """ 键盘快捷键方案2:Ctrl+主键盘 """
        try:
            # 下一首'Ctrl+d'
            if key.char == '\x04':
                print("'Ctrl+d' has been pressed")
                self.main_window.next_play()
            # 上一首'Ctrl+a'
            elif key.char == '\x01':
                print("'Ctrl+a' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'Ctrl+s'
            elif key.char == '\x13':
                print("'Ctrl+s' has been pressed")
                self.main_window.music_pause()
            # 随机播放'Ctrl+r'
            elif key.char == '\x12':
                print("'Ctrl+r' has been pressed")
                self.main_window.random_play()
            # 单曲循环'Ctrl+q'
            elif key.char == '\x11':
                print("'Ctrl+q' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            # 防止key没有字符值导致的报错
            pass

    def key_press_p3(self, key) -> None:
        """ 键盘快捷键方案3:数字键盘 """
        try:
            # 下一首'6'
            if str(key) == '<102>':
                print("'6' has been pressed")
                self.main_window.next_play()
            # 上一首'4'
            elif str(key) == '<100>':
                print("'4' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'5'
            elif str(key) == '<101>':
                print("'5' has been pressed")
                self.main_window.music_pause()
            # 随机播放'1'
            elif str(key) == '<97>':
                print("'1' has been pressed")
                self.main_window.random_play()
            # 单曲循环'0'
            elif str(key) == '<96>':
                print("'0' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            # 防止key没有字符值导致的报错
            pass

    def key_press_p4(self, key) -> None:
        """ 键盘快捷键方案4:Ctrl+数字键盘(当前使用的第三方库无法区分主键盘数字键与数字键盘的数字键) """
        try:
            # 下一首'Ctrl+6'
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('6'):
                print("'Ctrl+6' has been pressed")
                self.main_window.next_play()
            # 上一首'Ctrl+4'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('4'):
                print("'Ctrl+4' has been pressed")
                self.main_window.previous_play()
            # 暂停/开始'Ctrl+5'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('5'):
                print("'Ctrl+5' has been pressed")
                self.main_window.music_pause()
            # 随机播放'Ctrl+1'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('1'):
                print("'Ctrl+1' has been pressed")
                self.main_window.random_play()
            # 单曲循环'Ctrl+0'
            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('0'):
                print("'Ctrl+0' has been pressed")
                self.main_window.single_cycle_play()
        except AttributeError:
            pass
    
    def key_press_p5(self, key) -> None:
    #     content = {
    #     "播放下一首":[self.main_window.next_play()],
    #     "播放上一首":[self.main_window.previous_play()],
    #     "开始/暂停播放":[self.main_window.music_pause()],
    #     "随机播放":[self.main_window.random_play()],
    #     "循环播放":[self.main_window.single_cycle_play()]
    # }
        try:
            # 下一首
            if keyboard.is_pressed(config_js['custom_shortcut_keys']['next_play']):
                self.main_window.next_play()
            # 上一首
            elif keyboard.is_pressed(config_js['custom_shortcut_keys']['previous_play']):
                self.main_window.previous_play()
            # 暂停/开始
            elif keyboard.is_pressed(config_js['custom_shortcut_keys']['music_pause']):
                self.main_window.music_pause()
            # 随机播放
            elif keyboard.is_pressed(config_js['custom_shortcut_keys']['random_play']):
                self.main_window.random_play()
            # 单曲循环
            elif keyboard.is_pressed(config_js['custom_shortcut_keys']['single_cycle_play']):
                self.main_window.single_cycle_play()
        except AttributeError:
            pass

        

        
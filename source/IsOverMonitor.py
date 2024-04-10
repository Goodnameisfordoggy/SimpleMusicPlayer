'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-01-18 19:55:59
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\IsOverMonitor.py
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
import time
from PyQt5.QtCore import QTimer


class IsOverMonitor(object):
    """ 子线程--播放完毕检测 """

    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.which_play)  # 绑定方法
        self.timer_interval = 1000  # 定时器间隔，单位是毫秒
        self.timer.start(self.timer_interval)

    def is_over(self) -> bool:
        """ 播放完成检测 """
        if self.main_window.player.time > self.main_window.file_total_time:
            print("Next")
            return True

    def which_play(self) -> None:
        """ 播放完成后播放方式的选择 """
        if self.is_over():
            time.sleep(2)
            if self.main_window.need_cycle:
                self.main_window.play_song()
            else:
                self.main_window.random_play()

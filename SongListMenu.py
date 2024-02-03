'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-01-18 20:36:52
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\SongListMenu.py
Description: 

				*		写字楼里写字间，写字间里程序员；
				*		程序人员写程序，又拿程序换酒钱。
				*		酒醒只在网上坐，酒醉还来网下眠；
				*		酒醉酒醒日复日，网上网下年复年。
				*		但愿老死电脑间，不愿鞠躬老板前；
				*		奔驰宝马贵者趣，公交自行程序员。
				*		别人笑我忒疯癫，我笑自己命太贱；
				*		不见满街漂亮妹，哪个归得程序员？    
Copyright (c) ${2024} by ${HDJ}, All Rights Reserved. 
'''
from Simple_Qt import Menu, Action
from DataProtector import style_css, config_js


class ChangeFolderMenu(object):
    """ 一级菜单--更改文件夹(歌单) """

    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window
        # 底层变量
        self.menu_change_folder_path = None  # 一级菜单对象
        # 方法绑定
        self.build_menu()

    def build_menu(self) -> None:
        """ 创建菜单,用于显示用户自定义的歌单 """

        # 一级菜单
        self.menu_change_folder_path = Menu.create(
            parent=self.main_window,
            title='更改文件夹',
            ObjectName='menu--1',
            StyleSheet=style_css,
            superior=self.main_window.menubar
        )
        # 在config_js的music_folders_path中找到所有一级菜单名
        secmenu_names = [js_secmenu[0] for js_secmenu in config_js["music_folders_path"]]
        # 以二级菜单个数作为循环结束条件
        for i in range(0, len(config_js["music_folders_path"])):
            # 创建二级菜单
            secmenu = Menu.create(
                parent=self.main_window,
                title=secmenu_names[i],
                ObjectName='menu--1',
                StyleSheet=style_css,
                superior=self.menu_change_folder_path
            )
            # 在config_js的music_folders_path中找到当先二级菜单下的所有三级菜单列表
            actions = config_js["music_folders_path"][i][1:]
            # 创建三级菜单
            for action_name, action_path in actions:
                if isinstance(action_name, str) and isinstance(action_path, str):
                    action = Action.create(
                        parent=self.main_window,
                        text=f'{action_name}',
                        triggered_callback=[self.change_music_path, action_path],
                        superior=secmenu
                    )

    def change_music_path(self, path: str) -> None:
        """ 更改文件夹路径(菜单项绑定操作),用于切换歌单 """
        self.main_window.music_folder_path = path
        self.main_window.update_song_list()

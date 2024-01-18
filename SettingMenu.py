'''
Author: HDJ
StartDate: 2023-6-14 00:00:00
LastEditTime: 2024-01-18 19:21:27
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\SettingMenu.py
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
import os
from PyQt5.QtWidgets import QMessageBox
from MyWidgetMethod import PackingCreateMethod
from DataProtector import CONFIG_FOLDER_PATH, IMAGE_FOLDER_PATH, style_css


class SettingMenu(object):
    """ 一级菜单--设置 """

    def __init__(self, main_window) -> None:
        # 一级UI对象传入
        self.main_window = main_window
        # 底层变量
        self.menu_setting = None  # 一级菜单对象
        # 方法绑定
        self.build_menu()

    def build_menu(self) -> None:
        # 创建一级菜单
        self.menu_setting = PackingCreateMethod.my_menu(
            parent=self.main_window,
            title='⚙️',
            ObjectName='menu--1',
            StyleSheet=style_css,
            superior=self.main_window.menubar
        )
        # 创建二级菜单操作
        configuration_files_menu = self.ConfigurationFilesMenu(self)

###############################################################################
        # 创建二级菜单(样式选择)
        secmenu_style_selection = PackingCreateMethod.my_menu(
            parent=self.main_window,
            title=' ❖样式',
            ObjectName='menu--1',
            StyleSheet=style_css,
            superior=self.menu_setting
        )

    class ConfigurationFilesMenu(object):
        """ 
        二级菜单--配置文件

        提供打开配置文件的操作
        """

        def __init__(self, setting_menu) -> None:
            # 一级菜单SettingMenu对象传入
            self.setting_menu = setting_menu
            # 一级UI对象
            # self.setting_menu.main_window
            # 底层变量
            self.secmenu_setting_files = None  # 二级菜单对象
            # 方法绑定
            self.build_menu()

        def build_menu(self) -> None:
            # 创建二级菜单
            self.secmenu_setting_files = PackingCreateMethod.my_menu(
                parent=self.setting_menu.main_window,
                title=' 📖配置文件',
                ObjectName='menu--1',
                StyleSheet=style_css,
                superior=self.setting_menu.menu_setting
            )
            # 创建三级菜单
            action_json1 = PackingCreateMethod.my_action(
                parent=self.setting_menu.main_window,
                text="PlayerConfig.js",
                triggered_callback=lambda: self.open_selected_file(
                    CONFIG_FOLDER_PATH + r'\PlayerConfig.json'),
                Icon_path=IMAGE_FOLDER_PATH + r"\Json File Image.png",
                superior=self.secmenu_setting_files
            )
            action_json2 = PackingCreateMethod.my_action(
                parent=self.setting_menu.main_window,
                text="PlayerStyle.js",
                triggered_callback=lambda: self.open_selected_file(
                    CONFIG_FOLDER_PATH + r'\PlayerStyle.json'),
                Icon_path=IMAGE_FOLDER_PATH + r"\Json File Image.png",
                superior=self.secmenu_setting_files
            )
            action_css = PackingCreateMethod.my_action(
                parent=self.setting_menu.main_window,
                text="PlayerStyle.css",
                triggered_callback=lambda: self.open_selected_file(
                    CONFIG_FOLDER_PATH + r'\PlayerStyle.css'),
                Icon_path=IMAGE_FOLDER_PATH + r"\Css File Image.png",
                superior=self.secmenu_setting_files
            )

        def open_selected_file(self, file_path) -> None:
            """ 菜单项的绑定操作,用于打开选中的文件"""
            try:
                # 使用系统默认程序打开文件
                os.startfile(file_path)
            except FileNotFoundError:
                QMessageBox.critical(
                    self.main_window, 'FileNotFoundError', '文件不存在,请检查文件位置', QMessageBox.Ok)

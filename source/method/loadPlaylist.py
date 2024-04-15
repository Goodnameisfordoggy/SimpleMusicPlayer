'''
Author: HDJ
StartDate: please fill in
LastEditTime: 2024-04-13 21:55:01
FilePath: \pythond:\LocalUsers\Goodnameisfordoggy-Gitee\a-simple-MusicPlayer\source\method\loadPlaylist.py
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
import os
from pinyin import get_initial

def load_playlist(directory_path) -> list[list]:
            """
            加载播放列表:
            将目录结构转化为三级列表结构.
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

if __name__ == "__main__":
    folder_path = r"F:/music"
    print(load_playlist(folder_path))